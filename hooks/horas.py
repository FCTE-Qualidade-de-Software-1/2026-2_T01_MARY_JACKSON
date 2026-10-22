"""Gera as páginas de gestão do projeto (métricas do PSM/CID) na GitPage.

Marcadores que podem ser usados nas páginas Markdown:
- [[TABELA_HORAS]]: tabelas de horas e custos a partir de dados/gestao/horas.csv.
- [[PAINEL_PSM]]: painel com as métricas do PSM (planejado vs. concluído, estimado vs.
  realizado e tempo de ciclo), com tabelas e gráficos, lido das issues do GitHub a cada
  publicação do site: milestone (sprint), datas de abertura e fechamento e os campos
  "Estimativa (horas)" e "Horas reais" do formulário de tarefa.

No mkdocs.yml: extra.custo_hora, extra.horas_estimadas e os limites de decisão em extra.psm.
"""


import csv
import json
import os
import re
import statistics
import urllib.request
from datetime import datetime, timezone
from collections import OrderedDict
from pathlib import Path

MARCADOR_HORAS = "[[TABELA_HORAS]]"
API = "https://api.github.com/repos/{repo}/issues?state=all&per_page=100&page={page}"


def _num(texto):
    return float(str(texto).strip().replace(",", ".") or 0)


def _fmt_h(valor):
    return f"{valor:.2f}".rstrip("0").rstrip(".").replace(".", ",") + " h"


def _fmt_r(valor):
    inteiro, dec = f"{valor:,.2f}".split(".")
    return "R$ " + inteiro.replace(",", ".") + "," + dec


def _fmt_data(iso):
    partes = str(iso).strip().split("-")
    return f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else iso


def _link_issue(texto, repo_url):
    numero = str(texto).strip().lstrip("#")
    if not numero.isdigit():
        return str(texto).strip()
    return f"[#{numero}]({repo_url.rstrip('/')}/issues/{numero})" if repo_url else f"#{numero}"


def _tabela_horas(markdown, config):

    raiz = Path(config["config_file_path"]).parent
    arquivo = raiz / "dados" / "gestao" / "horas.csv"
    extra = config.get("extra", {}) or {}
    custo_hora = float(extra.get("custo_hora", 0))
    horas_estimadas = float(extra.get("horas_estimadas", 0))
    repo_url = config.get("repo_url") or ""

    if not arquivo.exists():
        return markdown.replace(MARCADOR_HORAS, "_Arquivo dados/gestao/horas.csv não encontrado._")

    linhas, invalidas = [], []
    with arquivo.open(encoding="utf-8") as f:
        for n, l in enumerate(csv.DictReader(f), start=2):
            if not (l.get("membro") or "").strip():
                continue
            try:
                if None in l:  # vírgula a mais na atividade gera colunas extras
                    raise ValueError
                _num(l["horas"])
                linhas.append(l)
            except (ValueError, TypeError):
                invalidas.append(n)
    linhas.sort(key=lambda l: (l.get("data") or "").strip())

    por_membro = OrderedDict()
    for l in linhas:
        nome = l["membro"].strip()
        por_membro[nome] = por_membro.get(nome, 0) + _num(l["horas"])
    total = sum(por_membro.values())

    saida = []
    if horas_estimadas:
        pct_gasto = total / horas_estimadas * 100
        saida += ["## Estimado vs. realizado (E1)", "",
                  "| | Horas | Custo |", "|---|---|---|",
                  f"| Estimado (linha de base) | {_fmt_h(horas_estimadas)} | {_fmt_r(horas_estimadas * custo_hora)} |",
                  f"| Realizado até agora | {_fmt_h(total)} | {_fmt_r(total * custo_hora)} |",
                  "", f"Realizado até agora: {pct_gasto:.0f}% das horas estimadas para a E1.", ""]

    saida += ["## Horas e custo por integrante", "",
              "| Integrante | Horas | % do total | Custo |", "|---|---|---|---|"]
    for nome, h in sorted(por_membro.items(), key=lambda x: -x[1]):
        pct = (h / total * 100) if total else 0
        saida.append(f"| {nome} | {_fmt_h(h)} | {pct:.0f}% | {_fmt_r(h * custo_hora)} |")
    saida.append(f"| **Total** | **{_fmt_h(total)}** | **100%** | **{_fmt_r(total * custo_hora)}** |")
    saida += ["", f"Custo da hora usado: {_fmt_r(custo_hora)}.", "",
              "## Registro de horas", "",
              "| Data | Integrante | Atividade | Issue | Horas |", "|---|---|---|---|---|"]
    for l in linhas:
        saida.append(f"| {_fmt_data(l.get('data', ''))} | {l['membro'].strip()} | {l.get('atividade', '')} | "
                     f"{_link_issue(l.get('issue', ''), repo_url)} | {_fmt_h(_num(l['horas']))} |")

    if invalidas:
        saida += ["", "Linhas ignoradas por erro de formato em `dados/gestao/horas.csv` "
                  "(vírgula na atividade ou horas inválidas): " + ", ".join(map(str, invalidas)) + "."]

    return markdown.replace(MARCADOR_HORAS, "\n".join(saida))


