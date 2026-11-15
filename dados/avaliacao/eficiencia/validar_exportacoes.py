"""Validacao dos arquivos exportados pelo draw.io (Dupla 2).

Complementa a coleta de Eficiencia de Desempenho. A coleta (coletar.py) mede
o tempo ate o draw.io concluir a exportacao, mas nao salva os arquivos. Este
script exporta e salva um arquivo de cada formato para cada porte e verifica
se o arquivo e valido e se contem o diagrama. Nao mede tempo.

    PNG: assinatura do formato e dimensoes da imagem, comparadas com a area
         ocupada pelas formas da carga (imagem cortada ou incompleta mudaria
         as dimensoes).
    SVG: XML valido e quantidade de rotulos distintos "Rotulo NNNN" igual ao
         numero de formas da carga.
    PDF: o draw.io prepara a pagina de impressao e o PDF e gerado pelo
         mecanismo de impressao do Chrome (o mesmo do "Salvar como PDF"),
         acionado por automacao. Verifica a assinatura do formato e conta as
         paginas e os rotulos distintos presentes no texto do PDF.

Uso (na pasta dados/avaliacao/eficiencia, com o draw.io rodando em localhost:8080):
    python validar_exportacoes.py
    python validar_exportacoes.py --portes 50 300
    python validar_exportacoes.py --portes 5000 --formatos svg --janela

Ao rodar de novo para alguns portes ou formatos, apenas as linhas
correspondentes de validacao.csv sao substituidas.

Saida: brutos/exportados/ com os arquivos e validacao.csv, que separa se o
arquivo abre (formato valido) de se o diagrama esta completo nele.
Requisitos: pip install playwright pypdf
"""
import argparse
import asyncio
import csv
import re
import struct
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from playwright.async_api import async_playwright

URL = "http://localhost:8080/?offline=1"
PORTES = [50, 300, 1000, 2000, 5000]
FORMATOS = ["png", "svg", "pdf"]
LIMITE_S = 300  # espera maxima por etapa, em segundos (alteravel com --limite)
ROTULO = re.compile(rb"Rotulo (\d{4})")
# Sem as APIs File System Access, o draw.io usa o seletor <input type=file>
# para abrir e oferece "Download" para salvar, o que permite a automacao.
# print() e substituida por uma marca e close() e neutralizada; o PDF e gerado
# em seguida pelo Chrome a partir da mesma pagina de impressao.
SCRIPT_INICIAL = """
delete Window.prototype.showOpenFilePicker; delete window.showOpenFilePicker;
delete Window.prototype.showSaveFilePicker; delete window.showSaveFilePicker;
(() => {
  const abrirJanela = window.open;
  window.open = function (...args) {
    const janela = abrirJanela.apply(this, args);
    try {
      if (janela) {
        janela.print = function () { window.__impressaoChamada = true; };
        janela.close = function () {};  // mantem a pagina aberta para gerar o PDF
      }
    }
    catch (erro) {}
    return janela;
  };
})();
"""


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


