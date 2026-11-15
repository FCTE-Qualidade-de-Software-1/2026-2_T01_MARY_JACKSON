"""Coleta automatizada de Eficiencia de Desempenho (Dupla 2).

Abre o Google Chrome instalado na maquina, executa as operacoes do plano de
avaliacao (Fase 3) e grava um trace do Chrome por operacao, no mesmo formato
do painel Performance do DevTools. Os traces sao lidos depois por
ler_traces.py.

Ao detectar o fim de cada operacao (formas na tela, novo rotulo na tela,
dialogo "Save as" ou pagina de impressao aberta), o script grava a marca
"fim_operacao" no trace, usada por ler_traces.py para definir tf.

Sessoes de cada tentativa, cada uma em um perfil novo e limpo do navegador:
    A: abre a carga (M2.1 e M2.2) e edita o rotulo da forma v0001 (M2.3)
    B, C, D: abre a carga sem gravar e exporta em PNG, PDF e SVG (M2.4 e M2.5)

Uso (na pasta dados/avaliacao/eficiencia, com o draw.io rodando em localhost:8080):
    python coletar.py --piloto                 1 tentativa, portes 50 e 5000
    python coletar.py                          5 tentativas, todos os portes
    python coletar.py --portes 50 300 --tentativas 1 2

Requisitos: pip install playwright   (usa o Chrome instalado; nao precisa de
"playwright install")
"""
import argparse
import asyncio
import gzip
import json
import sys
import time
from pathlib import Path

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

URL = "http://localhost:8080/?offline=1"
PORTES = [50, 300, 1000, 2000, 5000]
FORMATOS = ["png", "pdf", "svg"]
VIEWPORT = {"width": 1366, "height": 768}
CATEGORIAS = [
    "-*", "devtools.timeline", "disabled-by-default-devtools.timeline",
    "disabled-by-default-devtools.timeline.frame", "v8.execute", "blink.user_timing",
    "disabled-by-default-devtools.screenshot",
]
LIMITE_OPERACAO_S = 180   # tempo maximo de espera por operacao antes de registrar falha
ESPERA_APOS_ABRIR_S = 3   # garante a leitura do heap 2 s apos a abertura
ESPERA_APOS_ROTULO_S = 2
ESPERA_APOS_EXPORTAR_S = 1.5
# Sem a API File System Access, o draw.io usa o seletor <input type=file>,
# que pode ser preenchido pela automacao. O seletor nativo nao pode.
#
# No PDF, o draw.io prepara uma pagina de impressao em uma nova janela e chama
# print() nela; a impressao do navegador bloquearia a pagina ate alguem fechar
# o dialogo. Por isso print() e substituido por uma funcao que apenas grava a
# marca "fim_operacao" no trace: a preparacao da pagina pelo draw.io e medida
# por inteiro, e o PDF gerado pelo navegador nao faz parte da medida.
SCRIPT_INICIAL = """
delete Window.prototype.showOpenFilePicker;
delete window.showOpenFilePicker;
(() => {
  const abrirJanela = window.open;
  window.open = function (...args) {
    const janela = abrirJanela.apply(this, args);
    try {
      if (janela) {
        janela.print = function () {
          window.__impressaoChamada = true;
          performance.mark("fim_operacao");
        };
      }
    } catch (erro) {}
    return janela;
  };
})();
"""


class Falha(Exception):
    pass


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


async def nova_sessao(navegador):
    contexto = await navegador.new_context(viewport=VIEWPORT, locale="en-US",
                                           accept_downloads=False)
    await contexto.add_init_script(SCRIPT_INICIAL)
    pagina = await contexto.new_page()
    await pagina.goto(URL)
    await pagina.get_by_text("File", exact=True).wait_for(timeout=60_000)
    await pagina.wait_for_timeout(1500)
    cdp = await contexto.new_cdp_session(pagina)
    return contexto, pagina, cdp


