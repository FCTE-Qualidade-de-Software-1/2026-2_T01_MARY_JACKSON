# Coleta de dados

Esta página documenta a execução prática e a coleta de dados brutos realizados na versão `32.6.10` do draw.io (repositório `H3ytt0r10/drawio` e imagem oficial `jgraph/drawio:32.6.10`).

## Segurança (Dupla 1 — Objetivo G1)

- **Versão avaliada:** draw.io release `32.6.10` (`H3ytt0r10/drawio`, commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, e imagem oficial `jgraph/drawio:32.6.10`).
- **Ambiente de execução e limitação:** Contêiner Docker estático (`httpd:alpine`) para os testes de cliente (`Q1.1`, `Q1.2` e `Q1.5`) — registrando-se como limitação da primeira rodada o vínculo padrão em `0.0.0.0:8080`, corrigido para `127.0.0.1:8080` nos casos complementares (`TD-08` e `TD-09`) — e contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente ao *loopback* (`127.0.0.1:8080:8080`) para validação do *servlet* `/proxy` (`Q1.3`), além de sessão anônima sem rede externa, VS Code e `curl.exe`.
- **Dados brutos (CSV):** armazenados em `dados/avaliacao/seguranca/` (`resultados_dinamicos.csv` e `inspecao_estatica.csv`).

### Testes dinâmicos de penetração (M1.1 e M1.3)

Em conformidade com as diretrizes de divulgação responsável (protocolo 5.2.4), os arquivos XML utilizados nos testes foram executados exclusivamente em diretório temporário local e descartados imediatamente após a coleta. Nenhum *payload* literal ou comando de ataque é publicado neste repositório, registrando-se apenas a descrição funcional de cada cenário e o resultado observado.

| ID | Questão / Métrica | Descrição Funcional do Caso de Teste | Comportamento Observado | Status |
| --- | --- | --- | --- | --- |
| **TD-01** | Q1.1 (M1.1) — Importação XML | Importação de diagrama `.drawio` contendo tag de script embutida no atributo de texto de uma célula (`html=1`). | Forma importada sem conteúdo textual; tag de script removida durante o *parsing* sem disparo de alerta. | **Bloqueado** |
| **TD-02** | Q1.2 (M1.1) — Rótulos HTML *(ref. CVE-2026-46642)* | Abertura de diagrama com célula `html=1` contendo tag de imagem e manipulador de evento de erro inline. | Exibição apenas do ícone nativo de imagem quebrada; manipulador de evento inline neutralizado pela sanitização. | **Bloqueado** |
| **TD-03** | Q1.3 (M1.1) — Proxy / Servidor Java | Requisição HTTP `GET` ao endpoint `/proxy` no servidor Tomcat tentando acessar arquivo local do sistema operacional via esquema de arquivo. | `ProxyServlet` ativo retornou `HTTP/1.1 404` com `Content-Length: 0` por bloqueio preventivo padrão (`ENABLE_DRAWIO_PROXY` desabilitado em `ProxyServlet.java:74-76`). | **Bloqueado** |
| **TD-04** | Q1.3 (M1.1) — Proxy / Servidor Java | Requisição HTTP `GET` ao endpoint `/proxy` no servidor Tomcat tentando acessar o descritor interno `WEB-INF/web.xml` via endereço local. | `ProxyServlet` ativo retornou `HTTP/1.1 404` com `Content-Length: 0` sem exposição de configurações internas do servidor. | **Bloqueado** |
| **TD-05** | Q1.5 (M1.3) — Bypass 1 *(ref. CVE-2026-58504)* | Célula com `html=1` contendo elemento vetorial SVG aninhado e manipulador de evento de carregamento inline. | Elemento SVG e evento inline removidos; célula renderizada em branco. | **Bloqueado** |
| **TD-06** | Q1.5 (M1.3) — Bypass 2 *(ref. CVE-2026-58504)* | Célula bloqueada para edição (`html=1;editable=0`) contendo âncora com URI de execução de script. | Esquema de script removido; preservado apenas o texto seguro do rótulo bloqueado para edição. | **Bloqueado** |
| **TD-07** | Q1.5 (M1.3) — Bypass 3 *(ref. CVE-2026-58504)* | Célula com `html=1` contendo quadro embutido apontando para URI de execução de script. | Elemento de quadro embutido integralmente removido na renderização. | **Bloqueado** |
| **TD-08** | Q1.1 (M1.1) — Importação XML | Importação de diagrama `.drawio` contendo elemento vetorial SVG com manipulador de evento de carregamento inline (`html=1`). | Forma importada vazia sem disparo de alerta; elemento SVG removido durante o *parsing* de importação. | **Bloqueado** |
| **TD-09** | Q1.2 (M1.1) — Rótulos HTML *(ref. CVE-2026-46642 / 58504)* | Abertura de diagrama contendo célula irmã regular e célula não editável (`html=1;editable=0`) com imagem e manipulador de evento de erro inline. | Célula irmã renderizada normalmente e célula `editable=0` exibindo apenas o ícone de imagem quebrada, sem execução de script. | **Bloqueado** |