def area_esperada(porte: int):
    """Largura e altura, em px, da area das formas geradas por gerar_cargas.py
    (grade de 50 colunas, formas de 120 x 60 px, passo de 160 x 100 px), mais
    1 px de cada lado do contorno."""
    colunas, linhas = min(porte, 50), -(-porte // 50)
    return (colunas - 1) * 160 + 120 + 2, (linhas - 1) * 100 + 60 + 2


def validar_png(caminho: Path, porte: int):
    dados = caminho.read_bytes()
    if dados[:8] != b"\x89PNG\r\n\x1a\n" or dados[12:16] != b"IHDR":
        return False, False, "assinatura PNG invalida"
    largura, altura = struct.unpack(">II", dados[16:24])
    esperado = area_esperada(porte)
    return True, (largura, altura) == esperado, \
        f"{largura} x {altura} px (area do diagrama: {esperado[0]} x {esperado[1]} px)"


def validar_svg(caminho: Path, porte: int):
    dados = caminho.read_bytes()
    try:
        ET.fromstring(dados)
    except ET.ParseError as erro:
        return False, False, f"XML invalido: {erro}"
    rotulos = len(set(ROTULO.findall(dados)))
    return True, rotulos == porte, f"{rotulos} de {porte} rotulos"


def validar_pdf(caminho: Path, porte: int):
    dados = caminho.read_bytes()
    if not dados.startswith(b"%PDF-"):
        return False, False, "assinatura PDF invalida"
    try:
        from pypdf import PdfReader
    except ImportError:
        paginas = len(re.findall(rb"/Type\s*/Page(?!s)", dados))
        return paginas > 0, "", f"{paginas} paginas (instale pypdf para contar os rotulos)"
    leitor = PdfReader(str(caminho))
    caixa = leitor.pages[0].mediabox
    tamanho = f"{float(caixa.width) * 25.4 / 72:.0f} x {float(caixa.height) * 25.4 / 72:.0f} mm"
    # Cada pagina e lida separadamente: um rotulo cortado entre duas paginas
    # nao aparece inteiro em nenhuma delas e nao e contado.
    encontrados = set()
    for pagina in leitor.pages:
        encontrados.update(ROTULO.findall((pagina.extract_text() or "").encode()))
    rotulos = len(encontrados)
    return len(leitor.pages) > 0, rotulos == porte, \
        f"{len(leitor.pages)} paginas de {tamanho}, {rotulos} de {porte} rotulos inteiros"


VALIDADORES = {"png": validar_png, "svg": validar_svg, "pdf": validar_pdf}


async def abrir(pagina, carga: Path):
    await pagina.get_by_text("File", exact=True).click()
    await pagina.get_by_text("Open from").first.hover()
    async with pagina.expect_file_chooser() as escolha:
        await pagina.get_by_text("Device...").first.click()
    await (await escolha.value).set_files(str(carga))
    await pagina.get_by_text("Rotulo 0001", exact=True).wait_for(state="attached", timeout=LIMITE_S * 1000)
    await pagina.wait_for_timeout(1000)


async def exportar(navegador, carga: Path, porte: int, formato: str, destino: Path):
    contexto = await navegador.new_context(viewport={"width": 1366, "height": 768},
                                           locale="en-US", accept_downloads=True)
    await contexto.add_init_script(SCRIPT_INICIAL)
    try:
        pagina = await contexto.new_page()
        await pagina.goto(URL)
        await pagina.get_by_text("File", exact=True).wait_for(timeout=60_000)
        await abrir(pagina, carga)
        await pagina.get_by_text("File", exact=True).click()
        await pagina.get_by_text("Export as").first.hover()
        await pagina.wait_for_timeout(300)
        await pagina.get_by_text(f"{formato.upper()}...", exact=True).first.click()
        botao = pagina.get_by_role("button", name="Export")
        await botao.wait_for(timeout=30_000)
        await pagina.wait_for_timeout(500)
        if formato == "pdf":
            async with contexto.expect_page(timeout=LIMITE_S * 1000) as nova:
                await botao.click()
            impressao = await nova.value
            await pagina.wait_for_function("window.__impressaoChamada === true", timeout=LIMITE_S * 1000)
            await impressao.pdf(path=str(destino), prefer_css_page_size=True, print_background=True)
        else:
            await botao.click()
            # Sem a API de salvamento, o dialogo "Save as" oferece "Download" e o botao OK.
            salvar = pagina.get_by_role("button", name="OK", exact=True)
            await salvar.wait_for(timeout=LIMITE_S * 1000)
            async with pagina.expect_download(timeout=LIMITE_S * 1000) as baixado:
                await salvar.click()
            await (await baixado.value).save_as(str(destino))
    finally:
        await contexto.close()


async def principal(args):
    global LIMITE_S
    LIMITE_S = args.limite
    pasta = Path(args.saida)
    pasta.mkdir(parents=True, exist_ok=True)
    relatorio = pasta / "validacao.csv"
    anteriores = {}
    if relatorio.exists():
        with relatorio.open(newline="", encoding="utf-8") as f:
            anteriores = {(int(l["porte"]), l["formato"]): l for l in csv.DictReader(f)}
    linhas = []
    async with async_playwright() as p:
        opcoes = {} if args.chromium else {"channel": "chrome"}
        # O PDF e gerado com page.pdf(), disponivel apenas sem janela. PNG e
        # SVG podem rodar com a janela visivel (--janela), como na coleta: sem
        # janela, o Chrome pode demorar muito mais no SVG dos portes grandes.
        sem_janela = await p.chromium.launch(headless=True, **opcoes)
        com_janela = await p.chromium.launch(headless=False, **opcoes) if args.janela else None
        log(f"navegador: {sem_janela.version}" + (" (PNG e SVG com janela)" if args.janela else ""))
        for porte in args.portes:
            carga = Path(args.cargas) / f"carga-{porte:05d}.drawio"
            for formato in args.formatos:
                destino = pasta / f"p{porte:05d}.{formato}"
                linha = {"porte": porte, "formato": formato, "arquivo": destino.name}
                try:
                    navegador = com_janela if (com_janela and formato != "pdf") else sem_janela
                    await exportar(navegador, carga, porte, formato, destino)
                    abre, completo, detalhe = VALIDADORES[formato](destino, porte)
                    sim = lambda v: "" if v == "" else ("sim" if v else "nao")
                    linha.update(bytes=destino.stat().st_size, abre=sim(abre),
                                 diagrama_completo=sim(completo), detalhe=detalhe)
                except Exception as erro:
                    linha.update(bytes="", abre="nao", diagrama_completo="nao",
                                 detalhe=f"erro: {type(erro).__name__}: {str(erro)[:120]}")
                log(f"porte {porte} {formato}: abre {linha['abre']}, completo "
                    f"{linha['diagrama_completo']} ({linha['detalhe']})")
                linhas.append(linha)
        await sem_janela.close()
        if com_janela:
            await com_janela.close()
    for linha in linhas:
        anteriores[(int(linha["porte"]), linha["formato"])] = linha
    ordem = {f: i for i, f in enumerate(FORMATOS)}
    with relatorio.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=["porte", "formato", "arquivo", "bytes", "abre",
                                                 "diagrama_completo", "detalhe"])
        escritor.writeheader()
        escritor.writerows(anteriores[k] for k in sorted(anteriores, key=lambda k: (k[0], ordem.get(k[1], 9))))
    log(f"resultado em {relatorio}")


def argumentos():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--portes", type=int, nargs="+", default=PORTES)
    a.add_argument("--formatos", nargs="+", default=FORMATOS)
    a.add_argument("--cargas", default="cargas")
    a.add_argument("--saida", default="brutos/exportados")
    a.add_argument("--limite", type=int, default=LIMITE_S, help="espera maxima por etapa, em segundos")
    a.add_argument("--janela", action="store_true", help="PNG e SVG com a janela do Chrome visivel")
    a.add_argument("--chromium", action="store_true", help="usa o Chromium do Playwright (apenas para testes)")
    return a.parse_args()


if __name__ == "__main__":
    asyncio.run(principal(argumentos()))