async def coletar_lixo(pagina, cdp):
    await cdp.send("HeapProfiler.collectGarbage")
    await pagina.wait_for_timeout(1000)


async def abrir(pagina, carga: Path):
    await pagina.get_by_text("File", exact=True).click()
    await pagina.get_by_text("Open from").first.hover()
    async with pagina.expect_file_chooser() as escolha:
        await pagina.get_by_text("Device...").first.click()
    await (await escolha.value).set_files(str(carga))
    await pagina.get_by_text("Rotulo 0001", exact=True).wait_for(
        state="attached", timeout=LIMITE_OPERACAO_S * 1000)


async def editar_rotulo(pagina):
    caixa = await pagina.get_by_text("Rotulo 0001", exact=True).bounding_box()
    await pagina.mouse.click(caixa["x"] + caixa["width"] / 2, caixa["y"] + caixa["height"] / 2)
    await pagina.wait_for_timeout(500)
    await pagina.keyboard.press("F2")
    await pagina.wait_for_timeout(500)
    await pagina.keyboard.press("Control+A")
    await pagina.keyboard.type("Rotulo A001", delay=30)
    await pagina.wait_for_timeout(500)
    await pagina.keyboard.press("Control+Enter")
    await pagina.get_by_text("Rotulo A001", exact=True).wait_for(
        state="attached", timeout=LIMITE_OPERACAO_S * 1000)


async def preparar_exportacao(pagina, formato):
    await pagina.get_by_text("File", exact=True).click()
    await pagina.get_by_text("Export as").first.hover()
    await pagina.wait_for_timeout(300)
    await pagina.get_by_text(f"{formato.upper()}...", exact=True).first.click()
    await pagina.get_by_role("button", name="Export").wait_for(timeout=30_000)
    await pagina.wait_for_timeout(800)


async def exportar(pagina, formato):
    """Clica em Export e espera o fim da geracao: o dialogo "Save as" (PNG e
    SVG) ou a chamada de print() na pagina de impressao (PDF)."""
    botao = pagina.get_by_role("button", name="Export")
    if formato == "pdf":
        async with pagina.context.expect_page(timeout=LIMITE_OPERACAO_S * 1000) as nova:
            await botao.click()
        impressao = await nova.value
        await pagina.wait_for_function("window.__impressaoChamada === true",
                                       timeout=LIMITE_OPERACAO_S * 1000)
        return impressao
    await botao.click()
    await pagina.get_by_text("Save as:").wait_for(timeout=LIMITE_OPERACAO_S * 1000)
    return None


def compactar(origem: Path, destino: Path):
    """Grava o trace em .json.gz. URLs do tipo data: (conteudo de imagens
    geradas pelo draw.io durante a exportacao) sao truncadas em 200
    caracteres; o restante do trace nao e alterado."""
    dados = json.loads(origem.read_bytes())
    eventos = dados["traceEvents"] if isinstance(dados, dict) else dados
    for e in eventos:
        info = e.get("args", {}).get("data")
        if isinstance(info, dict) and str(info.get("url", "")).startswith("data:") \
                and len(info["url"]) > 200:
            info["url"] = info["url"][:200] + "...(truncado)"
    with gzip.open(destino, "wt", encoding="utf-8") as saida:
        json.dump(dados, saida)


async def gravar(navegador, pagina, destino: Path, acao, espera_s):
    temporario = destino.with_suffix("")  # .json
    await navegador.start_tracing(page=pagina, path=str(temporario), screenshots=True,
                                  categories=CATEGORIAS)
    try:
        resultado = await acao()
        # Marca no trace o instante em que o fim da operacao foi detectado.
        await pagina.evaluate("performance.mark('fim_operacao')")
        await pagina.wait_for_timeout(espera_s * 1000)
    finally:
        await navegador.stop_tracing()
        compactar(temporario, destino)
        temporario.unlink()
    return resultado


