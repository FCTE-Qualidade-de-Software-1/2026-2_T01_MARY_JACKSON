"""Extrai as medidas de Eficiencia de Desempenho (M2.1 a M2.5) dos traces do Chrome.

Le os traces salvos pelo painel Performance do DevTools (.json.gz ou .json) e
gera um CSV com uma linha por gravacao. O script apenas le os traces, sem
altera-los. Os criterios de leitura estao documentados na Fase 3.

Nome esperado dos arquivos:
    [piloto_]p<porte>_<operacao>[-<formato>][_t<tentativa>].json.gz
    exemplos: p00050_abrir_t1.json.gz, p05000_exportar-pdf_t3.json.gz
    operacoes: abrir (M2.1 e M2.2), rotulo (M2.3), exportar (M2.4 e M2.5)

Criterios:
    - Thread analisado: thread principal do renderer da pagina localhost.
    - Tarefas: RunTask de pelo menos 1 ms. Tarefas que so tratam movimento
      do mouse sao ignoradas.
    - ti (abrir): inicio da primeira tarefa apos o seletor de arquivos fechar,
      ou seja, apos o ultimo clique e um intervalo ocioso de pelo menos 500 ms.
    - ti (rotulo): inicio do tratamento da ultima tecla pressionada (Ctrl+Enter).
    - ti (exportar): inicio do tratamento do ultimo clique (botao Exportar).
    - tf: fim da ultima tarefa da sequencia de processamento iniciada em ti;
      a sequencia termina no primeiro intervalo de mais de 250 ms sem tarefas.
    - M2.2: heap JS usado 2 s apos tf (ultima amostra ate tf + 2 s).
    - M2.5: maior heap JS usado entre ti e tf.
    - MiB = bytes / 2^20.

Colunas manuais (memoria_em_uso_pct, resultado, observacao) ja preenchidas no
CSV de saida sao preservadas quando o script e executado de novo.

Uso: python ler_traces.py <pasta_dos_traces> <csv_de_saida> [versao_chrome]
"""
import csv
import gzip
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

VERSAO_CHROME_PADRAO = "157.0.8103.79"
TAREFA_MIN_US = 1_000
OCIOSO_SELETOR_US = 500_000
FIM_SEQUENCIA_US = 250_000
HEAP_APOS_US = 2_000_000
MOVIMENTO = {"mousemove", "pointermove", "mouseover", "pointerover", "mouseout",
             "pointerout", "mouseenter", "pointerenter", "mouseleave", "pointerleave"}
CLIQUE = {"click", "pointerup", "mouseup"}
NOME = re.compile(r"^(?:piloto_)?p(\d+)_([a-z]+)(?:-([a-z]+))?(?:_t(\d+))?$")
COLUNAS = ["data", "tentativa", "porte", "operacao", "formato", "versao_chrome",
           "memoria_em_uso_pct", "tempo_ms", "heap_mib", "resultado", "observacao",
           "trace", "ti_ms", "tf_ms"]
MANUAIS = ["memoria_em_uso_pct", "resultado", "observacao"]
FUSO = timezone(timedelta(hours=-3))  # horario de Brasilia


def carregar(caminho: Path) -> dict:
    bruto = caminho.read_bytes()
    if bruto[:2] == b"\x1f\x8b":
        bruto = gzip.decompress(bruto)
    dados = json.loads(bruto)
    return dados if isinstance(dados, dict) else {"traceEvents": dados}


def thread_principal(eventos):
    pids = set()
    for e in eventos:
        if e.get("name") == "TracingStartedInBrowser":
            for f in e["args"]["data"].get("frames", []):
                if "localhost" in f.get("url", "") and f.get("isOutermostMainFrame"):
                    pids.add(f["processId"])
    for e in eventos:
        if (e.get("ph") == "M" and e.get("name") == "thread_name"
                and e["args"].get("name") == "CrRendererMain" and e["pid"] in pids):
            return e["pid"], e["tid"]
    raise ValueError("thread principal da pagina localhost nao encontrado")


def tarefas_e_eventos(eventos, pid, tid):
    principal = [e for e in eventos if e.get("pid") == pid and e.get("tid") == tid]
    despachos = sorted((e["ts"], e["args"]["data"].get("type", ""))
                       for e in principal if e.get("name") == "EventDispatch")
    tarefas = []
    for e in principal:
        if e.get("name") == "RunTask" and e.get("dur", 0) >= TAREFA_MIN_US:
            ini, fim = e["ts"], e["ts"] + e["dur"]
            tipos = {t for ts, t in despachos if ini <= ts <= fim}
            if tipos and tipos <= MOVIMENTO:
                continue
            tarefas.append((ini, fim))
    tarefas.sort()
    return tarefas, despachos


def fim_da_sequencia(tarefas, ti):
    tf = None
    for ini, fim in tarefas:
        if fim < ti:
            continue
        if tf is not None and ini - tf > FIM_SEQUENCIA_US:
            break
        tf = fim if tf is None else max(tf, fim)
    return tf


