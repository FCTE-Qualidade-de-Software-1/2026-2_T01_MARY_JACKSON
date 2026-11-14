"""Dashboard do PSM: evolução do projeto inteiro, com gráficos dinâmicos (Chart.js).

Marcador usado na página Markdown:
- [[DASHBOARD_PSM]]: cartões por entrega e os dados dos gráficos.

Os cálculos e as regras vêm do hooks/horas.py (horas combinadas, issues não planejadas,
faixa do tempo de ciclo, entregas do mkdocs.yml); este arquivo só organiza os dados para os
gráficos. Os gráficos são desenhados por docs/javascripts/dashboard-psm.js.
"""

import html
import importlib.util
import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path

MARCADOR = "[[DASHBOARD_PSM]]"

_spec = importlib.util.spec_from_file_location("horas_psm", Path(__file__).with_name("horas.py"))
horas = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(horas)


def _curto(nome):
    return horas._rotulo(nome).strip('"')


def _situacao(dias, media, faixa):
    if not media:
        return "dentro"
    desvio = (dias - media) / media * 100
    if desvio > faixa:
        return "acima"
    if desvio < -faixa:
        return "abaixo"
    return "dentro"


def _montar(config):
    dados = horas._dados(config)
    if dados is None:
        return None
    extra = config.get("extra", {}) or {}
    limites = extra.get("psm", {}) or {}
    faixa = float(limites.get("faixa_ciclo", 10))
    custo_hora = float(extra.get("custo_hora", 0))
    entregas = horas._entregas(config)

    hoje = datetime.now(timezone.utc).astimezone(horas.BRASILIA).date()
    sprints, issues_ciclo = [], []
    for nome, lista in dados["sprints"].items():
        est = [horas._estimativa(i.get("body")) for i in lista]
        h_est = sum(e for e in est if e is not None)
        h_real = dados["horas_sprint"].get(nome, 0)
        concluidas = sum(1 for i in lista if horas._concluida(i))
        pares = [(i, horas._dias_ciclo(i)) for i in lista]
        pares = [(i, d) for i, d in pares if d is not None]
        dias = [d for _, d in pares]
        media = statistics.mean(dias) if dias else None
        due = (lista[0].get("milestone") or {}).get("due_on")
        prazo = datetime.strptime(due[:10], "%Y-%m-%d").date() if due else None
        sprints.append({
            "nome": nome, "rotulo": _curto(nome), "entrega": horas._entrega_de(lista[0], entregas),
            "planejadas": len(lista), "concluidas": concluidas,
            "canceladas": sum(1 for i in lista if horas._cancelada(i)),
            "pct": round(concluidas / len(lista) * 100, 1),
            "h_est": round(h_est, 2), "h_real": round(h_real, 2),
            "razao": round(h_real / h_est, 2) if h_est else None,
            "custo": round(h_real * custo_hora, 2),
            "media": round(media, 2) if media is not None else None,
            "mediana": round(statistics.median(dias), 2) if dias else None,
            "prazo": prazo.strftime("%d/%m") if prazo else None,
            "andamento": bool(prazo and hoje <= prazo),
        })
        for i, d in sorted(pares, key=lambda p: p[0]["number"]):
            titulo = re.sub(r"^\s*\[[^\]]*\]\s*", "", i.get("title") or "")
            issues_ciclo.append({"numero": i["number"], "sprint": _curto(nome), "dias": round(d, 2),
                                 "titulo": titulo, "entrega": horas._entrega_de(i, entregas),
                                 "situacao": _situacao(d, media, faixa)})

    resumo = horas._resumo_entregas(dados, config)
    fins = {e["nome"]: e["fim"] for e in entregas}
    entregas_json = []
    for nome, r in resumo.items():
        if not r["planejadas"]:
            continue
        entregas_json.append({
            "nome": nome, "fim": fins.get(nome), "base": r["base"], "real": round(r["real"], 2),
            "custo_base": round(r["custo_base"], 2), "custo_real": round(r["custo_real"], 2),
            "planejadas": r["planejadas"], "concluidas": r["concluidas"], "canceladas": r["canceladas"],
            "media": round(statistics.mean(r["dias"]), 2) if r["dias"] else None,
            "mediana": round(statistics.median(r["dias"]), 2) if r["dias"] else None,
        })

    agora = datetime.now(timezone.utc).astimezone(horas.BRASILIA)
    return {
        "atualizado": agora.strftime("%d/%m/%Y %H:%M"),
        "custo_hora": custo_hora,
        "limites": {"concluido": float(limites.get("concluido_minimo", 50)),
                    "razao": float(limites.get("razao_maxima", 1.5)), "faixa": faixa},
        "sprints": sprints, "issues": issues_ciclo, "entregas": entregas_json,
        "repo": dados["repo_url"],
    }


def _num(v, casas=1):
    return horas._fmt(v, casas)


def _esc(texto):
    return html.escape(str(texto))


def _data_curta(iso):
    return f"{iso[8:10]}/{iso[5:7]}" if iso and len(iso) == 10 and not iso.startswith("9999") else ""