### Inspeção estática de sanitização (M1.2 / Q1.4)

A varredura por `getLabelValue` nos arquivos `Format.js`, `Graph.js` e `Editor.js` identificou **9 ocorrências totais**. Adotou-se como critério de contagem contabilizar cada ponto de chamada onde o valor retornado é inserido ou avaliado no DOM, excluindo-se a definição base do método (`Graph.js:976`), que corresponde ao local onde a proteção é implementada, bem como comentários e verificações puramente lógicas sem manipulação de DOM:

- **5 ocorrências descartadas:**
  * `Format.js` (linha `5678`): comentário explicativo de código.
  * `Graph.js` (linhas `976` e `978`): definição base de `this.cellRenderer.getLabelValue` e chamada interna ao protótipo pai (onde `mxUtils.htmlEntities` ou `sanitizeLabel`/`DOMPurify` é aplicado conforme `isHtmlLabel`).
  * `Editor.js` (linhas `5374` e `5494`): verificações booleanas via `Editor.containsMath` para cálculo de dimensões sem inserção no DOM.
- **4 trechos válidos (`Pt = 4`) e protegidos (`Pp = 4`):**

| Arquivo | Linha | Fluxo de Renderização / Medição | Mecanismo de Proteção Identificado | Status |
| --- | --- | --- | --- | --- |
| `Format.js` | `5683` | Atribuição do rótulo ao `.innerHTML` em `canConvertHtmlToSvg` *(vetor central da CVE-2026-58504)* | Executa exclusivamente quando `html=1` está ativo, garantindo passagem prévia pelo `DOMPurify` dentro de `getLabelValue`. | **Protegido** |
| `Graph.js` | `36334` | Medição de fluxo de texto como HTML | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.isHtmlLabel(cell)` (rótulos HTML já vêm sanitizados de `getLabelValue`). | **Protegido** |
| `Graph.js` | `36601` | Preparação de rótulo com quebras de linha HTML para cálculo de fonte (`computeAutosizeTextFontSize`) | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.isHtmlLabel(cell)`. | **Protegido** |
| `Graph.js` | `50962` | Medição de fluxo HTML no *live preview* de redimensionamento | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.graph.isHtmlLabel(this.state.cell)`. | **Protegido** |

## Eficiência de desempenho (Dupla 2)

- **Versão avaliada:** draw.io release `32.6.10` (repositório `H3ytt0r10/drawio`, commit `c72c9a9`).
- **Ambiente de execução:** servidor HTTP estático local (`python -m http.server`) servindo `src/main/webapp`, Google Chrome 157.0.8103.79 em Windows 11, Intel Core i5-1235U e 16 GB de RAM, conforme o [plano de avaliação](index.md#eficiencia-de-desempenho-dupla-2).
- **Execução:** coleta automatizada pelo script `coletar.py` em 14/11/2026, das 19h06 às 19h47, com 52% da memória em uso no início. O porte de 50 formas foi coletado novamente das 20h18 às 20h21, nas mesmas condições, depois que se constatou que a carga desse porte havia sido alterada durante o piloto manual (ver [Piloto](index.md#piloto)); os valores abaixo são os da nova coleta. No total, são 125 gravações (5 portes, 5 operações e 5 tentativas), sem nenhuma falha de execução e sem tentativas descartadas.
- **Dados brutos (CSV):** `dados/avaliacao/eficiencia/brutos/tentativas.csv`, mantido no Git, com uma linha por gravação. Os valores foram extraídos pelo script `ler_traces.py`, segundo a [leitura das medidas](index.md#leitura-das-medidas).
- **Traces e integridade:** os 125 traces oficiais e os 14 dos pilotos são preservados em dois pacotes externos, com os caminhos originais de `dados/avaliacao/eficiencia/brutos/`. O acesso e a restauração estão documentados em `dados/avaliacao/eficiencia/README.md`, e os hashes, em `dados/avaliacao/eficiencia/SHA256SUMS.txt`. Os pacotes estão disponíveis na [pasta de evidências no Google Drive](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

### Tempo das operações (M2.1, M2.3 e M2.4)

Mediana das cinco tentativas, em ms, com o menor e o maior valor entre parênteses.

| Operação | 50 formas | 300 formas | 1.000 formas | 2.000 formas | 5.000 formas |
| --- | --- | --- | --- | --- | --- |
| M2.1 Abrir | 74 (51 a 90) | 160 (120 a 170) | 337 (316 a 343) | 580 (568 a 586) | 1.398 (1.275 a 1.611) |
| M2.3 Rótulo | 38 (36 a 46) | 40 (39 a 44) | 64 (49 a 83) | 77 (72 a 78) | 171 (162 a 182) |
| M2.4 Exportar PNG | 93 (91 a 127) | 231 (225 a 237) | 592 (590 a 612) | 1.055 (1.044 a 1.072) | 2.843 (1.716 a 3.589) |
| M2.4 Exportar PDF | 178 (156 a 185) | 355 (325 a 402) | 966 (927 a 1.010) | 2.019 (1.871 a 2.039) | 6.946 (6.095 a 7.246) |
| M2.4 Exportar SVG | 442 (438 a 444) | 1.931 (1.848 a 2.290) | 11.911 (10.046 a 13.066) | 29.472 (28.608 a 40.056) | 113.646 (110.704 a 126.108) |

### Memória do editor (M2.2 e M2.5)

Heap JavaScript usado, mediana das cinco tentativas, em MiB, com o menor e o maior valor entre parênteses.

| Medida | 50 formas | 300 formas | 1.000 formas | 2.000 formas | 5.000 formas |
| --- | --- | --- | --- | --- | --- |
| M2.2 Heap 2 s após abrir | 42,4 (39,3 a 43,9) | 45,5 (44,0 a 47,1) | 55,1 (52,0 a 56,3) | 51,2 (51,1 a 55,5) | 85,9 (83,8 a 90,3) |
| M2.5 Pico na exportação PNG | 38,1 (38,0 a 38,1) | 40,9 (40,9 a 41,0) | 52,5 (52,1 a 52,6) | 63,9 (62,6 a 66,2) | 90,9 (89,5 a 91,0) |
| M2.5 Pico na exportação PDF | 38,7 (38,4 a 38,7) | 43,8 (43,8 a 43,9) | 62,6 (59,8 a 62,8) | 91,9 (91,6 a 94,1) | 134,8 (134,2 a 134,8) |
| M2.5 Pico na exportação SVG | 40,4 (39,8 a 40,6) | 48,9 (48,8 a 55,8) | 120,6 (92,5 a 123,5) | 120,7 (110,7 a 140,8) | 381,9 (357,2 a 418,3) |

### Observações da coleta

- **Exportação SVG.** O tempo cresce muito mais rápido que o número de formas: de 442 ms com 50 formas para 113,6 s com 5.000, cerca de 260 vezes para 100 vezes mais formas. Os traces mostram que, nessa exportação, o draw.io converte os rótulos HTML em imagens, uma a uma (10.000 imagens geradas no porte de 5.000 formas).
- **Tentativas acima de duas vezes o limite candidato.** No SVG com 5.000 formas, as cinco tentativas passaram de 80 s (duas vezes o limite candidato de 40 s). No SVG com 2.000 formas, uma tentativa (40,1 s) passou de 34 s (duas vezes o limite de 17 s), e as outras quatro ficaram abaixo. Os valores medidos estão preservados no CSV; o tratamento como falha é feito na análise.
- **Exportação PDF.** Os valores medem a preparação da página de impressão pelo draw.io. O arquivo PDF é gerado pela impressão do navegador, que no piloto manual produziu um documento com cabeçalho do navegador, dividido em páginas e com formas cortadas na borda.
- **Dispersão.** A exportação PNG com 5.000 formas teve a maior variação relativa entre tentativas (1,7 a 3,6 s); nas demais operações, as cinco tentativas ficaram próximas entre si.
- **Memória.** O maior heap observado foi 418,3 MiB, no SVG com 5.000 formas. O heap após a abertura com 2.000 formas ficou ligeiramente abaixo do de 1.000 formas, o que é compatível com o momento da coleta de lixo do JavaScript.

### Validação dos arquivos exportados

Em 15/11/2026, o script `validar_exportacoes.py` exportou e salvou um arquivo de cada formato por porte e verificou cada um, conforme a [validação das exportações](index.md#validacao-das-exportacoes) do plano. O resultado está em `dados/avaliacao/eficiencia/brutos/exportados/validacao.csv`, e os arquivos, no pacote `eficiencia-exportacoes-2026-11-15.zip`, com publicação pelo grupo na [pasta de evidências](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

| Porte | PNG | SVG | PDF |
| --- | --- | --- | --- |
| 50 | Completo (7.962 x 62 px) | Completo (50 de 50 rótulos) | Abre; 10 páginas, 47 de 50 rótulos inteiros |
| 300 | Completo (7.962 x 562 px) | Completo (300 de 300 rótulos) | Abre; 10 páginas, 282 de 300 rótulos inteiros |
| 1.000 | Completo (7.962 x 1.962 px) | Completo (1.000 de 1.000 rótulos) | Abre; 20 páginas, 940 de 1.000 rótulos inteiros |
| 2.000 | Completo (7.962 x 3.962 px) | Completo (2.000 de 2.000 rótulos) | Abre; 40 páginas, 1.880 de 2.000 rótulos inteiros |
| 5.000 | Completo (7.962 x 9.962 px) | Não gerado | Abre; 100 páginas, 4.700 de 5.000 rótulos inteiros |

- **PNG e SVG.** Os arquivos gerados abrem e contêm o diagrama completo: as imagens PNG têm exatamente as dimensões da área das formas, e cada SVG traz todos os rótulos da carga.
- **PDF.** Todos os arquivos abrem, mas o diagrama é dividido em páginas tamanho carta, e as formas que caem na divisão entre páginas são cortadas. Em todos os portes, cerca de 6% dos rótulos não aparecem inteiros em nenhuma página. A medida confirma o que o piloto manual havia mostrado.
- **SVG com 5.000 formas.** O arquivo não foi gerado. Em quatro execuções, a exportação não concluiu: nas duas com a janela visível, o draw.io exibiu a mensagem "Error: Timeout"; nas duas sem janela, o diálogo de salvamento não apareceu em 5 e em 15 minutos. Na coleta, a mesma exportação chegou ao diálogo "Save as" nas cinco tentativas, em cerca de 2 minutos. A validação difere da coleta no caminho de salvamento (Download, em vez do seletor do navegador) e no estado da máquina, e esta avaliação não isolou a causa. O resultado indica que, nesse porte, a exportação SVG está no limite do que o draw.io consegue concluir.

O julgamento das medidas pelos níveis da Fase 2 está em [Análise dos dados e resultados](resultados.md).

## Manutenibilidade (Dupla 3)

- **Versão avaliada:** draw.io release `32.6.10` (`H3ytt0r10/drawio`). A campanha histórica utilizou o commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`; a nova inspeção informa o commit base `aacddaf44e6b4db468ef3f4f3e3bb56863f1d581`.
- **Ambiente de execução e limitação:** análise estática no fork do projeto, com SonarCloud na campanha histórica e inspeção local dos sete arquivos completos na revisão de 15/11/2026. Ainda não existem medidas SonarCloud coletadas para esse conjunto completo.
- **Dados e evidências:** [relatório consolidado das análises](evidencias/resultados-das-analises.md), preservado conforme o documento fornecido. Os CSVs anteriormente mencionados não estão disponíveis neste repositório; os scripts, manifestos e demais artefatos citados no relatório pertencem ao ambiente de origem.

