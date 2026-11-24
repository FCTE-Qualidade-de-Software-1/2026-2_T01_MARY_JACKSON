# Análise dos dados e resultados

Esta página apresenta o cálculo das métricas a partir dos registros da [coleta de dados](coleta-de-dados.md), a atribuição das notas conforme as [métricas](../fase-2/metricas.md) e os [níveis de julgamento](../fase-2/niveis-e-julgamento.md) definidos na Fase 2, além das sugestões de melhoria e da conclusão inicial de cada característica avaliada.

## Segurança (Dupla 1 — Objetivo G1)

### Cálculo das métricas e julgamento (ISO/IEC 25040)

Conforme definido na árvore GQM da Fase 2, a métrica **M1.1** é calculada individualmente por componente avaliado (sem agregação somada entre superfícies distintas):

| Questão / Métrica | Fórmula Aplicada | Resultado | Nota (1–5) | Critério Atingido |
| --- | --- | --- | --- | --- |
| **Q1.1** — Importação XML (**M1.1**) | `Cb,1 / Ct,1 = 2 / 2` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.2** — Rótulos HTML (**M1.1**) | `Cb,2 / Ct,2 = 2 / 2` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.3** — Proxy / Servidor (**M1.1**) | `Cb,3 / Ct,3 = 2 / 2` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.4** — Sanitização Estática (**M1.2**) | `M1.2 = (Pp / Pt) × 100 = (4 / 4) × 100` | **`100%`** | **5** | Cobertura total dos pontos válidos |
| **Q1.5** — Resistência a Bypasses (**M1.3**) | `M1.3 = (Wb / Wt) × 100 = (3 / 3) × 100` | **`100%`** | **5** | Neutralização de todas as variações |

### Pontuação final, sugestões e conclusão inicial

> **Nota Global (G1) = `min(Q1.1, Q1.2, Q1.3, Q1.4, Q1.5) = min(5, 5, 5, 5, 5) = 5`**

**Análise**

- **Cliente web e inspeção estática (`Q1.1`, `Q1.2`, `Q1.4` e `Q1.5`):** A versão `32.6.10` centraliza a sanitização de rótulos HTML no método sobrescrito `cellRenderer.getLabelValue` (aplicando `DOMPurify` via `sanitizeLabel` quando `html=1`) e aplica escape explícito por `mxUtils.htmlEntities` nos pontos de medição de texto plano renderizados como HTML. O ponto principal de validação da hipótese `H1.4` encontra-se em `Format.js:5683` (`canConvertHtmlToSvg`), onde o rótulo é atribuído ao `.innerHTML` — vetor explorado anteriormente na CVE-2026-58504 mediante células não editáveis (`editable=0`) — mas que na `32.6.10` executa exclusivamente sob `html=1` após sanitização completa, comportamento confirmado dinamicamente nos cenários com `editable=0` (`TD-06` e `TD-09`).
- **Servidor Java e *servlet* de exportação (`Q1.3`):** Na execução sobre a imagem oficial com servidor Tomcat (`jgraph/drawio:32.6.10`) com a variável `EXPORT_URL` configurada, avaliou-se o `ExportProxyServlet` mapeado nas rotas `/export` e `/service/*` (`WEB-INF/web.xml`) contra vetores de travessia de diretório (`TD-03` e `TD-04`, ref. CVE-2026-63416). Confirmou-se uma arquitetura de defesa em profundidade: o Apache Tomcat 9.0.123 rejeita URIs contendo sequências de travessia e barras codificadas diretamente na camada HTTP (`HTTP/1.1 400 Bad Request`) antes mesmo de acionar o *servlet*, complementando a verificação explícita de *Path Traversal* (`..`) implementada em `ExportProxyServlet.java` (linhas 99–113).

**Sugestões de melhoria ao draw.io**

- **Testes automatizados de regressão de sanitização:** Incluir na suíte de testes automatizados do cliente web casos cobrindo variações de evasão com elementos vetoriais SVG, quadros embutidos e esquemas de URI de script em células com `editable=0` (incluindo o fluxo de `canConvertHtmlToSvg`), prevenindo regressões em futuras atualizações da biblioteca de sanitização.
- **Cabeçalhos de *Content Security Policy* (CSP) no deploy estático:** Recomendar na documentação oficial de implantação estática (Apache, Nginx e Docker) uma política CSP restritiva (bloqueando scripts inline e URIs de execução de script) como camada complementar de defesa em profundidade ao `DOMPurify`.

