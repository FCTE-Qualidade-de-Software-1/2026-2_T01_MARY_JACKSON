"""Gera as páginas de gestão do projeto (métricas do PSM/CID) na GitPage.

Marcadores que podem ser usados nas páginas Markdown:
- [[TABELA_HORAS]]: horas e custos por entrega e por integrante (horas.csv + campo "Horas reais"
  das issues) e o registro de horas do horas.csv.
- [[PAINEL_PSM]]: painel com as métricas do PSM (planejado vs. concluído, estimado vs.
  realizado e tempo de ciclo), com tabelas e gráficos, lido das issues do GitHub a cada
  publicação do site: milestone (sprint), datas de abertura e fechamento e os campos
  "Estimativa (horas)" e "Horas reais" do formulário de tarefa.

O Dashboard do PSM (hooks/dashboard_psm.py) usa as funções deste arquivo.

No mkdocs.yml: extra.custo_hora, extra.entregas (linha de base de cada entrega) e os limites
de decisão em extra.psm. extra.horas_estimadas continua aceito quando extra.entregas não existe.

Issues fechadas como "não planejada" (Close as not planned) contam como planejadas, mas não
como concluídas, e ficam fora do tempo de ciclo.
"""


import csv
import json
import os
import re
import statistics
import unicodedata
import urllib.request
from datetime import date, datetime, timedelta, timezone
from collections import OrderedDict
from pathlib import Path
BRASILIA = timezone(timedelta(hours=-3))

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


def _ler_csv(config):
    """Linhas válidas e números das linhas ignoradas de dados/gestao/horas.csv.

    Uma linha é ignorada quando tem colunas a mais (vírgula na atividade ou nas horas, como "2,0")
    ou quando as horas não são um número.
    """
    arquivo = Path(config["config_file_path"]).parent / "dados" / "gestao" / "horas.csv"
    if not arquivo.exists():
        return None, []
    linhas, invalidas = [], []
    with arquivo.open(encoding="utf-8") as f:
        for n, l in enumerate(csv.DictReader(f), start=2):
            if not (l.get("membro") or "").strip():
                continue
            try:
                if None in l:  # vírgula a mais gera colunas extras
                    raise ValueError
                l["_horas"] = _num(l["horas"])
                linhas.append(l)
            except (ValueError, TypeError):
                invalidas.append(n)
    linhas.sort(key=lambda l: (l.get("data") or "").strip())
    return linhas, invalidas


def _aviso_csv(invalidas):
    if not invalidas:
        return []
    return ["!!! warning \"Linhas do horas.csv ignoradas\"",
            "    As linhas " + ", ".join(map(str, invalidas)) + " de `dados/gestao/horas.csv` não foram contadas "
            "por erro de formato (vírgula na atividade ou nas horas; use ponto decimal, como 2.0). "
            "Corrija o arquivo para que essas horas entrem nas medições.", ""]


