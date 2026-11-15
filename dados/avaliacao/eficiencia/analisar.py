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
    assert input_hash=="b7d51d18d2e57c6841d3e8e690dd1a545bc594b23c446c6a5fd7df7a9c813324" and rules_hash=="89c73498ce70227af961e945498c272fdecb48c0b765eba02ff687acdadb1ea3", "Insumos alterados: revisar a analise antes de regenerar o relato deste experimento"
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
                vals=[D(r[col]) for r in success];valid=len(vals)>=4
                x=median(vals) if valid else None;limit=limits[m,n,f];ratio=x/limit if valid else None
                records.append(dict(metrica=m,porte=n,operacao=op,formato=f,unidade=unit,tentativas=5,sucessos=len(success),falhas=5-len(success),mediana=str(x) if valid else "",minimo_sucessos=str(min(vals)) if vals else "",maximo_sucessos=str(max(vals)) if vals else "",limite=str(limit),razao=str(ratio) if valid else "",nota=nota(ratio) if valid else "",estado="exploratorio" if valid else "nao_conclusivo",mediana_descritiva_todas=str(median(D(r[col]) for r in group))))
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
    data=dict(entrada_sha256_lf=input_hash,criterios_sha256_lf=rules_hash,limites_aprovados=False,registros=125,sucessos=sum(r["resultado_analise"]=="sucesso" for r in classified),falhas=sum(r["resultado_analise"]=="falha" for r in classified),metricas=summary,capacidade_automatizada=largest,nota_capacidade_exploratoria=cap_note,G2=None,capacidade_por_porte=capacity)
    out=BASE/"analise";out.mkdir(exist_ok=True)
    write_csv(out/"tentativas-classificadas.csv",classified)
    write_csv(out/"metricas-por-cenario.csv",records)
    (out/"resumo.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
    lookup={(r["metrica"],r["porte"],r["formato"]):r for r in records}
    def cells(m,f=""):
        return [f'{fmt(lookup[m,n,f]["mediana"] or None,2 if m in ("M2.2","M2.5") else 1)} / {lookup[m,n,f]["nota"] or "—"}' for n in PORTES]
    times=table(["Métrica / operação (ms)"]+[fmt(n,0) for n in PORTES],[["M2.1 — Abrir"]+cells("M2.1"),["M2.3 — Rótulo"]+cells("M2.3")]+[["M2.4 — "+f.upper()]+cells("M2.4",f) for f in ("png","pdf","svg")])
    memory=table(["Métrica / operação (MiB)"]+[fmt(n,0) for n in PORTES],[["M2.2 — Após abrir"]+cells("M2.2")]+[["M2.5 — "+f.upper()]+cells("M2.5",f) for f in ("png","pdf","svg")])
    fails=table(["Porte","Tentativa SVG","Tempo (ms)","2L (ms)"],[[fmt(r["porte"],0),r["tentativa"],fmt(r["tempo_ms"]),fmt(r["duas_vezes_limite_ms"],0)] for r in classified if r["resultado_analise"]=="falha"])
    cap=table(["Porte","Demais operações*","SVG","Fluxo repetível?"],[[fmt(r["porte"],0),"5/5 em cada",str(r["sucessos"][-1])+"/5","Sim" if r["repetivel"] else "Não"] for r in capacity])
    report=f"""## Eficiência de desempenho (Dupla 2)

<div class="mj-resultados-eficiencia" markdown="1">

A análise de Thiago Gomes Pereira de Abreu utiliza as **125 tentativas oficiais** coletadas por Pedro Ian Guedes de Carvalho em 14/11/2026: cinco portes, cinco operações e cinco repetições.

Foram conferidos cenários, medidas obrigatórias e consistência entre duração e instantes registrados. Os pilotos não entram nos cálculos e o CSV original foi preservado.

**Julgamento exploratório:** os [limites da Fase 2](../fase-2/niveis-e-julgamento.md#eficiencia-de-desempenho-dupla-2) continuam candidatos, sem aprovação documentada. As notas abaixo dependem deles; não constituem aprovação definitiva do produto.

### Tratamento das tentativas

Pelo [protocolo](index.md#tentativas-validas-falhas-e-interrupcoes), uma operação acima de `2L` é falha temporal. A mediana exige quatro ou cinco sucessos; falhas são excluídas tanto do tempo quanto do heap da operação, sem receber valores artificiais. A classificação resulta em **{data['sucessos']} sucessos e {data['falhas']} falhas temporais**. As 125 operações concluíram na automação; a diferença é a aplicação posterior do critério temporal.

{fails}

No SVG de 2.000 formas, a exclusão da tentativa 4 altera as medianas de 29.471,8 para **29.082,5 ms** e de 120,74 para **116,305 MiB**. Em 5.000 formas, nenhum SVG atende a `2L`: M2.4 e M2.5 ficam **não conclusivas (NC)**. As medianas brutas de 113.646,1 ms e 381,90 MiB permanecem na auditoria, sem nota. Pela regra vigente, NC não é convertido automaticamente em nota 1.

### Medianas e notas por porte

Colunas indicam o número de formas; células mostram **mediana / nota exploratória**. São cinco sucessos por célula, exceto SVG de 2.000 formas (quatro). `NC / —` indica ausência de mediana julgável e nota. Os cálculos usam valores sem arredondamento.

**Tempo, em ms:**

<div class="mj-eficiencia-medidas" markdown="1">

{times}

</div>

**Heap JavaScript, em MiB:**

<div class="mj-eficiencia-medidas" markdown="1">

{memory}

</div>

A pontuação usa `r = mediana / L`: notas **5, 4, 3, 2 e 1** nas faixas `r ≤ 0,5`, `≤ 1`, `≤ 1,5`, `≤ 2` e `> 2`, respectivamente. No SVG, `11.911,4 / 9.000 ≈ 1,32349` resulta em nota 3; `29.082,5 / 17.000 ≈ 1,71074`, em nota 2.

### Capacidade e consolidação

{cap}

*Demais operações: abrir, editar rótulo, exportar PNG e preparar a impressão de PDF. Cada uma obteve 5/5 sucessos em todos os portes.*

**M2.6 = {fmt(largest,0)} formas, nota exploratória {cap_note}:** maior porte ensaiado com pelo menos quatro sucessos em cada operação até `2L`. Isso não significa atendimento a `L`: o SVG de 2.000 formas recebe nota temporal 2. **300 formas** é o maior porte ensaiado com todas as medianas de tempo e memória dentro de `L`.

| Métrica ou questão | Resultado exploratório | Condição |
| --- | --- | --- |
| M2.1, M2.2 e M2.3 | 5 em cada métrica | Todos os cenários têm nota 5. |
| M2.4 | Parcial; menor nota = 2 | SVG de 5.000 formas é NC. |
| M2.5 | Parcial; notas calculáveis = 5 | SVG de 5.000 formas é NC. |
| M2.6 / Q2.4 | 4 | Capacidade instrumentada de 2.000 formas. |
| Q2.1 / Q2.2 | 5 em cada questão | Abertura/memória e edição de rótulos. |
| Q2.3 | NC | Exportação sem todas as métricas conclusivas. |
| G2 | **Não emitido** | Q2.3 incompleto e limites não aprovados. |

A consolidação segue o mínimo entre cenários, métricas e questões, conforme a Fase 2. Cenários NC não são omitidos. A aprovação dos mesmos limites, por si só, não resolveria a ausência de julgamento do SVG em 5.000 formas.

### Hipóteses e interpretação

| Questão / hipótese | Situação exploratória | Evidência |
| --- | --- | --- |
| Q2.1 / H2.1 | Parcialmente corroborada | Tempo cresce de 74,0 a 1.397,9 ms; heap de 42,36 a 85,89 MiB, mas cai entre 1.000 e 2.000 formas. Todos atendem aos limites; o heap não cresce continuamente. |
| Q2.2 / H2.2 | Corroborada | Latência cresce de 37,7 a 171,0 ms, com nota 5 em todos os portes. |
| Q2.3 / H2.3 | Não corroborada | SVG recebe notas 3 e 2 em cenários conclusivos, contrariando a hipótese de notas 4 ou 5 em todos os formatos. |
| Q2.4 / H2.4 | Não corroborada | SVG tem 0/5 sucessos temporais em 5.000 formas; maior porte repetível instrumentado é 2.000. |

Abertura e rótulos ficam abaixo da metade dos limites candidatos. **SVG é a principal restrição:** a mediana bruta cresce cerca de 257 vezes para um aumento de 100 vezes nas formas. A conversão de rótulos HTML em imagens, descrita na [coleta](coleta-de-dados.md#observacoes-da-coleta), é uma pista de investigação, não uma causa comprovada por esta análise.

**PNG e preparação de PDF** atendem aos limites. A variação do PNG em 5.000 formas (1.716,5–3.588,8 ms) foi preservada, sem exclusão arbitrária.

**Memória:** o máximo bruto de heap, 418,30 MiB, pertence a um SVG que falhou temporalmente e não recebe nota. A oscilação pode envolver coleta de lixo, sem evidência suficiente para isolar essa causa.

### Limitações da avaliação

- **Ambiente e amostra:** draw.io 32.6.10, Chrome 157.0.8103.79, Windows 11 e Intel Core i5-1235U com 16 GB. São cinco repetições por cenário e cargas sintéticas de retângulos sem conectores. Não houve inferência estatística nem estimativa de capacidade absoluta.
- **Memória:** o heap JavaScript amostrado não representa RAM total e pode omitir picos entre amostras.
- **Automação e PDF:** o seletor de arquivos é alternativo e o salvamento não é medido. **PDF mede somente preparação de impressão**; a integridade final de todas as exportações não foi comprovada. A capacidade apresentada se restringe ao fluxo instrumentado.
- **Base da análise e critérios:** foi conferido o CSV extraído, sem revalidar independentemente todos os traces. Os limites permanecem candidatos, e o cenário NC impede fechar o julgamento da exportação.

### Sugestões de melhoria

1. **Otimizar a exportação SVG:** investigar trabalho repetido e medir separadamente conversão de rótulos HTML em imagens e serialização, verificando a correção da saída.
2. **Dar retorno durante exportações demoradas:** oferecer progresso e cancelamento, avaliando processamento em etapas que preserve a resposta da interface.
3. **Prevenir regressões de desempenho:** acompanhar tempos, heap e falhas com as cinco cargas em versões futuras, mantendo ambiente e critérios documentados.

### Conclusão

Abertura e edição apresentam desempenho favorável nas cargas testadas. **SVG é a principal restrição do fluxo:** a repetibilidade exploratória alcança **2.000 formas**, mas todas as medianas atendem a `L` somente até **300 formas**. Os resultados sustentam uma avaliação parcial de adoção, **sem nota global G2 ou recomendação irrestrita**.

**Para concluir a avaliação:** aprovar os critérios, formalizar o tratamento do cenário NC e medir/validar os arquivos finais, especialmente PDF. Essas pendências dizem respeito ao fechamento da avaliação; as sugestões acima se destinam à melhoria do produto.

### Reprodução e auditoria

```powershell
python dados/avaliacao/eficiencia/analisar.py
```

O script preserva os dados brutos, lê os limites da Fase 2 e atualiza apenas esta seção. Em `dados/avaliacao/eficiencia/analise/`, gera:

- `tentativas-classificadas.csv`: **125 tentativas**, com classificação e identificação das falhas;
- `metricas-por-cenario.csv`: **45 resultados**, com medidas, limites, razões e notas;
- `resumo.json`: consolidação e hashes SHA-256 dos insumos normalizados para LF.

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