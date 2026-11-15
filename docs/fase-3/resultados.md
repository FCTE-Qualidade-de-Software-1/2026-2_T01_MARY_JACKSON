# Análise dos dados e resultados

Esta página apresenta o cálculo das métricas a partir dos registros da [coleta de dados](coleta-de-dados.md), a atribuição das notas conforme as [métricas](../fase-2/metricas.md) e os [níveis de julgamento](../fase-2/niveis-e-julgamento.md) definidos na Fase 2, além das sugestões de melhoria e da conclusão inicial de cada característica avaliada.

## Segurança (Dupla 1 — Objetivo G1)

### Cálculo das métricas e julgamento (ISO/IEC 25040)

Conforme definido na árvore GQM da Fase 2, a métrica **M1.1** é calculada individualmente por componente avaliado (sem agregação somada entre superfícies distintas):

| Questão / Métrica | Fórmula Aplicada | Resultado | Nota (1–5) | Critério Atingido |
| --- | --- | --- | --- | --- |
| **Q1.1** — Importação XML (**M1.1**) | `Cb,1 / Ct,1 = 1 / 1` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.2** — Rótulos HTML (**M1.1**) | `Cb,2 / Ct,2 = 1 / 1` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.3** — Proxy / Servidor (**M1.1**) | `Cb,3 / Ct,3 = 2 / 2` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.4** — Sanitização Estática (**M1.2**) | `M1.2 = (Pp / Pt) × 100 = (4 / 4) × 100` | **`100%`** | **5** | Cobertura total dos pontos válidos |
| **Q1.5** — Resistência a Bypasses (**M1.3**) | `M1.3 = (Wb / Wt) × 100 = (3 / 3) × 100` | **`100%`** | **5** | Neutralização de todas as variações |

### Pontuação final, sugestões e conclusão inicial

> **Nota Global (G1) = `min(Q1.1, Q1.2, Q1.3, Q1.4, Q1.5) = min(5, 5, 5, 5, 5) = 5`**

- **Análise:**
  * **Cliente web e inspeção estática (`Q1.1`, `Q1.2`, `Q1.4` e `Q1.5`):** A versão `32.6.10` centraliza a sanitização de rótulos HTML no método sobrescrito `cellRenderer.getLabelValue` (aplicando `DOMPurify` via `sanitizeLabel` quando `html=1`) e aplica escape explícito por `mxUtils.htmlEntities` nos pontos de medição de texto plano renderizados como HTML. O ponto principal de validação da hipótese `H1.4` encontra-se em `Format.js:5683` (`canConvertHtmlToSvg`), onde o rótulo é atribuído ao `.innerHTML` — vetor explorado anteriormente na CVE-2026-58504 mediante células não editáveis (`editable=0`) — mas que na `32.6.10` executa exclusivamente sob `html=1` após sanitização completa.
  * **Servidor Java e *servlet* `/proxy` (`Q1.3`):** Na execução complementar sobre a imagem oficial com servidor Tomcat (`jgraph/drawio:32.6.10`), confirmou-se que o `ProxyServlet` está mapeado (`WEB-INF/web.xml:11-18`) e aplica defesa *secure by default* (`ProxyServlet.java:74-76`), recusando imediatamente qualquer requisição com `HTTP 404` vazio quando a variável de ambiente `ENABLE_DRAWIO_PROXY` não está explicitamente habilitada, além de validar esquemas e bloquear endereços locais/privados via `Utils.validatedAddress` quando ativo.
- **Sugestões de melhoria ao draw.io:**
  * **Testes automatizados de regressão de sanitização:** Incluir na suíte de testes automatizados do cliente web casos cobrindo variações de evasão com elementos vetoriais SVG, quadros embutidos e esquemas de URI de script em células com `editable=0` (incluindo o fluxo de `canConvertHtmlToSvg`), prevenindo regressões em futuras atualizações da biblioteca de sanitização.
  * **Cabeçalhos de *Content Security Policy* (CSP) no deploy estático:** Recomendar na documentação oficial de implantação estática (Apache, Nginx e Docker) uma política CSP restritiva (bloqueando scripts inline e URIs de execução de script) como camada complementar de defesa em profundidade ao `DOMPurify`.
- **Conclusão inicial:** Todas as hipóteses de segurança (`H1.1` a `H1.5`) foram confirmadas. Recomenda-se a **adoção** da versão `32.6.10` sob a perspectiva da característica de Segurança, registrando-se como limitação metodológica que os testes iniciais do cliente web utilizaram vínculo de porta aberto na rede local (`0.0.0.0:8080`), corrigido para `127.0.0.1:8080` na validação do servidor Java e adotado como padrão para as próximas coletas.

## Eficiência de desempenho (Dupla 2)

<div class="mj-resultados-eficiencia" markdown="1">

A análise de Thiago Gomes Pereira de Abreu utiliza as 125 tentativas oficiais coletadas por Pedro Ian Guedes de Carvalho em 14/11/2026: cinco portes, cinco operações e cinco repetições.