def _tabela_horas(markdown, config):

    extra = config.get("extra", {}) or {}
    custo_hora = float(extra.get("custo_hora", 0))
    repo_url = config.get("repo_url") or ""

    linhas, invalidas = _ler_csv(config)
    if linhas is None:
        return markdown.replace(MARCADOR_HORAS, "_Arquivo dados/gestao/horas.csv não encontrado._")

    saida = _aviso_csv(invalidas)
    dados = _dados(config)
    if dados is None:
        saida += ["_As horas registradas nas issues não puderam ser lidas nesta publicação; "
                  "as tabelas abaixo mostram só o horas.csv._", ""]
        por_membro = OrderedDict()
        for l in linhas:
            por_membro[l["membro"].strip()] = por_membro.get(l["membro"].strip(), 0) + l["_horas"]
    else:
        saida += _tabela_entregas_horas(dados, config)
        por_membro = {n: v["csv"] + v["issues"] for n, v in dados["conferencia"].items()}

    total = sum(por_membro.values())
    saida += ["## Horas e custo por integrante", "",
              "Soma do horas.csv e do campo \"Horas reais\" das issues, sem contar a mesma hora duas vezes "
              "(regras na [conferência das horas do Painel do PSM](painel-psm.md#conferencia-das-horas)).", "",
              "| Integrante | Horas | % do total | Custo |", "|---|---|---|---|"]
    for nome, h in sorted(por_membro.items(), key=lambda x: -x[1]):
        pct = (h / total * 100) if total else 0
        saida.append(f"| {nome} | {_fmt_h(h)} | {pct:.0f}% | {_fmt_r(h * custo_hora)} |")
    saida.append(f"| **Total** | **{_fmt_h(total)}** | **100%** | **{_fmt_r(total * custo_hora)}** |")
    saida += ["", f"Custo da hora usado: {_fmt_r(custo_hora)}.", "",
              "## Registro de horas no horas.csv", "",
              "Registro oficial até 22/10 (Ata 04); depois, as horas passaram ao campo \"Horas reais\" das issues.", "",
              "| Data | Integrante | Atividade | Issue | Horas |", "|---|---|---|---|---|"]
    for l in linhas:
        saida.append(f"| {_fmt_data(l.get('data', ''))} | {l['membro'].strip()} | {l.get('atividade', '')} | "
                     f"{_link_issue(l.get('issue', ''), repo_url)} | {_fmt_h(l['_horas'])} |")

    return markdown.replace(MARCADOR_HORAS, "\n".join(saida))


# ---------- Painel do PSM (issues do GitHub) ----------

MARCADOR_PSM = "[[PAINEL_PSM]]"
_CACHE = {}


def _baixar_issues(repo):
    """Lê as issues pela API (uma vez por publicação). Para testes locais, aceita PSM_ISSUES_JSON."""
    if repo in _CACHE:
        return _CACHE[repo]
    arquivo = os.environ.get("PSM_ISSUES_JSON")
    if arquivo:
        with open(arquivo, encoding="utf-8") as f:
            _CACHE[repo] = json.load(f)
        return _CACHE[repo]
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
            _CACHE[repo] = issues
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
    return sum(float(x.replace(",", ".")) for x in re.findall(r"(\d+(?:[.,]\d+)?)\s*h\b", texto, re.I))


def _linhas_horas(corpo):
    """Linhas 'dd/mm - Nome - X h' do campo 'Horas reais', como ((mês, dia), nome, horas)."""
    resultado = []
    for linha in _campo(corpo, "Horas reais").splitlines():
        m = re.match(r"\s*[-*]?\s*(\d{1,2})/(\d{1,2})\s*[-–]\s*(.+?)\s*[-–]\s*(\d+(?:[.,]\d+)?)\s*h\b", linha, re.I)
        if m:
            resultado.append(((int(m.group(2)), int(m.group(1))), m.group(3).strip(),
                              float(m.group(4).replace(",", "."))))
    return resultado


def _rotulo(nome):
    """Nome curto da sprint para o eixo do gráfico ("Sprint 1 - Fase 1" vira "Sprint 1")."""
    curto = re.split(r"\s+[-–]\s+", nome)[0]
    return '"' + curto.replace('"', "'") + '"'


def _grafico(rotulos, barras, eixo_y, linha=None, maximo=None, legenda=""):
    """Gráfico de barras (e linha opcional) em Mermaid, seguido da legenda da figura.

    Barras em lilás e linha em azul; o tema não desenha legenda, por isso ela vai no texto da figura.
    """
    numeros = lambda valores: "[" + ", ".join(f"{v:.1f}" for v in valores) + "]"
    if maximo is None:
        maximo = max(list(barras) + list(linha or []) + [1]) * 1.15
    partes = ["```mermaid",
              '%%{init: {"themeVariables": {"xyChart": {"plotColorPalette": "#c5cae9, #3f51b5"}}}}%%',
              "xychart-beta",
              f"    x-axis [{', '.join(rotulos)}]",
              f'    y-axis "{eixo_y}" 0 --> {maximo:.0f}',
              f"    bar {numeros(barras)}"]
    if linha is not None:
        partes.append(f"    line {numeros(linha)}")
    partes += ["```", ""]
    if legenda:
        partes += [f"_{legenda}_", ""]
    return partes