### Verificação de duplicidade entre os códigos (Q3.3 e M3.2)

A métrica utiliza a razão entre as linhas duplicadas e o total de linhas do recorte de exportação PNG, PDF e SVG, multiplicada por 100. O resultado histórico disponível corresponde a recortes de funções, com cobertura parcial do fluxo de PDF:

| Componente | Número de linhas duplicadas | Número total de linhas | Porcentagem | Status histórico |
| --- | ---: | ---: | ---: | --- |
| Exportação PNG/PDF/SVG — recorte de 08/11/2026 | 28 | 2.846 | 0,983837% | Adequado |

Para o novo escopo, as linhas duplicadas e o percentual de duplicação ainda não foram coletados no SonarCloud. Assim, os zeros e os julgamentos anteriormente apresentados por arquivo foram retirados. O total dos sete arquivos inclui outras funcionalidades e não pode ser utilizado automaticamente como denominador da exportação. Também não se deve calcular a média simples dos percentuais individuais dos arquivos.

### Verificação da complexidade cognitiva das funções (Q3.1, Q3.2 e M3.1)

A complexidade cognitiva média deve ser calculada pela divisão da complexidade cognitiva total pela quantidade de funções de cada componente. A complexidade total de um arquivo não pode ser comparada diretamente às faixas de julgamento da média por função.