# ---------- Painel do PSM (issues do GitHub) ----------

MARCADOR_PSM = "[[PAINEL_PSM]]"


def _baixar_issues(repo):
    """Lê as issues pela API. Para testes locais, aceita um arquivo em PSM_ISSUES_JSON."""
    arquivo = os.environ.get("PSM_ISSUES_JSON")
    if arquivo:
        with open(arquivo, encoding="utf-8") as f:
            return json.load(f)
    token = os.environ.get("GITHUB_TOKEN")
    issues, page = [], 1
    while True:
        req = urllib.request.Request(API.format(repo=repo, page=page))
        req.add_header("Accept", "application/vnd.github+json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            lote = json.load(resp)
        issues += lote
        if len(lote) < 100:
            return issues
        page += 1


def _campo(corpo, rotulo):
    """Valor de um campo do formulário de issue (texto abaixo de '### rótulo')."""
    m = re.search(r"###\s*" + re.escape(rotulo) + r"\s*\n(.*?)(?=\n###\s|\Z)", corpo or "", re.S)
    if not m:
        return ""
    valor = m.group(1).strip()
    return "" if valor == "_No response_" else valor


def _estimativa(corpo):
    """Número de horas estimadas; None se o campo não for um número único."""
    valor = _campo(corpo, "Estimativa (horas)").replace(",", ".").lower().replace("h", "").strip()
    try:
        return float(valor)
    except ValueError:
        return None


def _horas_reais(corpo):
    """Soma das horas no campo 'Horas reais' (linhas como '20/10 - Yasmin - 2 h')."""
    texto = _campo(corpo, "Horas reais")
    return sum(float(x.replace(",", ".")) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*h\b", texto))


def _horas_por_pessoa(corpo):
    """Horas de cada pessoa no campo 'Horas reais' (linhas 'dd/mm - Nome - X h')."""
    resultado = {}
    for linha in _campo(corpo, "Horas reais").splitlines():
        m = re.match(r"\s*[-*]?\s*\d{1,2}/\d{1,2}\s*[-–]\s*(.+?)\s*[-–]\s*(\d+(?:[.,]\d+)?)\s*h\b", linha)
        if m:
            nome = m.group(1).strip()
            resultado[nome] = resultado.get(nome, 0) + float(m.group(2).replace(",", "."))
    return resultado


def _rotulo(nome):
    """Nome curto da sprint para o eixo do gráfico ("Sprint 1 - Fase 1" vira "Sprint 1")."""
    curto = re.split(r"\s+[-–]\s+", nome)[0]
    return '"' + curto.replace('"', "'") + '"'


def _grafico(titulo, rotulos, barras, eixo_y, linha=None, maximo=None):
    """Gráfico de barras (e linha opcional) em Mermaid, desenhado pelo próprio tema do site."""
    numeros = lambda valores: "[" + ", ".join(f"{v:.1f}" for v in valores) + "]"
    if maximo is None:
        maximo = max(list(barras) + list(linha or []) + [1]) * 1.15
    partes = ["```mermaid", "xychart-beta", f'    title "{titulo}"',
              f"    x-axis [{', '.join(rotulos)}]",
              f'    y-axis "{eixo_y}" 0 --> {maximo:.0f}',
              f"    bar {numeros(barras)}"]
    if linha is not None:
        partes.append(f"    line {numeros(linha)}")
    partes += ["```", ""]
    return partes


def _data(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def _fmt(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


def _painel_psm(markdown, config):

    extra = config.get("extra", {}) or {}
    limites = extra.get("psm", {}) or {}
    lim_concluido = float(limites.get("concluido_minimo", 50))
    lim_razao = float(limites.get("razao_maxima", 1.5))
    lim_dias = float(limites.get("dias_parada", 3))
    custo_hora = float(extra.get("custo_hora", 0))

    repo_url = (config.get("repo_url") or "").rstrip("/")
    repo = "/".join(repo_url.split("/")[-2:])
    try:
        bruto = _baixar_issues(repo)
    except Exception as erro:  # sem rede ou API indisponível: o site continua sendo gerado
        return markdown.replace(MARCADOR_PSM, f"_Painel indisponível nesta publicação ({erro.__class__.__name__})._")

    issues = [i for i in bruto if "pull_request" not in i]
    agora = datetime.now(timezone.utc)

    sprints = OrderedDict()
    for i in sorted(issues, key=lambda x: ((x.get("milestone") or {}).get("due_on") or "9999", x["number"])):
        nome = (i.get("milestone") or {}).get("title") or "Sem sprint"
        sprints.setdefault(nome, []).append(i)

    saida = [f"_Atualizado automaticamente em {agora.astimezone().strftime('%d/%m/%Y %H:%M')} "
             f"a partir de {len(issues)} issues._", ""]

    # Calendário e Progresso: planejado vs. concluído
    saida += ["## Planejado vs. concluído", "",
              "| Sprint | Planejadas | Concluídas | Concluído | Situação |", "|---|---|---|---|---|"]
    for nome, lista in sprints.items():
        feitas = sum(1 for i in lista if i["state"] == "closed")
        pct = feitas / len(lista) * 100
        alerta = "abaixo do limite" if pct < lim_concluido else "ok"
        saida.append(f"| {nome} | {len(lista)} | {feitas} | {_fmt(pct)}% | {alerta} |")
    saida += ["", f"Limite: menos de {_fmt(lim_concluido, 0)}% concluído na metade da sprint indica redistribuir tarefas.", ""]
    rotulos = [_rotulo(n) for n in sprints]
    pcts = [sum(1 for i in l if i["state"] == "closed") / len(l) * 100 for l in sprints.values()]
    saida += _grafico("Concluído por sprint (%); linha: limite", rotulos, pcts, "%",
                      [lim_concluido] * len(pcts), maximo=100)

    # Recursos e Custos: estimado vs. realizado
    saida += ["## Estimado vs. realizado", "",
              "| Sprint | Horas estimadas | Horas reais | Razão | Custo real | Issues sem estimativa numérica |",
              "|---|---|---|---|---|---|"]
    for nome, lista in sprints.items():
        est = [_estimativa(i.get("body")) for i in lista]
        h_est = sum(e for e in est if e is not None)
        h_real = sum(_horas_reais(i.get("body")) for i in lista)
        razao = (h_real / h_est) if h_est else 0
        sem = ", ".join(f"#{i['number']}" for i, e in zip(lista, est) if e is None) or "—"
        saida.append(f"| {nome} | {_fmt(h_est)} h | {_fmt(h_real)} h | {_fmt(razao, 2)} | "
                     f"R$ {_fmt(h_real * custo_hora, 2)} | {sem} |")
    saida += ["", f"Limite: razão acima de {_fmt(lim_razao)} indica revisar as estimativas. "
              "As horas reais vêm do campo \"Horas reais\" de cada issue.", ""]
    est_sprint = [sum(e for e in (_estimativa(i.get("body")) for i in l) if e is not None) for l in sprints.values()]
    real_sprint = [sum(_horas_reais(i.get("body")) for i in l) for l in sprints.values()]
    saida += _grafico("Horas por sprint: barras estimadas, linha reais", rotulos, est_sprint, "horas",
                      real_sprint)

    # Horas por pessoa (para a tabela de contribuição)
    pessoas = {}
    for i in issues:
        for nome, h in _horas_por_pessoa(i.get("body")).items():
            pessoas[nome] = pessoas.get(nome, 0) + h
    if pessoas:
        total = sum(pessoas.values())
        saida += ["### Horas por integrante", "", "| Integrante | Horas | % do total |", "|---|---|---|"]
        for nome, h in sorted(pessoas.items(), key=lambda x: -x[1]):
            saida.append(f"| {nome} | {_fmt(h)} h | {_fmt(h / total * 100, 0)}% |")
        saida.append("")

    # Desempenho dos Processos: tempo de ciclo
    saida += ["## Tempo de ciclo", "",
              "| Sprint | Issues concluídas | Média (dias) | Mediana (dias) |", "|---|---|---|---|"]
    for nome, lista in sprints.items():
        dias = [(_data(i["closed_at"]) - _data(i["created_at"])).total_seconds() / 86400
                for i in lista if i["state"] == "closed" and i.get("closed_at")]
        if dias:
            saida.append(f"| {nome} | {len(dias)} | {_fmt(statistics.mean(dias))} | {_fmt(statistics.median(dias))} |")
        else:
            saida.append(f"| {nome} | 0 | — | — |")
    medias = []
    for lista in sprints.values():
        d = [(_data(i["closed_at"]) - _data(i["created_at"])).total_seconds() / 86400
             for i in lista if i["state"] == "closed" and i.get("closed_at")]
        medias.append(statistics.mean(d) if d else 0)
    saida += [""] + _grafico("Tempo de ciclo médio por sprint (dias)", rotulos, medias, "dias")
    paradas = [i for i in issues if i["state"] == "open"
               and (agora - _data(i.get("updated_at") or i["created_at"])).total_seconds() / 86400 > lim_dias]
    saida += ["", f"Limite: issue sem atualização há mais de {_fmt(lim_dias, 0)} dias indica cobrar ou dividir a tarefa.", ""]
    if paradas:
        saida.append("Issues abertas acima do limite: " + ", ".join(
            f"[#{i['number']}]({repo_url}/issues/{i['number']})" for i in paradas) + ".")
    else:
        saida.append("Nenhuma issue aberta acima do limite.")

    return markdown.replace(MARCADOR_PSM, "\n".join(saida))


def on_page_markdown(markdown, page, config, files):
    if MARCADOR_HORAS in markdown:
        markdown = _tabela_horas(markdown, config)
    if MARCADOR_PSM in markdown:
        markdown = _painel_psm(markdown, config)
    return markdown