def _data(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def _fmt(valor, casas=1):
    return f"{valor:.{casas}f}".replace(".", ",")


def _pessoa(nome):
    """Chave para comparar nomes: primeiro nome, minúsculo e sem acento ("Miquéias Ezequiel" vira "miqueias")."""
    primeiro = (nome or "").strip().split(" ")[0]
    sem_acento = unicodedata.normalize("NFKD", primeiro).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def _cancelada(issue):
    """Issue fechada como "não planejada" (replanejada ou descartada)."""
    return issue.get("state") == "closed" and issue.get("state_reason") == "not_planned"


def _concluida(issue):
    return issue.get("state") == "closed" and not _cancelada(issue)


def _dias_ciclo(issue):
    """Tempo de ciclo em dias; None se a issue não foi concluída."""
    if not _concluida(issue) or not issue.get("closed_at"):
        return None
    return (_data(issue["closed_at"]) - _data(issue["created_at"])).total_seconds() / 86400


def _horas_combinadas(issues, sprints, config, fim_csv=(10, 22)):
    """Junta as horas do horas.csv e do campo "Horas reais" das issues.

    - Linha do CSV com número de issue: entra na sprint (milestone) dessa issue.
    - Linha do CSV sem issue: entra na sprint pela data, comparada com o prazo de cada milestone.
    - Linha "dd/mm - Nome - X h" de uma issue: entra, exceto quando é de até 22/10 (período em que o
      CSV era o registro oficial) e a mesma pessoa já registrou a mesma issue no CSV; nesse caso vale o CSV.
      Linhas a partir de 23/10 sempre entram.

    Devolve as horas por sprint, a conferência por pessoa e a lista de linhas ignoradas.
    """
    por_numero = {i["number"]: i for i in issues}
    prazos = []
    for nome, lista in sprints.items():
        prazo = (lista[0].get("milestone") or {}).get("due_on")
        if prazo:
            prazos.append((prazo[:10], nome))
    prazos.sort()

    def sprint_da_data(data):
        for prazo, nome in prazos:
            if data <= prazo:
                return nome
        return prazos[-1][1] if prazos else "Sem sprint"

    por_sprint, nomes, conferencia, ignoradas = {}, {}, {}, []
    ja_no_csv = set()

    def pessoa(nome):
        chave = _pessoa(nome) or "sem nome"
        nomes.setdefault(chave, (nome or "Sem nome").strip().split(" ")[0])
        return conferencia.setdefault(chave, {"csv": 0.0, "issues": 0.0, "ignoradas": 0.0})

    for l in _ler_csv(config)[0] or []:
        texto = str(l.get("issue") or "").strip().lstrip("#")
        numero = int(texto) if texto.isdigit() else None
        issue = por_numero.get(numero) if numero else None
        sprint = ((issue or {}).get("milestone") or {}).get("title")
        if sprint is None:
            sprint = sprint_da_data(str(l.get("data") or "").strip())
        if numero:
            ja_no_csv.add((numero, _pessoa(l["membro"])))
        pessoa(l["membro"])["csv"] += l["_horas"]
        por_sprint[sprint] = por_sprint.get(sprint, 0) + l["_horas"]

    for i in issues:
        sprint = (i.get("milestone") or {}).get("title") or "Sem sprint"
        linhas = _linhas_horas(i.get("body"))
        for dia, nome, horas in linhas:
            repetida = (i["number"], _pessoa(nome)) in ja_no_csv and dia <= fim_csv
            if repetida:
                pessoa(nome)["ignoradas"] += horas
                ignoradas.append((i["number"], nomes[_pessoa(nome) or "sem nome"], horas))
            else:
                pessoa(nome)["issues"] += horas
                por_sprint[sprint] = por_sprint.get(sprint, 0) + horas
        sem_nome = _horas_reais(i.get("body")) - sum(h for _, _, h in linhas)
        if sem_nome > 0.001:
            pessoa("")["issues"] += sem_nome
            por_sprint[sprint] = por_sprint.get(sprint, 0) + sem_nome

    conferencia = {nomes[k]: v for k, v in conferencia.items()}
    return por_sprint, conferencia, ignoradas


def _entregas(config):
    """Entregas do mkdocs.yml (extra.entregas), ordenadas pela data de fim.

    Cada entrega: nome, fim (AAAA-MM-DD) e horas_estimadas (linha de base). Sem extra.entregas,
    usa uma entrega única com extra.horas_estimadas.
    """
    extra = config.get("extra", {}) or {}
    lista = []
    for e in extra.get("entregas") or []:
        lista.append({"nome": str(e.get("nome")), "fim": str(e.get("fim")),
                      "horas": float(e.get("horas_estimadas") or 0)})
    if not lista:
        lista = [{"nome": "Entrega", "fim": "9999-12-31", "horas": float(extra.get("horas_estimadas") or 0)}]
    return sorted(lista, key=lambda e: e["fim"])


def _entrega_de(issue, entregas):
    """Entrega da issue: pelo prazo da milestone ou, sem milestone, pela data de abertura."""
    ref = ((issue.get("milestone") or {}).get("due_on") or issue.get("created_at") or "")[:10]
    for e in entregas:
        if ref <= e["fim"]:
            return e["nome"]
    return entregas[-1]["nome"]


def _dados(config):
    """Issues, sprints e horas combinadas; None se a API não puder ser lida."""
    repo_url = (config.get("repo_url") or "").rstrip("/")
    repo = "/".join(repo_url.split("/")[-2:])
    try:
        bruto = _baixar_issues(repo)
    except Exception:  # sem rede ou API indisponível: o site continua sendo gerado
        return None
    issues = [i for i in bruto if "pull_request" not in i]
    sprints = OrderedDict()
    for i in sorted(issues, key=lambda x: ((x.get("milestone") or {}).get("due_on") or "9999", x["number"])):
        nome = (i.get("milestone") or {}).get("title") or "Sem sprint"
        sprints.setdefault(nome, []).append(i)
    horas_sprint, conferencia, ignoradas = _horas_combinadas(issues, sprints, config)
    return {"issues": issues, "sprints": sprints, "horas_sprint": horas_sprint,
            "conferencia": conferencia, "ignoradas": ignoradas, "repo_url": repo_url}


def _resumo_entregas(dados, config):
    """Totais de cada entrega nas três categorias de informação."""
    entregas = _entregas(config)
    custo_hora = float((config.get("extra", {}) or {}).get("custo_hora", 0))
    resumo = OrderedDict((e["nome"], {"base": e["horas"], "planejadas": 0, "concluidas": 0, "canceladas": 0,
                                      "est_issues": 0.0, "real": 0.0, "dias": []}) for e in entregas)
    for nome, lista in dados["sprints"].items():
        for i in lista:
            r = resumo[_entrega_de(i, entregas)]
            r["planejadas"] += 1
            r["concluidas"] += _concluida(i)
            r["canceladas"] += _cancelada(i)
            r["est_issues"] += _estimativa(i.get("body")) or 0
            d = _dias_ciclo(i)
            if d is not None:
                r["dias"].append(d)
        if lista:
            resumo[_entrega_de(lista[0], entregas)]["real"] += dados["horas_sprint"].get(nome, 0)
    for r in resumo.values():
        r["custo_base"] = r["base"] * custo_hora
        r["custo_real"] = r["real"] * custo_hora
    return resumo


def _tabela_entregas_horas(dados, config):
    """Tabela de horas e custo por entrega (linha de base vs. realizado)."""
    saida = ["## Estimado vs. realizado por entrega", "",
             "| Entrega | Linha de base | Custo previsto | Horas reais | Custo real | Real ÷ linha de base |",
             "|---|---|---|---|---|---|"]
    for nome, r in _resumo_entregas(dados, config).items():
        razao = _fmt(r["real"] / r["base"], 2) if r["base"] else "—"
        base = _fmt_h(r["base"]) if r["base"] else "a definir"
        saida.append(f"| {nome} | {base} | {_fmt_r(r['custo_base']) if r['base'] else '—'} | "
                     f"{_fmt_h(r['real'])} | {_fmt_r(r['custo_real'])} | {razao} |")
    saida += ["", "A linha de base é a soma das estimativas do planejamento de cada entrega (extra.entregas no "
              "mkdocs.yml). Os detalhes por sprint estão no [Painel do PSM](painel-psm.md).", ""]
    return saida


def _ficha(o_que_mede, formula, fonte, limite, referencia):
    """Lista curta que explica a métrica antes dos números."""
    return [f"- **O que mede:** {o_que_mede}",
            f"- **Como é calculada:** {formula}",
            f"- **De onde vêm os dados:** {fonte}",
            f"- **Quando exige decisão:** {limite}",
            f"- **Referência:** {referencia}", ""]


def _painel_psm(markdown, config):

    extra = config.get("extra", {}) or {}
    limites = extra.get("psm", {}) or {}
    lim_concluido = float(limites.get("concluido_minimo", 50))
    lim_razao = float(limites.get("razao_maxima", 1.5))
    lim_dias = float(limites.get("dias_parada", 3))
    lim_faixa = float(limites.get("faixa_ciclo", 10))
    custo_hora = float(extra.get("custo_hora", 0))

    dados = _dados(config)
    if dados is None:
        return markdown.replace(MARCADOR_PSM, "_Painel indisponível nesta publicação (API do GitHub)._")
    issues, sprints, horas_sprint = dados["issues"], dados["sprints"], dados["horas_sprint"]
    conferencia, ignoradas, repo_url = dados["conferencia"], dados["ignoradas"], dados["repo_url"]
    agora = datetime.now(timezone.utc)
    rotulos = [_rotulo(n) for n in sprints]
    link = lambda n: f"[#{n}]({repo_url}/issues/{n})"

    data_hoje = agora.astimezone(BRASILIA).strftime("%d/%m/%Y")
    saida = [f"_Atualizado automaticamente em {agora.astimezone(BRASILIA).strftime('%d/%m/%Y %H:%M')} (horário de Brasília), "
             f"a partir de {len(issues)} issues e do registro de horas._", ""]
    saida += _aviso_csv(_ler_csv(config)[1])

    # Como o painel é montado
    saida += ["## Como este painel é montado", "",
              "A cada publicação do site, o script `hooks/horas.py` lê as issues do GitHub e o registro de horas, "
              "calcula as três métricas do [Plano de medição](plano-de-medicao.md) e compara cada resultado com o limite "
              "de decisão. A interpretação e as decisões de cada medição ficam no [Registro de medições](registro-de-medicoes.md).",
              "",
              "```mermaid",
              "flowchart LR",
              '    I["Issues do GitHub"] --> S["Script horas.py"]',
              '    C["Registro de horas<br/>(horas.csv)"] --> S',
              '    S --> M1["Planejado vs. concluído"]',
              '    S --> M2["Estimado vs. realizado"]',
              '    S --> M3["Tempo de ciclo"]',
              '    M1 --> L["Comparação com os limites"]',
              "    M2 --> L",
              "    M3 --> L",
              '    L --> R["Registro de medições"]',
              "```", "",
              "_Figura 1. Fluxo de cálculo do painel. Fonte: elaboração da equipe._", ""]

    # 1. Calendário e Progresso
    saida += ["## 1. Planejado vs. concluído (Calendário e Progresso)", ""]
    saida += _ficha("Quanto do que a equipe planejou para a sprint já foi entregue.",
                    "Issues concluídas da sprint ÷ issues da sprint × 100. Issues fechadas como \"não planejada\" "
                    "contam como planejadas, mas não como concluídas.",
                    "Milestone (sprint), situação e motivo do fechamento de cada issue.",
                    f"Menos de {_fmt(lim_concluido, 0)}% concluído na metade da sprint: redistribuir tarefas.",
                    "PSM/CID, Parte 1, Tabela 5, linha 1; Parte 2, seção 8.3.")
    saida += ["| Sprint | Planejadas | Concluídas | Não planejadas | Concluído | Situação |", "|---|---|---|---|---|---|"]
    pcts, canceladas = [], []
    for nome, lista in sprints.items():
        feitas = sum(1 for i in lista if _concluida(i))
        canc = [i for i in lista if _cancelada(i)]
        canceladas += canc
        pct = feitas / len(lista) * 100
        pcts.append(pct)
        alerta = "abaixo do limite" if pct < lim_concluido else "dentro do limite"
        saida.append(f"| {nome} | {len(lista)} | {feitas} | {len(canc) or '—'} | {_fmt(pct)}% | {alerta} |")
    saida += [""]
    if canceladas:
        saida += ["Issues fechadas como \"não planejada\" (replanejadas ou descartadas): "
                  + ", ".join(link(i["number"]) for i in canceladas) + ".", ""]
    saida += _grafico(rotulos, pcts, "% concluído", [lim_concluido] * len(pcts), maximo=100,
                      legenda=f"Figura 2. Percentual de issues concluídas por sprint. Barras lilás: "
                              f"percentual concluído; linha azul: limite de decisão ({_fmt(lim_concluido, 0)}%). "
                              f"Fonte: issues e milestones do GitHub, em {data_hoje}.")

    # 2. Recursos e Custos
    saida += ["## 2. Estimado vs. realizado (Recursos e Custos)", ""]
    saida += _ficha("Se o esforço gasto está de acordo com o que foi estimado.",
                    f"Horas reais ÷ horas estimadas. Custo = horas reais × R$ {_fmt(custo_hora, 2)}.",
                    "Estimativa: campo \"Estimativa (horas)\" das issues. Horas reais: registro de horas e campo "
                    "\"Horas reais\" das issues (ver a conferência abaixo).",
                    f"Razão acima de {_fmt(lim_razao)}: revisar as estimativas das tarefas restantes.",
                    "PSM/CID, Parte 1, Tabela 5, linha 8.")
    saida += ["| Sprint | Horas estimadas | Horas reais | Razão | Custo real | Issues sem estimativa numérica |",
              "|---|---|---|---|---|---|"]
    est_sprint, real_sprint = [], []
    for nome, lista in sprints.items():
        est = [_estimativa(i.get("body")) for i in lista]
        h_est = sum(e for e in est if e is not None)
        h_real = horas_sprint.get(nome, 0)
        est_sprint.append(h_est)
        real_sprint.append(h_real)
        razao = (h_real / h_est) if h_est else 0
        sem = ", ".join(link(i["number"]) for i, e in zip(lista, est) if e is None) or "—"
        saida.append(f"| {nome} | {_fmt(h_est)} h | {_fmt(h_real)} h | {_fmt(razao, 2)} | "
                     f"{_fmt_r(h_real * custo_hora)} | {sem} |")
    t_est, t_real = sum(est_sprint), sum(real_sprint)
    saida.append(f"| **Total** | **{_fmt(t_est)} h** | **{_fmt(t_real)} h** | "
                 f"**{_fmt(t_real / t_est, 2) if t_est else '—'}** | **{_fmt_r(t_real * custo_hora)}** | |")
    saida += ["", "Issues sem estimativa numérica não entram na soma das horas estimadas; "
              "por isso, a razão dessas sprints pode estar acima do valor real.", ""]
    saida += _grafico(rotulos, est_sprint, "horas", real_sprint,
                      legenda=f"Figura 3. Horas estimadas e realizadas por sprint. Barras lilás: horas estimadas; "
                              f"linha azul: horas reais. Fonte: issues do GitHub e registro de horas, em {data_hoje}.")

    # Conferência das horas
    saida += ["### Conferência das horas", "",
              "As horas reais vêm de dois lugares: o registro de horas (`dados/gestao/horas.csv`), usado desde o início "
              "do projeto, e o campo \"Horas reais\" das issues, adotado a partir de 21/10 (Ata 04). As regras são:", "",
              "1. Linha do registro **com** número de issue: entra na sprint dessa issue.",
              "2. Linha do registro **sem** número de issue: entra na sprint pela data.",
              "3. Horas escritas na issue **até 22/10** (fim da Sprint 2, quando o registro de horas era o oficial): entram, "
              "**exceto** quando a mesma pessoa já registrou a mesma issue no registro de horas. Nesse caso vale o registro, "
              "para não contar o mesmo trabalho duas vezes.",
              "4. Horas escritas na issue **a partir de 23/10**: entram sempre.", "",
              "| Integrante | Registradas no horas.csv | Registradas nas issues | Repetidas (já estavam no horas.csv) | Total contado | % do total |",
              "|---|---|---|---|---|---|"]
    h = lambda v: f"{_fmt(v)} h" if v > 0.001 else "—"
    total = sum(v["csv"] + v["issues"] for v in conferencia.values())
    for nome, v in sorted(conferencia.items(), key=lambda x: -(x[1]["csv"] + x[1]["issues"])):
        contadas = v["csv"] + v["issues"]
        pct = contadas / total * 100 if total else 0
        saida.append(f"| {nome} | {h(v['csv'])} | {h(v['issues'] + v['ignoradas'])} | "
                     f"{h(v['ignoradas'])} | **{_fmt(contadas)} h** | {_fmt(pct, 0)}% |")
    saida.append(f"| **Total** | | | | **{_fmt(total)} h** | 100% |")
    saida += ["", "Como ler: **Total contado** = horas no horas.csv + horas nas issues − horas repetidas. "
              "Um traço (—) indica que a pessoa não registrou horas naquele lugar.", ""]
    if ignoradas:
        saida.append("**Horas repetidas, contadas uma vez só:** " + "; ".join(
            f"{link(n)} ({nome}, {_fmt(hh)} h)" for n, nome, hh in ignoradas) + ".")
    else:
        saida.append("**Horas repetidas:** nenhuma.")
    saida += ["", "A página [Horas e custos](horas.md) usa a mesma soma, por entrega e por integrante.", ""]

    # 3. Desempenho dos Processos
    saida += ["## 3. Tempo de ciclo (Desempenho dos Processos)", ""]
    saida += _ficha("Quanto tempo uma tarefa leva entre ser aberta e ser concluída.",
                    "Data de fechamento da issue − data de abertura, em dias, por issue; média e mediana por sprint. "
                    "Issues fechadas como \"não planejada\" ficam de fora.",
                    "Datas registradas pelo GitHub em cada issue.",
                    f"Guia: investigar as issues mais de {_fmt(lim_faixa, 0)}% acima ou abaixo da média da sprint. "
                    f"Equipe: issue aberta há mais de {_fmt(lim_dias, 0)} dia(s) sem atualização, contados a partir do "
                    "início da sprint: cobrar o responsável ou dividir a tarefa.",
                    "PSM/CID, Parte 1, Tabela 5, linha 32; Parte 2, seção 8.5, p. 26.")
    saida += ["| Sprint | Issues concluídas | Média (dias) | Mediana (dias) | Fora da faixa de ±"
              f"{_fmt(lim_faixa, 0)}% |", "|---|---|---|---|---|"]
    medias, por_issue = [], []
    for nome, lista in sprints.items():
        pares = [(i, _dias_ciclo(i)) for i in lista]
        pares = [(i, d) for i, d in pares if d is not None]
        dias = [d for _, d in pares]
        media = statistics.mean(dias) if dias else 0
        medias.append(media)
        fora = 0
        for i, d in pares:
            desvio = (d - media) / media * 100 if media else 0
            situacao = "dentro da faixa"
            if desvio > lim_faixa:
                situacao, fora = f"acima (+{_fmt(desvio, 0)}%)", fora + 1
            elif desvio < -lim_faixa:
                situacao, fora = f"abaixo ({_fmt(desvio, 0)}%)", fora + 1
            por_issue.append((nome, i["number"], d, situacao))
        if dias:
            saida.append(f"| {nome} | {len(dias)} | {_fmt(media)} | {_fmt(statistics.median(dias))} | {fora} |")
        else:
            saida.append(f"| {nome} | 0 | — | — | — |")
    saida += ["", "O tempo é contado até o **fechamento** da issue. Uma tarefa concluída e fechada depois aparece com "
              "tempo maior que o real; esses casos são explicados no Registro de medições.", ""]
    saida += _grafico(rotulos, medias, "dias",
                      legenda=f"Figura 4. Tempo de ciclo médio por sprint. Barras lilás: média de dias entre abrir e "
                              f"fechar a issue. Fonte: datas das issues no GitHub, em {data_hoje}.")
    saida += [f"??? info \"Tempo de ciclo de cada issue e comparação com a média da sprint (±{_fmt(lim_faixa, 0)}%)\"", "",
              "    | Sprint | Issue | Dias | Comparação com a média da sprint |", "    |---|---|---|---|"]
    for nome, numero, d, situacao in por_issue:
        saida.append(f"    | {nome} | {link(numero)} | {_fmt(d)} | {situacao} |")
    saida.append("")

    # Início de cada sprint: a data no começo da descrição da milestone ("07/11 a 16/11: ...");
    # sem ela, o dia seguinte ao prazo da sprint anterior. Uma issue criada antes da sprint
    # só começa a contar como parada a partir do início da sprint dela.
    prazos = sorted({(i.get("milestone") or {}).get("due_on") for i in issues
                     if (i.get("milestone") or {}).get("due_on")})

    def inicio_da_sprint(issue):
        marco = issue.get("milestone") or {}
        prazo = marco.get("due_on")
        m = re.match(r"\s*(\d{1,2})/(\d{1,2})", marco.get("description") or "")
        if m and prazo:
            ano = _data(prazo).year
            return datetime(ano, int(m.group(2)), int(m.group(1)), 3, tzinfo=timezone.utc)  # 0h em Brasília
        anteriores = [p for p in prazos if prazo and p < prazo]
        if not anteriores:
            return None
        fim = _data(anteriores[-1])  # o GitHub guarda só a data do prazo
        return datetime(fim.year, fim.month, fim.day, 3, tzinfo=timezone.utc) + timedelta(days=1)  # dia seguinte, 0h em Brasília

    def sem_andamento(issue):
        referencia = _data(issue.get("updated_at") or issue["created_at"])
        inicio = inicio_da_sprint(issue)
        if inicio and inicio > referencia:
            referencia = inicio
        return (agora - referencia).total_seconds() / 86400

    paradas = [i for i in issues if i["state"] == "open" and sem_andamento(i) > lim_dias]
    saida += [f"### Issues paradas", "",
              f"Issues ainda abertas e sem nenhuma atualização há mais de {_fmt(lim_dias, 0)} dia(s), "
              "contados a partir do início da sprint de cada issue "
              "(limite de decisão desta métrica):", ""]
    if paradas:
        saida.append(", ".join(link(i["number"]) for i in paradas) + ".")
    else:
        saida.append("Nenhuma no momento.")
    saida.append("")

    saida += ["O previsto e o realizado de cada entrega, com a evolução das três categorias ao longo das sprints, "
              "estão no [Dashboard do PSM](dashboard.md).", ""]

    return markdown.replace(MARCADOR_PSM, "\n".join(saida))


def on_page_markdown(markdown, page, config, files):
    if MARCADOR_HORAS in markdown:
        markdown = _tabela_horas(markdown, config)
    if MARCADOR_PSM in markdown:
        markdown = _painel_psm(markdown, config)
    return markdown