**Para as funções de rótulos: edição de texto e tratamento HTML**

O escopo inclui `src/main/webapp/js/diagramly/EditorUi.js`, `src/main/webapp/mxgraph/src/view/mxCellEditor.js`, `src/main/webapp/js/grapheditor/Graph.js` e `src/main/webapp/js/sanitizer/purify.min.js`.

| Arquivo | Complexidade cognitiva | Status |
| --- | --- | --- |
| `EditorUi.js` | Não coletada no novo escopo | Sem julgamento |
| `mxCellEditor.js` | Não coletada no novo escopo | Sem julgamento |
| `Graph.js` | Não coletada no novo escopo | Sem julgamento |
| `purify.min.js` | Não coletada no novo escopo | Sem julgamento |

O recorte histórico corrigido de rótulos registrou complexidade total de **1.057** e **116 funções**, com média de **9,112069 (Adequado)**. A média original de `9,512820512820513` foi invalidada por sobreposição de trechos. Esses números não representam os quatro arquivos completos.

**Para as funções de importação: abertura de arquivos locais `.drawio` e `.xml`**

O escopo inclui `src/main/webapp/js/diagramly/EditorUi.js`, `src/main/webapp/js/diagramly/App.js`, `src/main/webapp/js/grapheditor/Editor.js` e `src/main/webapp/mxgraph/src/io/mxCodec.js`. O caminho correto é `grapheditor/Editor.js`, distinto de `diagramly/Editor.js` utilizado anteriormente.