**Conclusão inicial**

Todas as hipóteses de segurança (`H1.1` a `H1.5`) foram confirmadas. Recomenda-se a **adoção** da versão `32.6.10` sob a perspectiva da característica de Segurança, registrando-se como limitação metodológica que a primeira rodada de testes do cliente web utilizou vínculo de porta aberto na rede local (`0.0.0.0:8080`), corrigido para `127.0.0.1:8080` na validação do servidor Java e nos casos complementares (`TD-08` e `TD-09`), adotado como padrão para as próximas coletas.

### Mitigação Complementar: Aplicação de Content Security Policy (Antes × Depois)

Como camada adicional de defesa em profundidade (*defense-in-depth*) para implantações *self-hosted*, validou-se o impacto da aplicação de uma política CSP restritiva sobre a funcionalidade do editor e sobre a neutralização de vetores de XSS:

| Critério Avaliado | Antes (Configuração Padrão) | Depois (Com CSP via `mod_headers`) |
| :--- | :--- | :--- |
| **Cabeçalho `Content-Security-Policy`** | Ausente na resposta HTTP (`HTTP/1.1 200 OK` apenas com cabeçalhos padrão do Apache). | Presente em todas as respostas (`default-src 'self'; script-src 'self' 'unsafe-eval'; object-src 'none'; ...`). |
| **Carregamento e Edição (`?offline=1`)** | Funcional; dependente exclusivamente da sanitização DOM no cliente. | Funcional; criação de formas, edição de rótulos e renderização do canvas operam sem erros de CSP. |
| **Exportação Local (PNG)** | Funcional. | Funcional (`Untitled Diagram.drawio.png` gerado sem bloqueios para `blob:`/`data:` em `img-src`). |
| **Scripts Externos de Terceiros** | Carregamento permitido se houver acesso à rede. | Bloqueado ativamente (`bootstrap.js:209` — tentativa de carregar `https://apis.google.com/js/api.js` barrada por `script-src 'self'`). |
| **Manipuladores Inline (`onerror` / `onload`)** | Mitigados apenas pela sanitização do cliente. | Dupla camada: mesmo quando nós HTML (`<img src="x">`) alcançam o DOM do rótulo, o navegador bloqueia a execução em `app.min.js:7` por violação de `script-src 'self' 'unsafe-eval'`. |

#### Evidência dos Cabeçalhos HTTP (`curl.exe -I http://127.0.0.1:8080`)

**Antes (sem CSP):**
```http
HTTP/1.1 200 OK
Date: Mon, 23 Nov 2026 01:37:12 GMT
Server: Apache/2.4.71 (Unix)
Last-Modified: Fri, 13 Nov 2026 21:46:14 GMT
ETag: "1082-6602f5b754af7"
Accept-Ranges: bytes
Content-Length: 4226
Content-Type: text/html
```

**Depois (com CSP ativa):**
```http
HTTP/1.1 200 OK
Date: Mon, 23 Nov 2026 01:37:15 GMT
Server: Apache/2.4.71 (Unix)
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-eval' ; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self';
Last-Modified: Fri, 13 Nov 2026 21:46:14 GMT
ETag: "1082-6602f5b754af7"
Accept-Ranges: bytes
Content-Length: 4226
Content-Type: text/html
```

## Eficiência de desempenho (Dupla 2)

<div class="mj-resultados-eficiencia" markdown="1">

A análise de Thiago Gomes Pereira de Abreu utiliza as 125 tentativas oficiais coletadas por Pedro Ian Guedes de Carvalho em 14/11/2026: cinco portes, cinco operações e cinco repetições. Foram conferidos cenários e medidas, excluindo os pilotos e preservando os dados brutos.

### Cálculo das métricas e julgamento

