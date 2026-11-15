"""Analise reprodutivel da coleta oficial. Uso, na raiz: python dados/avaliacao/eficiencia/analisar.py
Usa somente biblioteca padrao; preserva o CSV original. Julgamentos exploratorios.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from statistics import median
from collections import defaultdict
import csv, hashlib, json
BASE=Path(__file__).resolve().parent
REPO=BASE.parents[2]
PORTES=(50,300,1000,2000,5000)
OPS=(("abrir",""),("rotulo",""),("exportar","png"),("exportar","pdf"),("exportar","svg"))
D=Decimal
REVISAO_ANTERIOR={'data_revisao': '2026-11-15', 'coleta': '2026-11-14', 'momento': 'pos-coleta', 'criterios_anteriores_sha256_lf': '89c73498ce70227af961e945498c272fdecb48c0b765eba02ff687acdadb1ea3', 'justificativa': 'Distinguir falha temporal observada de falta de dados e julgar memoria por medidas completas, sem alterar limites ou dados brutos.', 'resultados_anteriores': [{'metrica': 'M2.5', 'porte': '2000', 'operacao': 'exportar', 'formato': 'svg', 'unidade': 'MiB', 'tentativas': '5', 'sucessos': '4', 'falhas': '1', 'mediana': '116.305', 'minimo_sucessos': '110.69', 'maximo_sucessos': '140.83', 'limite': '620', 'razao': '0.1875887096774193548387096774', 'nota': '5', 'estado': 'exploratorio', 'mediana_descritiva_todas': '120.74'}, {'metrica': 'M2.4', 'porte': '5000', 'operacao': 'exportar', 'formato': 'svg', 'unidade': 'ms', 'tentativas': '5', 'sucessos': '0', 'falhas': '5', 'mediana': '', 'minimo_sucessos': '', 'maximo_sucessos': '', 'limite': '40000', 'razao': '', 'nota': '', 'estado': 'nao_conclusivo', 'mediana_descritiva_todas': '113646.1'}, {'metrica': 'M2.5', 'porte': '5000', 'operacao': 'exportar', 'formato': 'svg', 'unidade': 'MiB', 'tentativas': '5', 'sucessos': '0', 'falhas': '5', 'mediana': '', 'minimo_sucessos': '', 'maximo_sucessos': '', 'limite': '1050', 'razao': '', 'nota': '', 'estado': 'nao_conclusivo', 'mediana_descritiva_todas': '381.9'}], 'resumo_anterior': {'entrada_sha256_lf': 'b7d51d18d2e57c6841d3e8e690dd1a545bc594b23c446c6a5fd7df7a9c813324', 'criterios_sha256_lf': '89c73498ce70227af961e945498c272fdecb48c0b765eba02ff687acdadb1ea3', 'limites_aprovados': False, 'registros': 125, 'sucessos': 119, 'falhas': 6, 'metricas': {'M2.1': {'nota': 5, 'menor_nota_cenarios_conclusivos': 5, 'cenarios_nao_conclusivos': 0}, 'M2.2': {'nota': 5, 'menor_nota_cenarios_conclusivos': 5, 'cenarios_nao_conclusivos': 0}, 'M2.3': {'nota': 5, 'menor_nota_cenarios_conclusivos': 5, 'cenarios_nao_conclusivos': 0}, 'M2.4': {'nota': None, 'menor_nota_cenarios_conclusivos': 2, 'cenarios_nao_conclusivos': 1}, 'M2.5': {'nota': None, 'menor_nota_cenarios_conclusivos': 5, 'cenarios_nao_conclusivos': 1}}, 'capacidade_automatizada': 2000, 'nota_capacidade_exploratoria': 4, 'G2': None, 'capacidade_por_porte': [{'porte': 50, 'sucessos': [5, 5, 5, 5, 5], 'repetivel': True}, {'porte': 300, 'sucessos': [5, 5, 5, 5, 5], 'repetivel': True}, {'porte': 1000, 'sucessos': [5, 5, 5, 5, 5], 'repetivel': True}, {'porte': 2000, 'sucessos': [5, 5, 5, 5, 4], 'repetivel': True}, {'porte': 5000, 'sucessos': [5, 5, 5, 5, 0], 'repetivel': False}]}}

def sha(p):
    return hashlib.sha256(p.read_bytes().replace(b"\r\n",b"\n")).hexdigest()

def nota(r):
    for bound,value in ((D("0.5"),5),(D(1),4),(D("1.5"),3),(D(2),2)):
        if r<=bound:return value
    return 1

def fmt(x,p=1):
    if x is None:return "NC"
    v=D(str(x)).quantize(D(10)**-p,rounding=ROUND_HALF_UP)
    return f"{v:,.{p}f}".replace(",","_").replace(".",",").replace("_",".")

def table(head,rows):
    return "\n".join(["| "+" | ".join(head)+" |","| "+" | ".join("---" for _ in head)+" |"]+["| "+" | ".join(map(str,r))+" |" for r in rows])

def write_csv(path,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)

def main():
    source=BASE/"brutos/tentativas.csv"
    rules=REPO/"docs/fase-2/niveis-e-julgamento.md"
    input_hash,rules_hash=sha(source),sha(rules)
    assert input_hash=="b7d51d18d2e57c6841d3e8e690dd1a545bc594b23c446c6a5fd7df7a9c813324" and rules_hash=="6929f1a5535764744dcaa8a016a59dff7a4fcb5196de7f8032dbdea00f979379", "Insumos alterados: revisar a analise antes de regenerar o relato deste experimento"
    labels={"M2.1 abrir (ms)":("M2.1",""),"M2.2 heap após abrir (MiB)":("M2.2",""),"M2.3 rótulo (ms)":("M2.3","")}
    labels.update({f"{m} {f.upper()} ({u})":(m,f) for m,u in (("M2.4","ms"),("M2.5","MiB")) for f in ("png","pdf","svg")})
    limits={}
    for line in rules.read_text(encoding="utf-8").splitlines():
        cells=[c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in labels:
            assert len(cells)==6
            m,f=labels[cells[0]]
            for n,x in zip(PORTES,cells[1:]):limits[m,n,f]=D(x.replace(".","").replace(",","."))
    assert len(limits)==45
    with source.open(encoding="utf-8-sig",newline="") as f:rows=list(csv.DictReader(f))
    assert len(rows)==125
    expected={(n,op,f,t) for n in PORTES for op,f in OPS for t in range(1,6)}
    actual=[(int(r["porte"]),r["operacao"],r["formato"],int(r["tentativa"])) for r in rows]
    assert len(set(actual))==125 and set(actual)==expected
    validation_source=BASE/"brutos/exportados/validacao.csv"
    validation_hash=sha(validation_source)
    assert validation_hash=="b6d5fc14b46e6fa54b62a5ea0dbce28a453b0ed7169e0950509f309a802169e1", "Validacao alterada: revisar o encerramento"
    with validation_source.open(encoding="utf-8-sig",newline="") as f:validation=list(csv.DictReader(f))
    assert len(validation)==15 and {(int(v["porte"]),v["formato"]) for v in validation}=={(n,f) for n in PORTES for f in ("png","svg","pdf")}
    validation_summary={f:{"portes":5,"arquivos_abrem":sum(v["abre"]=="sim" for v in validation if v["formato"]==f),"checagem_completo":sum(v["diagrama_completo"]=="sim" for v in validation if v["formato"]==f)} for f in ("png","svg","pdf")}
    groups=defaultdict(list);classified=[]
    for raw in rows:
        r=dict(raw);n,op,f=int(r["porte"]),r["operacao"],r["formato"]
        time=D(r["tempo_ms"])
        assert r["data"]=="2026-11-14" and r["versao_chrome"]=="157.0.8103.79"
        assert time>=0 and abs(D(r["tf_ms"])-D(r["ti_ms"])-time)<=D("0.11")
        assert r["resultado"]=="sucesso" and not r["observacao"], "Registro exige revisao humana"
        if op!="rotulo":assert r["heap_mib"] and D(r["heap_mib"])>=0
        metric="M2.1" if op=="abrir" else "M2.3" if op=="rotulo" else "M2.4"
        limit=limits[metric,n,f]
        status="falha" if time>2*limit else "sucesso"
        r.update(limite_tempo_ms=str(limit),duas_vezes_limite_ms=str(2*limit),resultado_analise=status,motivo_analise="Tempo acima de 2L (limite candidato)" if status=="falha" else "Operacao concluida dentro de 2L")
        groups[n,op,f].append(r);classified.append(r)
    records=[]
    for n in PORTES:
        for op,f in OPS:
            group=groups[n,op,f];success=[r for r in group if r["resultado_analise"]=="sucesso"]
            measures=(("M2.1","tempo_ms","ms"),("M2.2","heap_mib","MiB")) if op=="abrir" else (("M2.3","tempo_ms","ms"),) if op=="rotulo" else (("M2.4","tempo_ms","ms"),("M2.5","heap_mib","MiB"))
            for m,col,unit in measures:
                amostras=group if m in ("M2.2","M2.5") else success
                vals=[D(r[col]) for r in amostras];valid=len(vals)>=4
                falha_temporal=m in ("M2.1","M2.3","M2.4") and not valid and len(group)==5 and (len(group)-len(success))>=2
                x=median(vals) if valid else None;limit=limits[m,n,f];ratio=x/limit if valid else None
                records.append(dict(metrica=m,porte=n,operacao=op,formato=f,unidade=unit,tentativas=5,sucessos=len(success),falhas=5-len(success),amostras_utilizadas=len(vals),mediana=str(x) if valid else "",minimo_sucessos=str(min(vals)) if vals else "",maximo_sucessos=str(max(vals)) if vals else "",limite=str(limit),razao=str(ratio) if valid else "",nota=nota(ratio) if valid else 1 if falha_temporal else "",estado="julgado_criterios_dupla" if valid else "falha_temporal" if falha_temporal else "nao_conclusivo",criterio_nota="mediana" if valid else "menos_de_quatro_sucessos_por_falha_temporal" if falha_temporal else "dados_insuficientes",mediana_descritiva_todas=str(median(D(r[col]) for r in group))))
    assert len(records)==45
    capacity=[]
    for n in PORTES:
        counts=[sum(r["resultado_analise"]=="sucesso" for r in groups[n,op,f]) for op,f in OPS]
        capacity.append(dict(porte=n,sucessos=counts,repetivel=all(c>=4 for c in counts)))
    largest=max((r["porte"] for r in capacity if r["repetivel"]),default=0)
    cap_note={5000:5,2000:4,1000:3,300:2,50:1,0:1}[largest]
    summary={}
    for m in ("M2.1","M2.2","M2.3","M2.4","M2.5"):
        rs=[r for r in records if r["metrica"]==m];notes=[r["nota"] for r in rs if r["nota"]!=""]
        summary[m]=dict(nota=min(notes) if len(notes)==len(rs) else None,menor_nota_cenarios_conclusivos=min(notes),cenarios_nao_conclusivos=len(rs)-len(notes))
    questoes={"Q2.1":min(summary["M2.1"]["nota"],summary["M2.2"]["nota"]),"Q2.2":summary["M2.3"]["nota"],"Q2.3":min(summary["M2.4"]["nota"],summary["M2.5"]["nota"]),"Q2.4":cap_note}
    data=dict(entrada_sha256_lf=input_hash,criterios_sha256_lf=rules_hash,limites_aprovados=True,aprovacao_limites={"responsavel":"Dupla 2 (Thiago e Pedro)","data":"2026-11-15","momento":"ratificacao pos-coleta, valores mantidos","aprovacao_externa_comprovada":False},registros=125,sucessos=sum(r["resultado_analise"]=="sucesso" for r in classified),falhas=sum(r["resultado_analise"]=="falha" for r in classified),metricas=summary,capacidade_automatizada=largest,nota_capacidade=cap_note,G2=min(questoes.values()),questoes=questoes,escopo_G2="fluxo instrumentado; PDF mede preparacao de impressao",validacao_exportacoes=validation_summary,validacao_sha256_lf=validation_hash,capacidade_fluxo_integral="nao demonstrada na validacao complementar",pendencias=[],revisao_pos_coleta="2026-11-15",capacidade_por_porte=capacity)
    out=BASE/"analise";out.mkdir(exist_ok=True)
    write_csv(out/"tentativas-classificadas.csv",classified)
    write_csv(out/"metricas-por-cenario.csv",records)
    (out/"resumo.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    encerramento=dict(data="2026-11-15",ratificacao_limites=data["aprovacao_limites"],validacao_pr=57,validacao_commits=["48d9f76","e913192"],validacao_sha256_lf=validation_hash,validacao_resultados=validation_summary,validacao_temporal_complementar=False,arquivos_finais_aprovados=False,analise_concluida=True,G2=data["G2"],escopo_G2=data["escopo_G2"],observacao="Verificacao executada com achados negativos: PDFs incompletos e SVG de 5000 nao gerado. Os resultados nao sao uma aprovacao funcional do fluxo completo. O pacote de exportacoes ja esta disponivel no Drive.")
    (out/"encerramento-pendencias.json").write_text(json.dumps(encerramento,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    revisao=dict(REVISAO_ANTERIOR,criterios_revisados_sha256_lf=rules_hash,resultados_revisados=[x for x in records if x["formato"]=="svg" and ((x["porte"]==2000 and x["metrica"]=="M2.5") or x["porte"]==5000)],resumo_revisado=data)
    (out/"revisao-criterios.json").write_text(json.dumps(revisao,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    lookup={(r["metrica"],r["porte"],r["formato"]):r for r in records}
    def cells(m,f=""):
        return [f'{(fmt(lookup[m,n,f]["mediana"],2 if m in ("M2.2","M2.5") else 1) if lookup[m,n,f]["mediana"] != "" else "—" if lookup[m,n,f]["nota"]==1 else "NC")} / {lookup[m,n,f]["nota"] or "—"}' for n in PORTES]
    times=table(["Métrica / operação (ms)"]+[fmt(n,0) for n in PORTES],[["M2.1 — Abrir"]+cells("M2.1"),["M2.3 — Rótulo"]+cells("M2.3")]+[["M2.4 — "+f.upper()]+cells("M2.4",f) for f in ("png","pdf","svg")])
    memory=table(["Métrica / operação (MiB)"]+[fmt(n,0) for n in PORTES],[["M2.2 — Após abrir"]+cells("M2.2")]+[["M2.5 — "+f.upper()]+cells("M2.5",f) for f in ("png","pdf","svg")])
    fails=table(["Porte","Tentativa SVG","Tempo (ms)","2L (ms)"],[[fmt(r["porte"],0),r["tentativa"],fmt(r["tempo_ms"]),fmt(r["duas_vezes_limite_ms"],0)] for r in classified if r["resultado_analise"]=="falha"])
    cap=table(["Porte","Demais operações*","SVG","Fluxo repetível?"],[[fmt(r["porte"],0),"5/5 em cada",str(r["sucessos"][-1])+"/5","Sim" if r["repetivel"] else "Não"] for r in capacity])
    validation_table=table(["Formato","Portes que passaram na checagem","Resultado"],[["PNG","5/5","Assinatura e dimensões esperadas nos cinco portes."],["SVG","4/5","Rótulos completos até 2.000 formas; arquivo de 5.000 não gerado."],["PDF","0/5","Os cinco abrem, mas a contagem encontrou 94% dos rótulos inteiros em cada porte."]])
    report=f"""## Eficiência de desempenho (Dupla 2)