| Arquivo | Complexidade cognitiva | Status |
| --- | --- | --- |
| `EditorUi.js` | Não coletada no novo escopo | Sem julgamento |
| `App.js` | Não coletada no novo escopo | Sem julgamento |
| `Editor.js` (`grapheditor`) | Não coletada no novo escopo | Sem julgamento |
| `mxCodec.js` | Não coletada no novo escopo | Sem julgamento |

O recorte histórico de importação registrou complexidade total de **275** e **25 funções**, com média de **11,000000 (Atenção)**. Esses números não representam os quatro arquivos completos.

### Observações e falhas da coleta

- **Necessidade de nova análise.** Os dados iniciais pareciam estranhos, especialmente os zeros de complexidade e duplicação em arquivos extensos. Por isso, foi necessário realizar uma nova análise do escopo e do procedimento.
- **Diferenças de escopo.** A campanha anterior utilizou 41 recortes e omitiu quatro arquivos das imagens. A revisão inventariou sete arquivos únicos completos e corrigiu a identificação de `Editor.js`.
- **Configuração da análise.** Além da falha de configuração relatada inicialmente, foi identificado risco de exclusão dos arquivos maiores. O relatório informa a preparação de configuração conjunta com limite de tamanho ampliado; isso ainda exige confirmação do processamento remoto e não comprova exclusão na campanha passada.
- **Validação local.** Segundo o relatório, os sete arquivos passaram em `node --check`. Isso verifica a sintaxe, sem comprovar funcionamento ou baixa complexidade. O inventário de linhas, tamanhos e os achados qualitativos estão no relatório consolidado.
- **Limites dos dados.** Ausência de coleta não equivale a zero. Os valores históricos pertencem aos recortes de 08/11/2026 e não classificam os sete arquivos completos. O novo escopo permanece sem julgamento quantitativo.

Os cálculos, os critérios de julgamento e os limites das conclusões estão em [Análise dos dados e resultados](resultados.md#manutenibilidade-dupla-3).