def _foco(dados):
    """Entrega em foco: a mais recente com linha de base e issues; sem nenhuma, a mais recente com issues."""
    com_base = [e for e in dados["entregas"] if e["base"] and e["planejadas"]]
    return (com_base or dados["entregas"] or [None])[-1]


def _cartao(rotulo, numero, detalhe="", estado="", destaque=""):
    classe = f" mj-pa-cartao--{estado}" if estado else ""
    extra = f' <b class="mj-pa-dif">{_esc(destaque)}</b>' if destaque else ""
    return (f'<div class="mj-pa-cartao{classe}"><span class="mj-pa-rot">{_esc(rotulo)}</span>'
            f'<strong class="mj-pa-num">{_esc(numero)}</strong>'
            f'<span class="mj-pa-det">{_esc(detalhe)}{extra}</span></div>')


def _faixa_numeros(e, limites):
    """Linha de cartões de uma entrega: horas, custo, issues e tempo de ciclo."""
    fim = _data_curta(e.get("fim"))
    titulo = f"{e['nome']} · até {fim}" if fim else e["nome"]
    if e["base"]:
        dif = (e["real"] - e["base"]) / e["base"] * 100
        estado = "ruim" if dif > 0 else "bom"
        destaque = f"{'+' if dif > 0 else ''}{_num(dif, 0)}%"
        cartoes = [_cartao("Horas reais", f"{_num(e['real'])} h", f"previsto {_num(e['base'])} h ·", estado, destaque),
                   _cartao("Custo real", horas._fmt_r(e["custo_real"]),
                           f"previsto {horas._fmt_r(e['custo_base'])} ·", estado, destaque)]
    else:
        cartoes = [_cartao("Horas reais", f"{_num(e['real'])} h", "previsto: a definir"),
                   _cartao("Custo real", horas._fmt_r(e["custo_real"]), "previsto: a definir")]
    pct = e["concluidas"] / e["planejadas"] * 100 if e["planejadas"] else 0
    det = f"{e['concluidas']} de {e['planejadas']}"
    if e["canceladas"]:
        det += f"; {e['canceladas']} não planejada(s)"
    cartoes.append(_cartao("Issues concluídas", f"{_num(pct, 0)}%", det,
                           "bom" if pct >= limites["concluido"] else "ruim"))
    if e["media"] is not None:
        cartoes.append(_cartao("Tempo de ciclo", f"{_num(e['media'])} dias", f"média; mediana {_num(e['mediana'])}"))
    else:
        cartoes.append(_cartao("Tempo de ciclo", "—", "sem issues concluídas"))
    return (f'<div class="mj-pa-linha"><div class="mj-pa-entrega">{_esc(titulo)}</div>'
            f'<div class="mj-pa-cartoes">{"".join(cartoes)}</div></div>')


def _ponte(dados, foco):
    """Da linha de base às horas reais da entrega em foco, passo a passo."""
    if not foco or not foco["base"]:
        return []
    sprints = [s for s in dados["sprints"] if s["entrega"] == foco["nome"]]
    com_sprint = [s for s in sprints if s["nome"] != "Sem sprint"]
    soma_est = sum(s["h_est"] for s in com_sprint)
    passos = [{"rotulo": "Previsto", "valor": foco["base"], "tipo": "base"}]
    ajuste = soma_est - foco["base"]
    if abs(ajuste) >= 0.05:
        passos.append({"rotulo": "Estimativas", "valor": round(ajuste, 2), "tipo": "variacao"})
    for s in com_sprint:
        passos.append({"rotulo": s["rotulo"], "valor": round(s["h_real"] - s["h_est"], 2), "tipo": "variacao"})
    sem = sum(s["h_real"] for s in sprints if s["nome"] == "Sem sprint")
    if sem >= 0.05:
        passos.append({"rotulo": "Sem sprint", "valor": round(sem, 2), "tipo": "variacao"})
    passos.append({"rotulo": "Real", "valor": round(foco["real"], 2), "tipo": "total"})
    return passos


