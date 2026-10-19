"""Monta as tabelas de horas e custos da página de gestão a partir de dados/gestao/horas.csv.

Na página Markdown, escreva [[TABELA_HORAS]] onde as tabelas devem aparecer.
O custo da hora vem de extra.custo_hora no mkdocs.yml.
"""

import csv
from collections import OrderedDict
from pathlib import Path

MARCADOR = "[[TABELA_HORAS]]"


def _num(texto):
    return float(str(texto).strip().replace(",", ".") or 0)


def _fmt_h(valor):
    return f"{valor:.1f}".replace(".", ",") + " h"


def _fmt_r(valor):
    inteiro, dec = f"{valor:,.2f}".split(".")
    return "R$ " + inteiro.replace(",", ".") + "," + dec


def on_page_markdown(markdown, page, config, files):
    if MARCADOR not in markdown:
        return markdown

    raiz = Path(config["config_file_path"]).parent
    arquivo = raiz / "dados" / "gestao" / "horas.csv"
    custo_hora = float(config.get("extra", {}).get("custo_hora", 0))

    if not arquivo.exists():
        return markdown.replace(MARCADOR, "_Arquivo dados/gestao/horas.csv não encontrado._")

    with arquivo.open(encoding="utf-8") as f:
        linhas = [l for l in csv.DictReader(f) if (l.get("membro") or "").strip()]

    por_membro = OrderedDict()
    for l in linhas:
        nome = l["membro"].strip()
        por_membro[nome] = por_membro.get(nome, 0) + _num(l["horas"])
    total = sum(por_membro.values())

    saida = ["## Horas e custo por integrante", "",
             "| Integrante | Horas | % do total | Custo |", "|---|---|---|---|"]
    for nome, h in sorted(por_membro.items(), key=lambda x: -x[1]):
        pct = (h / total * 100) if total else 0
        saida.append(f"| {nome} | {_fmt_h(h)} | {pct:.0f}% | {_fmt_r(h * custo_hora)} |")
    saida.append(f"| **Total** | **{_fmt_h(total)}** | **100%** | **{_fmt_r(total * custo_hora)}** |")
    saida += ["", f"Custo da hora usado: {_fmt_r(custo_hora)}.", "",
              "## Registro de horas", "",
              "| Data | Integrante | Atividade | Issue | Horas |", "|---|---|---|---|---|"]
    for l in linhas:
        saida.append(f"| {l.get('data','')} | {l['membro']} | {l.get('atividade','')} | "
                     f"{l.get('issue','')} | {_fmt_h(_num(l['horas']))} |")

    return markdown.replace(MARCADOR, "\n".join(saida))