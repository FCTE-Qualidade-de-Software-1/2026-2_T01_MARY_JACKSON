"""Monta as tabelas de horas e custos da página de gestão a partir de dados/gestao/horas.csv.

Na página Markdown, escreva [[TABELA_HORAS]] onde as tabelas devem aparecer.
O custo da hora vem de extra.custo_hora e as horas estimadas da E1 de extra.horas_estimadas,
ambos no mkdocs.yml.
"""

import csv
from collections import OrderedDict
from pathlib import Path

MARCADOR = "[[TABELA_HORAS]]"


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


def on_page_markdown(markdown, page, config, files):
    if MARCADOR not in markdown:
        return markdown

    raiz = Path(config["config_file_path"]).parent
    arquivo = raiz / "dados" / "gestao" / "horas.csv"
    extra = config.get("extra", {}) or {}
    custo_hora = float(extra.get("custo_hora", 0))
    horas_estimadas = float(extra.get("horas_estimadas", 0))
    repo_url = config.get("repo_url") or ""

    if not arquivo.exists():
        return markdown.replace(MARCADOR, "_Arquivo dados/gestao/horas.csv não encontrado._")

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

    return markdown.replace(MARCADOR, "\n".join(saida))