Conforme o [protocolo](../fase-3/ambiente-de-execucao.md#tentativas-validas-falhas-e-interrupcoes-eficiencia) e a [revisão do julgamento](../fase-2/niveis-e-julgamento.md#revisao-pos-coleta-do-julgamento-15112026), tempos acima de `2L` são falhas. A mediana temporal exige pelo menos quatro sucessos; menos sucessos por falha temporal recebem nota 1. Memória usa as cinco medidas completas, inclusive de operações lentas; dados ausentes ou inválidos permanecem não conclusivos.

As 125 operações concluíram na automação, mas o critério temporal resulta em 119 sucessos e 6 falhas, todas no SVG: uma em 2.000 formas (tentativa 4, 40.056,2 ms > 34.000 ms) e cinco em 5.000 formas (> 80.000 ms).

As células mostram mediana / nota, calculada sem arredondamento por `r = mediana / L`: notas 5, 4, 3, 2 e 1 para `r ≤ 0,5`, `≤ 1`, `≤ 1,5`, `≤ 2` e `> 2`. SVG de 2.000 formas usa quatro sucessos temporais; `— / 1` indica falha temporal sem mediana de sucessos.

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

### Pontuação e interpretação das hipóteses

<div class="mj-eficiencia-sintese" markdown="1">

| Questão / métricas | Nota | Hipótese | Interpretação |
| --- | --- | --- | --- |
| Q2.1 / M2.1 e M2.2 | 5 em ambas | H2.1 parcialmente corroborada | Abertura e heap atendem aos limites, mas o heap cai de 55,12 para 51,25 MiB entre 1.000 e 2.000 formas; não há crescimento contínuo. |
| Q2.2 / M2.3 | 5 | H2.2 corroborada | Latência de rótulo entre 37,7 e 171,0 ms, sempre abaixo de metade de L. |
| Q2.3 / M2.4 e M2.5 | 1 | H2.3 não corroborada | Tempo de SVG recebe notas 3, 2 e 1 nos três maiores portes, contrariando a hipótese de notas 4 ou 5. M2.4 = 1 e M2.5 = 5; memória adequada não compensa falha temporal. |
| Q2.4 / M2.6 | 4 | H2.4 não corroborada | SVG tem 4/5 sucessos temporais em 2.000 formas e 0/5 em 5.000; demais operações têm 5/5 em todos os portes. |

</div>

A capacidade temporal instrumentada é de 2.000 formas, com pelo menos quatro sucessos por operação até `2L`. O maior porte ensaiado com todas as medianas dentro de `L` é 300 formas. A capacidade temporal não comprova integridade dos arquivos finais.

A agregação utiliza o mínimo entre cenários, métricas e questões: `G2 = mínimo(5, 5, 1, 4) = 1`, restrito ao fluxo instrumentado.

### Validação dos arquivos exportados

A campanha complementar de Pedro ([PR #57](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/pull/57)) verificou 15 combinações de porte/formato, com 14 arquivos gerados. Os resultados de `brutos/exportados/validacao.csv` são funcionais, sem medição de tempo e separados das 125 tentativas oficiais.

<div class="mj-eficiencia-sintese" markdown="1">

| Formato | Portes que passaram na checagem | Resultado |
| --- | --- | --- |
| PNG | 5/5 | Assinatura e dimensões esperadas nos cinco portes. |
| SVG | 4/5 | Rótulos completos até 2.000 formas; arquivo de 5.000 não gerado. |
| PDF | 0/5 | Os cinco abrem, mas a contagem encontrou 94% dos rótulos inteiros em cada porte. |

</div>

Nos SVGs gerados, a checagem cobre XML e contagem de rótulos; em PNG, assinatura e dimensões, sem inspeção exaustiva dos elementos. O SVG de 5.000 formas não foi obtido em quatro execuções complementares, com timeouts e condições de salvamento diferentes da coleta original; a causa não foi isolada. Os PDFs abrem, mas nenhum preserva todos os rótulos inteiros nas opções testadas.

### Sugestões de melhoria

- **Otimizar SVG:** investigar conversão de rótulos HTML em imagens e serialização, medindo suas etapas e verificando a saída; a causa da lentidão não foi comprovada.
- **Investigar a saída PDF:** revisar paginação e recorte de rótulos nas opções testadas, verificando a integridade dos diagramas exportados.
- **Melhorar a resposta durante exportações:** oferecer progresso e cancelamento e avaliar processamento em etapas.
- **Prevenir regressões:** acompanhar tempos, heap, integridade e falhas com as cinco cargas nas próximas versões.

### Conclusão e limitações

Abertura e edição apresentam desempenho favorável nas cargas testadas. G2 = 1 indica restrição de desempenho, principalmente por SVG. Os PDFs incompletos e a ausência do SVG de 5.000 formas também impedem recomendar adoção irrestrita do fluxo completo nas opções testadas. PNG é a alternativa funcional melhor sustentada pelas checagens realizadas.

**Limitações:**

- **Ambiente e amostra:** draw.io 32.6.10, Chrome 157.0.8103.79, Windows 11 e Intel Core i5-1235U com 16 GB. Cinco repetições por cenário, cargas sintéticas sem conectores e ausência de inferência estatística não permitem generalizar capacidade absoluta ou uso com diagramas reais.
- **Instrumentação:** heap amostrado não equivale à RAM total e pode omitir picos. O salvamento não é cronometrado; PDF mede somente preparação de impressão, sem tempo de geração do arquivo final.
- **Base e critérios:** a análise conferiu os CSVs, sem revalidar todos os traces ou reabrir independentemente os arquivos externos. A Dupla 2 ratificou os [limites](../fase-2/niveis-e-julgamento.md#eficiencia-de-desempenho-dupla-2) em 15/11/2026, após a coleta, mantendo os valores, sem aceite externo demonstrado. A revisão do julgamento também é pós-coleta e mantém o resultado anterior para auditoria.

**Reprodução e evidências:** o [README da coleta](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/blob/main/dados/avaliacao/eficiencia/README.md) reúne o comando, os arquivos derivados e os detalhes de auditoria. O pacote `eficiencia-exportacoes-2026-11-15.zip`, os traces e o manifesto estão na [pasta do Drive](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

</div>

## Manutenibilidade (Dupla 3)

### Resultado atualizado

A revisão realizada em 15/11/2026 apresentava uma inspeção qualitativa e correções no procedimento de avaliação. Naquele momento, ainda não havia métricas do SonarCloud disponíveis para os sete arquivos completos, portanto, essa característica permanecia sem um julgamento conclusivo.

Entretanto, com a nova coleta realizada em 20/11/2026, foi possível reunir dados suficientes para estabelecer uma conclusão sobre a manutenibilidade do software. Os resultados obtidos estão disponíveis na aba [Coleta de Dados](../fase-4/coleta-de-dados.md).

### Cálculo das métricas, notas e julgamento

A coleta realizada em 20/11/2026, referente à versão `32.6.10` e ao commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, avaliou recortes específicos de funções. A comparação apresentada a seguir utiliza as [fórmulas definidas na Fase 2](../fase-2/metricas.md#manutenibilidade-dupla-3) e os [critérios de julgamento e pontuação](../fase-2/niveis-e-julgamento.md#manutenibilidade-dupla-3).

A correspondência entre os níveis de julgamento e as notas foi estabelecida da seguinte forma: Adequado = 5, Atenção = 3 e Crítico = 1. Além disso, a regra de agregação do objetivo G3 foi acrescentada após a coleta, com o propósito de completar a pontuação, preservando as faixas de classificação originalmente estabelecidas.

Para as Q3.1 e Q3.2, para ter uma nota geral para cada parte do escopo, foi feita uma média de complexidade cognitiva para cada função relacionada ao escopo e um média das médias. 

| Questão / Métrica | Fórmula aplicada | Resultado | Critério atingido da Fase 2 | Nota (1–5) |
| --- | --- | ---: | --- | ---: |
| **Q3.1 — Importação / M3.1** | `C / F = 28,474861 / 4` | **7,11871525** | **Adequado:** `M3.1 <= 10` | **5** |
| **Q3.2 — Rótulos / M3.1** | `C / F = 34,260286 / 4` | **8,5650715** | **Adequado:** `M3.1 <= 10` | **5** |
| **Q3.3 — Exportação / M3.2** | `100 × Ld / Lt = 100 × 28 / 2846` | **0,983837%** | **Adequado:** `M3.2 <= 5%` | **5** |

### Pontuação do objetivo de Manutenibilidade (G3)

> **Nota de G3 nos recortes históricos = `mínimo(Q3.1, Q3.2, Q3.3) = mínimo(5, 5, 5) = 5` — Adequado.**

Essa agregação indica que todos os recortes avaliados atenderam aos critérios estabelecidos para o nível adequado de manutenibilidade. Entretanto, é importante destacar que os resultados representam apenas as funções selecionadas para análise, não sendo possível generalizar essa classificação para todo o código-fonte do draw.io.

Além disso, embora os resultados estejam dentro dos limites estabelecidos, a complexidade observada na edição de rótulos foi a maior entre os recortes avaliados. Esse aspecto merece atenção em futuras manutenções, especialmente devido à relação entre a implementação-base e suas redefinições.

### Interpretação das questões e hipóteses

| Questão | Interpretação dos resultados históricos | Situação da hipótese no recorte histórico |
| --- | --- | --- |
| **Q3.1** | O resultado de 7,11871525 indica um nível de complexidade dentro dos limites estabelecidos como adequados pelas métricas. Entretanto, esse resultado não garante que todas as funções de importação apresentem baixa complexidade. | **H3.1 confirmada:** o resultado é inferior a 10. |
| **Q3.2** | O resultado de 8,5650715 atende ao limite estabelecido para o nível adequado, embora represente a maior complexidade entre os recortes analisados. A inspeção qualitativa também identificou dependências entre a implementação-base e suas redefinições. | **H3.2 confirmada no recorte medido:** o resultado é inferior a 10. |
| **Q3.3** | O percentual de duplicação de 0,983837% demonstra que a quantidade de código duplicado no recorte avaliado está abaixo do limite de 5%, atendendo ao critério estabelecido. | **H3.3 atendida:** o resultado é inferior a 5%. |

### Sugestões de melhoria ao draw.io

- **Documentar as redefinições na edição de rótulos:** explicitar a relação entre `mxCellEditor.js` e as redefinições presentes em `Graph.js`, incluindo a aplicação do texto e a integração da sanitização. Essa documentação facilitaria a compreensão do comportamento efetivo do sistema e o acompanhamento das responsabilidades distribuídas entre os arquivos.

- **Proteger os fluxos durante refatorações:** implementar testes de regressão para os processos de leitura e conversão XML, confirmação e cancelamento de rótulos e geração de arquivos PNG, PDF e SVG, considerando os caminhos efetivamente implementados. Essa medida visa reduzir o risco de introdução de falhas durante alterações nas responsabilidades distribuídas entre as diferentes camadas do sistema.

- **Investigar a duplicação antes de consolidar as exportações:** inspecionar os blocos identificados como duplicados e analisar suas diferenças de implementação entre os formatos de exportação antes de considerar a extração de rotinas compartilhadas. O baixo percentual de duplicação observado historicamente não justifica, isoladamente, uma refatoração ampla.

### Conclusão

Com base nos resultados obtidos na coleta de 20/11/2026, a característica de **Manutenibilidade recebeu nota 5 (Adequado)** nos recortes históricos avaliados. Os resultados demonstram que as funções selecionadas para análise atenderam aos limites estabelecidos na Fase 2, tanto em relação à complexidade cognitiva quanto à duplicidade de código.

Entre os aspectos avaliados, a edição de rótulos apresentou o maior índice de complexidade, embora ainda esteja dentro do limite considerado adequado. Esse resultado, associado à inspeção qualitativa, evidencia a importância de documentar melhor as relações entre a implementação-base e suas redefinições, facilitando futuras intervenções e reduzindo o esforço necessário para compreender o comportamento do código.

Em relação à exportação, o percentual de duplicidade encontrado foi consideravelmente inferior ao limite estabelecido, indicando que não há, nos recortes analisados, evidências quantitativas que justifiquem uma refatoração ampla com o objetivo exclusivo de eliminar código duplicado. Ainda assim, recomenda-se a investigação dos blocos identificados e a adoção de testes de regressão para preservar o comportamento existente durante futuras modificações.

Portanto, **os resultados sustentam uma avaliação adequada da manutenibilidade nos recortes selecionados**, indicando que o software apresenta condições satisfatórias para manutenção sob os critérios adotados neste estudo. Contudo, essa conclusão deve ser interpretada considerando as limitações do escopo da coleta, uma vez que a análise foi realizada sobre funções específicas e não representa uma avaliação integral de todo o código-fonte do draw.io. 