async def sessao_abrir_rotulo(navegador, carga, pasta, prefixo, porte, t):
    contexto, pagina, cdp = await nova_sessao(navegador)
    try:
        await coletar_lixo(pagina, cdp)
        await gravar(navegador, pagina, pasta / f"{prefixo}p{porte:05d}_abrir_t{t}.json.gz",
                     lambda: abrir(pagina, carga), ESPERA_APOS_ABRIR_S)
        log(f"  abrir ok")
        await gravar(navegador, pagina, pasta / f"{prefixo}p{porte:05d}_rotulo_t{t}.json.gz",
                     lambda: editar_rotulo(pagina), ESPERA_APOS_ROTULO_S)
        log(f"  rotulo ok")
    finally:
        await contexto.close()


async def sessao_exportar(navegador, carga, pasta, prefixo, porte, t, formato):
    contexto, pagina, cdp = await nova_sessao(navegador)
    try:
        await abrir(pagina, carga)
        await pagina.wait_for_timeout(1500)
        await preparar_exportacao(pagina, formato)
        await coletar_lixo(pagina, cdp)
        impressao = await gravar(
            navegador, pagina, pasta / f"{prefixo}p{porte:05d}_exportar-{formato}_t{t}.json.gz",
            lambda: exportar(pagina, formato), ESPERA_APOS_EXPORTAR_S)
        if impressao is not None:
            await impressao.close(run_before_unload=False)
        log(f"  exportar {formato} ok")
    finally:
        await contexto.close()


async def principal(args):
    pasta = Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)
    cargas = Path(args.cargas)
    prefixo = "piloto_" if args.piloto else ""
    falhas = pasta / "falhas.txt"
    async with async_playwright() as p:
        opcoes = {"headless": args.headless}
        if not args.chromium:
            opcoes["channel"] = "chrome"
        navegador = await p.chromium.launch(**opcoes)
        log(f"navegador: {navegador.version}")
        for porte in args.portes:
            carga = cargas / f"carga-{porte:05d}.drawio"
            for t in args.tentativas:
                etapas = [("abrir/rotulo", lambda: sessao_abrir_rotulo(
                    navegador, carga, pasta, prefixo, porte, t))]
                for formato in args.formatos:
                    etapas.append((f"exportar {formato}", lambda f=formato: sessao_exportar(
                        navegador, carga, pasta, prefixo, porte, t, f)))
                log(f"porte {porte}, tentativa {t}")
                for nome, etapa in etapas:
                    try:
                        await etapa()
                    except (PWTimeout, Falha) as erro:
                        msg = f"porte {porte} tentativa {t} {nome}: {type(erro).__name__}"
                        log("  FALHA " + msg)
                        with falhas.open("a", encoding="utf-8") as f:
                            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
        await navegador.close()
    log("coleta concluida")


def argumentos():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--piloto", action="store_true", help="1 tentativa nos portes 50 e 5000, em brutos/piloto")
    a.add_argument("--portes", type=int, nargs="+")
    a.add_argument("--tentativas", type=int, nargs="+")
    a.add_argument("--formatos", nargs="+", default=FORMATOS)
    a.add_argument("--cargas", default="cargas")
    a.add_argument("--saida")
    a.add_argument("--headless", action="store_true", help="sem janela (apenas para testes)")
    a.add_argument("--chromium", action="store_true", help="usa o Chromium do Playwright (apenas para testes)")
    args = a.parse_args()
    if args.piloto:
        args.portes = args.portes or [50, 5000]
        args.tentativas = args.tentativas or [1]
        args.saida = args.saida or "brutos/piloto"
    args.portes = args.portes or PORTES
    args.tentativas = args.tentativas or [1, 2, 3, 4, 5]
    args.saida = args.saida or "brutos/traces"
    return args


if __name__ == "__main__":
    asyncio.run(principal(argumentos()))