def tarefa_que_contem(tarefas, ts):
    for ini, fim in tarefas:
        if ini <= ts <= fim:
            return ini
    return ts


def medir(caminho: Path, versao_chrome: str) -> dict:
    nome = caminho.name.split(".")[0]
    m = NOME.match(nome)
    if not m:
        raise ValueError(f"nome fora do padrao: {caminho.name}")
    porte, operacao, formato, tentativa = int(m[1]), m[2], m[3] or "", m[4] or "1"
    dados = carregar(caminho)
    eventos = dados["traceEvents"]
    pid, tid = thread_principal(eventos)
    tarefas, despachos = tarefas_e_eventos(eventos, pid, tid)
    janela = dados.get("metadata", {}).get("modifications", {}).get("initialBreadcrumb", {}).get("window")
    t0 = janela["min"] if janela else min(e["ts"] for e in eventos if e.get("ts", 0) > 0)
    t_max = janela["max"] if janela else max(e["ts"] for e in eventos if e.get("ts", 0) > 0)
    obs = []

    if operacao == "abrir":
        cliques = [ts for ts, t in despachos if t in CLIQUE]
        ref = cliques[-1] if cliques else t0
        ti, anterior = None, ref
        for ini, fim in tarefas:
            if fim <= ref:
                continue
            if ini - anterior >= OCIOSO_SELETOR_US:
                ti = ini
                break
            anterior = max(anterior, fim)
        if ti is None:
            raise ValueError("fechamento do seletor de arquivos nao identificado")
    elif operacao in ("rotulo", "exportar"):
        tipos = {"keydown"} if operacao == "rotulo" else CLIQUE
        alvo = [ts for ts, t in despachos if t in tipos]
        if not alvo:
            raise ValueError("evento de inicio nao encontrado")
        ti = tarefa_que_contem(tarefas, alvo[-1])
    else:
        raise ValueError(f"operacao desconhecida: {operacao}")

    tf = fim_da_sequencia(tarefas, ti)
    heap = sorted((e["ts"], e["args"]["data"]["jsHeapSizeUsed"])
                  for e in eventos if e.get("name") == "UpdateCounters" and e.get("pid") == pid)
    heap_mib = ""
    if operacao == "abrir":
        alvo_ts = tf + HEAP_APOS_US
        if t_max < alvo_ts:
            obs.append("gravacao terminou antes de tf + 2 s")
        amostras = [v for ts, v in heap if ts <= alvo_ts]
        heap_mib = round(amostras[-1] / 2**20, 2) if amostras else ""
    elif operacao == "exportar":
        amostras = [v for ts, v in heap if ti <= ts <= tf]
        heap_mib = round(max(amostras) / 2**20, 2) if amostras else ""

    return {
        "data": data_local(dados.get("metadata", {}).get("startTime", "")),
        "tentativa": tentativa, "porte": porte, "operacao": operacao, "formato": formato,
        "versao_chrome": versao_chrome, "tempo_ms": round((tf - ti) / 1000, 1),
        "heap_mib": heap_mib, "trace": caminho.name,
        "ti_ms": round((ti - t0) / 1000, 1), "tf_ms": round((tf - t0) / 1000, 1),
        "observacao": "; ".join(obs),
    }


def data_local(inicio: str) -> str:
    if not inicio:
        return ""
    return datetime.fromisoformat(inicio.replace("Z", "+00:00")).astimezone(FUSO).strftime("%Y-%m-%d")


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    pasta, saida = Path(sys.argv[1]), Path(sys.argv[2])
    versao = sys.argv[3] if len(sys.argv) > 3 else VERSAO_CHROME_PADRAO
    anteriores = {}
    if saida.exists():
        with saida.open(newline="", encoding="utf-8") as f:
            anteriores = {linha["trace"]: linha for linha in csv.DictReader(f)}
    linhas = []
    for caminho in sorted(list(pasta.glob("*.json.gz")) + list(pasta.glob("*.json"))):
        antiga = anteriores.get(caminho.name, {})
        try:
            linha = medir(caminho, versao)
            linha["resultado"] = antiga.get("resultado") or "sucesso"
        except Exception as erro:
            linha = {"trace": caminho.name, "resultado": antiga.get("resultado") or "verificar",
                     "observacao": f"erro na leitura: {erro}"}
        for col in MANUAIS:
            if antiga.get(col):
                linha[col] = antiga[col]
        linhas.append(linha)
        print(f"{caminho.name:<40} {str(linha.get('tempo_ms', '')):>10} ms "
              f"{str(linha.get('heap_mib', '')):>8} MiB  {linha.get('observacao', '')}")
    with saida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(linhas)
    print(f"\n{len(linhas)} gravacoes em {saida}")


if __name__ == "__main__":
    main()