<div class="mj-resultados-eficiencia" markdown="1">

A análise de Thiago Gomes Pereira de Abreu utiliza as 125 tentativas oficiais coletadas por Pedro Ian Guedes de Carvalho em 14/11/2026: cinco portes, cinco operações e cinco repetições.

Foram conferidos cenários, medidas obrigatórias e consistência entre duração e instantes registrados. Os pilotos não entram nos cálculos e o CSV original foi preservado.

**Critérios adotados:** a Dupla 2 ratificou os [limites da Fase 2](../fase-2/niveis-e-julgamento.md#eficiencia-de-desempenho-dupla-2) em 15/11/2026, após a coleta, mantendo os valores. Trata-se de decisão da dupla, não de aprovação prévia ou aceite externo. As notas julgam o fluxo instrumentado; a validação funcional complementar é apresentada separadamente.

### Tratamento das tentativas

Pelo [protocolo](index.md#tentativas-validas-falhas-e-interrupcoes), uma operação acima de `2L` é falha temporal. A mediana temporal exige quatro ou cinco sucessos. Pela [revisão pós-coleta de 15/11/2026](../fase-2/niveis-e-julgamento.md#revisao-pos-coleta-do-julgamento-15112026), menos de quatro sucessos por falha temporal do produto recebe nota 1, sem inventar uma mediana de sucessos. A memória é julgada separadamente, com as medidas completas das operações concluídas. Dados ausentes ou inválidos continuam não conclusivos. A classificação resulta em {data['sucessos']} sucessos e {data['falhas']} falhas temporais. As 125 operações concluíram na automação; a diferença é a aplicação posterior do critério temporal.

{fails}

No SVG de 2.000 formas, a exclusão temporal da tentativa 4 altera a mediana dos sucessos de 29.471,8 para 29.082,5 ms. As cinco medidas de memória completas são mantidas: mediana de 120,74 MiB. Em 5.000 formas, o SVG recebe nota temporal 1 pelas cinco falhas; não há mediana de sucessos. O tempo mediano bruto de 113.646,1 ms permanece descritivo. As cinco operações concluíram e forneceram heap válido, cuja mediana é 381,90 MiB e nota 5 (`381,90 / 1.050 ≈ 0,364`). A nota de memória não transforma a falha temporal em sucesso. O julgamento anterior foi preservado para auditoria; a revisão foi adotada após a coleta e não altera L.

### Medianas e notas por porte

Colunas indicam o número de formas; células mostram mediana / nota. Tempo usa cinco sucessos, exceto SVG de 2.000 formas (quatro); memória usa cinco medidas completas por cenário. `— / 1` indica falha temporal sem mediana de sucessos. Os cálculos usam valores sem arredondamento.

**Tempo, em ms:**

<div class="mj-eficiencia-medidas" markdown="1">

{times}

</div>

**Heap JavaScript, em MiB:**

<div class="mj-eficiencia-medidas" markdown="1">

{memory}

</div>

A pontuação usa `r = mediana / L`: notas 5, 4, 3, 2 e 1 nas faixas `r ≤ 0,5`, `≤ 1`, `≤ 1,5`, `≤ 2` e `> 2`, respectivamente. No SVG, `11.911,4 / 9.000 ≈ 1,32349` resulta em nota 3; `29.082,5 / 17.000 ≈ 1,71074`, em nota 2.

### Capacidade e consolidação

{cap}

*Demais operações: abrir, editar rótulo, exportar PNG e preparar a impressão de PDF. Cada uma obteve 5/5 sucessos temporais em todos os portes. A contagem não demonstra integridade dos arquivos finais.*

**M2.6 = {fmt(largest,0)} formas, nota {cap_note} no fluxo instrumentado:** maior porte ensaiado com pelo menos quatro sucessos em cada operação até `2L`. Isso não significa atendimento a `L`: o SVG de 2.000 formas recebe nota temporal 2. 300 formas é o maior porte ensaiado com todas as medianas de tempo e memória dentro de `L`.

| Métrica ou questão | Resultado | Condição |
| --- | --- | --- |
| M2.1, M2.2 e M2.3 | 5 em cada métrica | Todos os cenários têm nota 5. |
| M2.4 | 1 | SVG de 5.000 formas: 0/5 sucessos temporais. |
| M2.5 | 5 | Medidas de memória completas, inclusive nas operações lentas. |
| M2.6 / Q2.4 | 4 | Capacidade instrumentada de 2.000 formas. |
| Q2.1 / Q2.2 | 5 em cada questão | Abertura/memória e edição de rótulos. |
| Q2.3 | 1 | Mínimo entre M2.4 = 1 e M2.5 = 5. |
| G2 | 1 | Critérios ratificados pela dupla, no escopo temporal instrumentado. |

A consolidação segue o mínimo entre cenários, métricas e questões: `G2 = mínimo(5, 5, 1, 4) = 1`, conforme os critérios ratificados pela dupla. A revisão é pós-coleta e permanece identificada como tal. Dados ausentes ou inválidos não seriam omitidos nem receberiam nota artificial. A validação complementar abaixo não é incorporada como se fosse uma nova série de cinco medições.

### Validação complementar dos arquivos

O [PR #57](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/pull/57), integrado em 15/11/2026, registra a verificação realizada por Pedro em `brutos/exportados/validacao.csv`: 15 combinações de porte/formato, com 14 arquivos gerados. A análise utiliza esse CSV e o procedimento documentado, sem alegar reabertura independente dos arquivos externos. Trata-se de campanha funcional separada, sem nova medição de tempo.

{validation_table}

No PNG, a checagem cobre assinatura e dimensões, não inspeção exaustiva de cada elemento. No SVG gerado, cobre XML e quantidade de rótulos. Nos PDFs, há 10, 10, 20, 40 e 100 páginas nos cinco portes, com 47/50, 282/300, 940/1.000, 1.880/2.000 e 4.700/5.000 rótulos inteiros encontrados. Abrir o arquivo não equivale a preservar todo o diagrama.

O SVG de 5.000 formas não foi obtido nas quatro execuções complementares documentadas, incluindo erros de timeout. Como o caminho de salvamento e as condições diferem da coleta original, esses resultados não são somados às 125 tentativas nem usados para inventar tempos ou reclassificar retroativamente cada tentativa de PDF. A causa do comportamento distinto não foi isolada.

A capacidade temporal de 2.000 formas não demonstra capacidade funcional integral: a amostra complementar não apresenta PDF completo em nenhum porte. O pacote `eficiencia-exportacoes-2026-11-15.zip` já está disponível no Drive; o CSV e o manifesto já estão versionados.

### Hipóteses e interpretação

| Questão / hipótese | Situação no escopo medido | Evidência |
| --- | --- | --- |
| Q2.1 / H2.1 | Parcialmente corroborada | Tempo cresce de 74,0 a 1.397,9 ms; heap de 42,36 a 85,89 MiB, mas cai entre 1.000 e 2.000 formas. Todos atendem aos limites; o heap não cresce continuamente. |
| Q2.2 / H2.2 | Corroborada | Latência cresce de 37,7 a 171,0 ms, com nota 5 em todos os portes. |
| Q2.3 / H2.3 | Não corroborada | SVG recebe notas 3, 2 e 1 em 1.000, 2.000 e 5.000 formas, contrariando a hipótese de notas 4 ou 5 em todos os formatos. |
| Q2.4 / H2.4 | Não corroborada | SVG tem 0/5 sucessos temporais em 5.000 formas; maior porte repetível instrumentado é 2.000. |

Abertura e rótulos ficam abaixo da metade dos limites candidatos. SVG é a principal restrição: a mediana bruta cresce cerca de 257 vezes para um aumento de 100 vezes nas formas. A conversão de rótulos HTML em imagens, descrita na [coleta](coleta-de-dados.md#observacoes-da-coleta), é uma pista de investigação, não uma causa comprovada por esta análise.

PNG e preparação de PDF atendem aos limites. A variação do PNG em 5.000 formas (1.716,5–3.588,8 ms) foi preservada, sem exclusão arbitrária.

**Memória:** o máximo bruto de heap, 418,30 MiB, pertence a um SVG que falhou temporalmente. A nota 5 de memória resulta da mediana de 381,90 MiB das cinco operações concluídas, não desse máximo isolado. A oscilação pode envolver coleta de lixo, sem evidência suficiente para isolar essa causa.

### Limitações da avaliação

- **Ambiente e amostra:** draw.io 32.6.10, Chrome 157.0.8103.79, Windows 11 e Intel Core i5-1235U com 16 GB. São cinco repetições por cenário e cargas sintéticas de retângulos sem conectores. Não houve inferência estatística nem estimativa de capacidade absoluta.
- **Memória:** o heap JavaScript amostrado não representa RAM total e pode omitir picos entre amostras.
- **Automação e PDF:** o seletor de arquivos é alternativo e o salvamento não é medido. PDF mede somente preparação de impressão. A validação posterior verificou arquivos finais, mas não mediu seu tempo de geração. M2.6 continua restrita à repetibilidade temporal instrumentada, sem equivaler a capacidade funcional completa.
- **Base da análise e critérios:** foi conferido o CSV extraído, sem revalidar independentemente todos os traces. Os limites foram ratificados pela dupla após a coleta; não há aceite externo demonstrado. A regra de falha temporal também é posterior aos dados, e o julgamento anterior está preservado para comparação.

### Sugestões de melhoria

1. **Otimizar a exportação SVG:** investigar trabalho repetido e medir separadamente conversão de rótulos HTML em imagens e serialização, verificando a correção da saída.
2. **Dar retorno durante exportações demoradas:** oferecer progresso e cancelamento, avaliando processamento em etapas que preserve a resposta da interface.
3. **Prevenir regressões de desempenho:** acompanhar tempos, heap e falhas com as cinco cargas em versões futuras, mantendo ambiente e critérios documentados.

### Conclusão

Abertura e edição apresentam desempenho favorável nas cargas testadas. SVG é a principal restrição do fluxo: a repetibilidade temporal instrumentada alcança 2.000 formas, mas todas as medianas atendem a `L` somente até 300 formas. G2 = 1 indica restrição de desempenho no fluxo instrumentado, principalmente por SVG. A verificação complementar identificou ainda PDFs incompletos em todos os portes e ausência do SVG de 5.000 formas. Não se recomenda a adoção irrestrita do fluxo completo com as opções testadas. PNG é a alternativa funcional melhor sustentada pelas checagens realizadas; a validação não substitui testes com diagramas reais.


### Reprodução e auditoria

```powershell
python dados/avaliacao/eficiencia/analisar.py
```

O script preserva os dados brutos, lê os limites da Fase 2 e atualiza apenas esta seção. Em `dados/avaliacao/eficiencia/analise/`, gera:

- `tentativas-classificadas.csv`: 125 tentativas, com classificação e identificação das falhas;
- `metricas-por-cenario.csv`: 45 resultados, com medidas, limites, razões e notas;
- `resumo.json`: consolidação e hashes SHA-256 dos insumos normalizados para LF;
- `revisao-criterios.json`: regra adotada em 15/11/2026, julgamento anterior e resultados alterados;
- `encerramento-pendencias.json`: ratificação dos limites, origem e hash da validação complementar e alcance da conclusão.

Os hashes vinculam o relato à coleta e aos critérios utilizados; mudanças exigem revisão. As medidas brutas permanecem nesses arquivos. Traces e manifesto estão na [pasta de evidências](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

</div>

"""
    target=REPO/"docs/fase-3/resultados.md"
    old=target.read_text(encoding="utf-8")
    start=old.index("## Eficiência de desempenho (Dupla 2)")
    end=old.index("## Manutenibilidade (Dupla 3)",start)
    target.write_text(old[:start]+report+old[end:],encoding="utf-8",newline="\n")
    assert sha(source)==input_hash and sha(rules)==rules_hash
    print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=="__main__":main()