Foram conferidos cenários, medidas obrigatórias e consistência entre duração e instantes registrados. Os pilotos não entram nos cálculos e o CSV original foi preservado.

**Julgamento exploratório:** os [limites da Fase 2](../fase-2/niveis-e-julgamento.md#eficiencia-de-desempenho-dupla-2) continuam candidatos, sem aprovação documentada. As notas abaixo dependem deles; não constituem aprovação definitiva do produto.

### Tratamento das tentativas

Pelo [protocolo](index.md#tentativas-validas-falhas-e-interrupcoes), uma operação acima de `2L` é falha temporal. A mediana temporal exige quatro ou cinco sucessos. Pela [revisão pós-coleta de 15/11/2026](../fase-2/niveis-e-julgamento.md#revisao-pos-coleta-do-julgamento-15112026), menos de quatro sucessos por falha temporal do produto recebe nota 1, sem inventar uma mediana de sucessos. A memória é julgada separadamente, com as medidas completas das operações concluídas. Dados ausentes ou inválidos continuam não conclusivos. A classificação resulta em 119 sucessos e 6 falhas temporais. As 125 operações concluíram na automação; a diferença é a aplicação posterior do critério temporal.

| Porte | Tentativa SVG | Tempo (ms) | 2L (ms) |
| --- | --- | --- | --- |
| 2.000 | 4 | 40.056,2 | 34.000 |
| 5.000 | 1 | 113.422,1 | 80.000 |
| 5.000 | 2 | 118.537,9 | 80.000 |
| 5.000 | 3 | 110.703,9 | 80.000 |
| 5.000 | 4 | 126.107,8 | 80.000 |
| 5.000 | 5 | 113.646,1 | 80.000 |

No SVG de 2.000 formas, a exclusão temporal da tentativa 4 altera a mediana dos sucessos de 29.471,8 para 29.082,5 ms. As cinco medidas de memória completas são mantidas: mediana de 120,74 MiB. Em 5.000 formas, o SVG recebe nota temporal 1 pelas cinco falhas; não há mediana de sucessos. O tempo mediano bruto de 113.646,1 ms permanece descritivo. As cinco operações concluíram e forneceram heap válido, cuja mediana é 381,90 MiB e nota 5 (`381,90 / 1.050 ≈ 0,364`). A nota de memória não transforma a falha temporal em sucesso. O julgamento anterior foi preservado para auditoria; a revisão foi adotada após a coleta e não altera L.

### Medianas e notas por porte

Colunas indicam o número de formas; células mostram mediana / nota exploratória. Tempo usa cinco sucessos, exceto SVG de 2.000 formas (quatro); memória usa cinco medidas completas por cenário. `— / 1` indica falha temporal sem mediana de sucessos. Os cálculos usam valores sem arredondamento.

**Tempo, em ms:**

<div class="mj-eficiencia-medidas" markdown="1">

| Métrica / operação (ms) | 50 | 300 | 1.000 | 2.000 | 5.000 |
| --- | --- | --- | --- | --- | --- |
| M2.1 — Abrir | 74,0 / 5 | 159,6 / 5 | 337,4 / 5 | 580,0 / 5 | 1.397,9 / 5 |
| M2.3 — Rótulo | 37,7 / 5 | 40,1 / 5 | 64,3 / 5 | 77,1 / 5 | 171,0 / 5 |
| M2.4 — PNG | 92,7 / 5 | 231,1 / 5 | 592,3 / 5 | 1.055,2 / 5 | 2.843,0 / 5 |
| M2.4 — PDF | 177,6 / 5 | 355,3 / 5 | 966,1 / 5 | 2.019,2 / 5 | 6.946,4 / 5 |
| M2.4 — SVG | 442,2 / 5 | 1.930,7 / 5 | 11.911,4 / 3 | 29.082,5 / 2 | — / 1 |

</div>

**Heap JavaScript, em MiB:**

<div class="mj-eficiencia-medidas" markdown="1">

| Métrica / operação (MiB) | 50 | 300 | 1.000 | 2.000 | 5.000 |
| --- | --- | --- | --- | --- | --- |
| M2.2 — Após abrir | 42,36 / 5 | 45,53 / 5 | 55,12 / 5 | 51,25 / 5 | 85,89 / 5 |
| M2.5 — PNG | 38,09 / 5 | 40,93 / 5 | 52,45 / 5 | 63,92 / 5 | 90,87 / 5 |
| M2.5 — PDF | 38,66 / 5 | 43,77 / 5 | 62,65 / 5 | 91,89 / 5 | 134,77 / 5 |
| M2.5 — SVG | 40,36 / 5 | 48,92 / 5 | 120,62 / 5 | 120,74 / 5 | 381,90 / 5 |

</div>

A pontuação usa `r = mediana / L`: notas 5, 4, 3, 2 e 1 nas faixas `r ≤ 0,5`, `≤ 1`, `≤ 1,5`, `≤ 2` e `> 2`, respectivamente. No SVG, `11.911,4 / 9.000 ≈ 1,32349` resulta em nota 3; `29.082,5 / 17.000 ≈ 1,71074`, em nota 2.

### Capacidade e consolidação

| Porte | Demais operações* | SVG | Fluxo repetível? |
| --- | --- | --- | --- |
| 50 | 5/5 em cada | 5/5 | Sim |
| 300 | 5/5 em cada | 5/5 | Sim |
| 1.000 | 5/5 em cada | 5/5 | Sim |
| 2.000 | 5/5 em cada | 4/5 | Sim |
| 5.000 | 5/5 em cada | 0/5 | Não |

*Demais operações: abrir, editar rótulo, exportar PNG e preparar a impressão de PDF. Cada uma obteve 5/5 sucessos em todos os portes.*

**M2.6 = 2.000 formas, nota exploratória 4:** maior porte ensaiado com pelo menos quatro sucessos em cada operação até `2L`. Isso não significa atendimento a `L`: o SVG de 2.000 formas recebe nota temporal 2. 300 formas é o maior porte ensaiado com todas as medianas de tempo e memória dentro de `L`.

| Métrica ou questão | Resultado exploratório | Condição |
| --- | --- | --- |
| M2.1, M2.2 e M2.3 | 5 em cada métrica | Todos os cenários têm nota 5. |
| M2.4 | 1 | SVG de 5.000 formas: 0/5 sucessos temporais. |
| M2.5 | 5 | Medidas de memória completas, inclusive nas operações lentas. |
| M2.6 / Q2.4 | 4 | Capacidade instrumentada de 2.000 formas. |
| Q2.1 / Q2.2 | 5 em cada questão | Abertura/memória e edição de rótulos. |
| Q2.3 | 1 | Mínimo entre M2.4 = 1 e M2.5 = 5. |
| G2 | 1 exploratório | Julgamento definitivo pendente de critérios aprovados e exportação completa. |

A consolidação segue o mínimo entre cenários, métricas e questões: `G2 = mínimo(5, 5, 1, 4) = 1`, de forma exploratória. A lacuna das 5.000 formas foi fechada pela regra pós-coleta; continuam pendentes a aprovação dos limites e a validação da exportação completa. Dados ausentes ou inválidos, caso existissem, não seriam omitidos nem receberiam nota artificial.

### Hipóteses e interpretação

| Questão / hipótese | Situação exploratória | Evidência |
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
- **Automação e PDF:** o seletor de arquivos é alternativo e o salvamento não é medido. PDF mede somente preparação de impressão; a integridade final de todas as exportações não foi comprovada. A capacidade apresentada se restringe ao fluxo instrumentado.
- **Base da análise e critérios:** foi conferido o CSV extraído, sem revalidar independentemente todos os traces. Os limites permanecem candidatos. A regra de falha temporal foi revisada após observar os dados, e o julgamento anterior está preservado para comparação.

### Sugestões de melhoria

1. **Otimizar a exportação SVG:** investigar trabalho repetido e medir separadamente conversão de rótulos HTML em imagens e serialização, verificando a correção da saída.
2. **Dar retorno durante exportações demoradas:** oferecer progresso e cancelamento, avaliando processamento em etapas que preserve a resposta da interface.
3. **Prevenir regressões de desempenho:** acompanhar tempos, heap e falhas com as cinco cargas em versões futuras, mantendo ambiente e critérios documentados.

### Conclusão

Abertura e edição apresentam desempenho favorável nas cargas testadas. SVG é a principal restrição do fluxo: a repetibilidade exploratória alcança 2.000 formas, mas todas as medianas atendem a `L` somente até 300 formas. O julgamento exploratório G2 = 1 indica restrição de desempenho do fluxo completo sob os critérios adotados, principalmente por SVG, sem uma recomendação definitiva de adoção.

**Pendências para o julgamento definitivo:** registrar a aprovação dos [limites candidatos](../fase-2/niveis-e-julgamento.md#eficiencia-de-desempenho-dupla-2) e medir/validar os arquivos exportados, especialmente o PDF final. A análise dos dados disponíveis está apresentada acima. Essas pendências limitam uma decisão definitiva de adoção e não se confundem com melhorias do produto.

### Reprodução e auditoria

```powershell
python dados/avaliacao/eficiencia/analisar.py
```

O script preserva os dados brutos, lê os limites da Fase 2 e atualiza apenas esta seção. Em `dados/avaliacao/eficiencia/analise/`, gera:

- `tentativas-classificadas.csv`: 125 tentativas, com classificação e identificação das falhas;
- `metricas-por-cenario.csv`: 45 resultados, com medidas, limites, razões e notas;
- `resumo.json`: consolidação e hashes SHA-256 dos insumos normalizados para LF;
- `revisao-criterios.json`: regra adotada em 15/11/2026, julgamento anterior e resultados alterados.

Os hashes vinculam o relato à coleta e aos critérios utilizados; mudanças exigem revisão. As medidas brutas permanecem nesses arquivos. Traces e manifesto estão na [pasta de evidências](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

</div>

## Manutenibilidade (Dupla 3)

*Espaço reservado para a análise e resultados da Dupla 3.*