def _frases(dados, foco):
    """Uma frase por categoria do PSM, calculada a partir dos dados da entrega em foco."""
    if not foco:
        return []
    lim = dados["limites"]
    sprints = [s for s in dados["sprints"] if s["entrega"] == foco["nome"] and s["nome"] != "Sem sprint"]
    frases = []

    pct = foco["concluidas"] / foco["planejadas"] * 100 if foco["planejadas"] else 0
    txt = f"{foco['nome']}: {foco['concluidas']} de {foco['planejadas']} issues concluídas ({_num(pct, 0)}%)."
    abaixo = [s for s in sprints if not s["andamento"] and s["pct"] < lim["concluido"]]
    if abaixo:
        txt += " Abaixo do limite de " + f"{_num(lim['concluido'], 0)}%: " + \
               ", ".join(f"{s['rotulo']} ({_num(s['pct'], 0)}%)" for s in abaixo) + "."
    frases.append(("Calendário e Progresso", txt))

    if foco["base"]:
        dif = (foco["real"] - foco["base"]) / foco["base"] * 100
        txt = (f"{foco['nome']} usou {_num(foco['real'])} h, {_num(abs(dif), 0)}% "
               f"{'acima' if dif > 0 else 'abaixo'} do previsto ({horas._fmt_r(foco['custo_real'])}).")
        maior = max(sprints, key=lambda s: s["h_real"] - s["h_est"], default=None)
        if maior and maior["h_real"] > maior["h_est"]:
            txt += f" Maior diferença entre estimado e real: {maior['rotulo']} (+{_num(maior['h_real'] - maior['h_est'])} h)."
    else:
        txt = f"{foco['nome']}: {_num(foco['real'])} h registradas; linha de base a definir."
    frases.append(("Recursos e Custos", txt))

    issues = [i for i in dados["issues"] if i["entrega"] == foco["nome"]]
    if foco["media"] is not None:
        fora = sum(1 for i in issues if i["situacao"] == "acima")
        txt = (f"Tempo de ciclo médio de {_num(foco['media'])} dias, mediana de {_num(foco['mediana'])}. "
               f"{fora} issue(s) mais de {_num(lim['faixa'], 0)}% acima da média da sua sprint.")
    else:
        txt = "Nenhuma issue concluída ainda."
    frases.append(("Desempenho dos Processos", txt))
    return frases


def _grafico(id_, titulo, subtitulo, legenda, classe=""):
    return (f'<figure class="mj-pa-grafico {classe}"><figcaption>'
            f'<span class="mj-pa-gtitulo">{_esc(titulo)}</span>'
            f'<span class="mj-pa-gsub">{_esc(subtitulo)}</span></figcaption>'
            f'<div class="mj-pa-canvas"><canvas id="{id_}" role="img" aria-label="{_esc(titulo)}"></canvas></div>'
            f'<p class="mj-pa-legenda">{_esc(legenda)}</p></figure>')


def _dashboard(markdown, config):
    dados = _montar(config)
    if dados is None:
        return markdown.replace(MARCADOR, "_Dashboard indisponível nesta publicação (API do GitHub)._")
    lim, data = dados["limites"], dados["atualizado"].split(" ")[0]
    foco = _foco(dados)
    dados["foco"] = foco["nome"] if foco else None
    dados["ponte"] = _ponte(dados, foco)
    fonte = f"Fonte: issues, milestones e registro de horas do GitHub, em {data}."
    nome_foco = foco["nome"] if foco else ""

    topo = ('<div class="mj-pa-topo"><div><p class="mj-pa-titulo">Visão geral do projeto</p>'
            '<p class="mj-pa-sub">Medidas do PSM por entrega e por sprint</p></div>'
            f'<p class="mj-pa-atualizado">Atualizado em {_esc(dados["atualizado"])}</p></div>')
    numeros = "".join(_faixa_numeros(e, lim) for e in dados["entregas"])

    graficos = "".join([
        _grafico("psm-horas", "Estimado vs. real por sprint", "Horas de cada sprint",
                 "Figura 1. Barras: horas reais. Linha: horas estimadas nas issues. "
                 "A razão e o custo aparecem ao passar o mouse."),
        _grafico("psm-ponte", f"Por que a {nome_foco} passou do previsto" if dados["ponte"] else "Da linha de base às horas reais",
                 "Da linha de base às horas reais, em horas",
                 "Figura 2. Previsto: linha de base do planejamento. Estimativas: diferença entre a soma das estimativas das issues e a linha de base. Laranja: horas a mais; azul-claro: horas a menos."),
        _grafico("psm-progresso", "Issues concluídas por sprint", f"Percentual do planejado; tracejado: limite de {_num(lim['concluido'], 0)}%",
                 "Figura 3. Azul-claro: sprint em andamento."),
        _grafico("psm-ranking", "Issues que mais demoraram", f"{nome_foco}: as 10 de maior tempo de ciclo, em dias",
                 f"Figura 4. Laranja: mais de {_num(lim['faixa'], 0)}% acima da média da sprint (PSM/CID Parte 2, p. 26)."),
    ])

    frases = "".join(f'<div class="mj-pa-frase"><strong>{_esc(t)}</strong><span>{_esc(x)}</span></div>'
                     for t, x in _frases(dados, foco))

    corpo = (f'<div class="mj-pa">{topo}<div class="mj-pa-numeros">{numeros}</div>'
             f'<div class="mj-pa-graficos">{graficos}</div>'
             f'<div class="mj-pa-frases">{frases}</div>'
             f'<p class="mj-pa-fonte">{_esc(fonte)} Regras de cálculo no Plano de medição.</p></div>')
    saida = [corpo, "",
             f'<script type="application/json" id="psm-dados">{json.dumps(dados, ensure_ascii=False)}</script>', ""]
    return markdown.replace(MARCADOR, "\n".join(saida))


def on_page_markdown(markdown, page, config, files):
    if MARCADOR in markdown:
        markdown = _dashboard(markdown, config)
    return markdown