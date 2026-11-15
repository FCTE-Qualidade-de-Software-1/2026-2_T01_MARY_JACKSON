# Coleta de dados

Esta página documenta a execução prática e a coleta de dados brutos realizados na versão `32.6.10` do draw.io (repositório `H3ytt0r10/drawio` e imagem oficial `jgraph/drawio:32.6.10`).

## Segurança (Dupla 1 — Objetivo G1)

- **Versão avaliada:** draw.io release `32.6.10` (`H3ytt0r10/drawio`, commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, e imagem oficial `jgraph/drawio:32.6.10`).
- **Ambiente de execução e limitação:** Contêiner Docker estático (`httpd:alpine`) para os testes de cliente (`Q1.1`, `Q1.2` e `Q1.5`) — registrando-se como limitação da coleta inicial o vínculo padrão em `0.0.0.0:8080` — e contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente ao *loopback* (`127.0.0.1:8080:8080`) para validação do *servlet* `/proxy` (`Q1.3`), além de sessão anônima sem rede externa, VS Code e `curl.exe`.
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

O julgamento das medidas pelos níveis da Fase 2 está em [Análise dos dados e resultados](resultados.md).

## Manutenibilidade (Dupla 3)

- **Versão avaliada:** draw.io release `32.6.10` (`H3ytt0r10/drawio`, commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`).
- **Ambiente de execução e limitação:**  — Foi utilizado o sonarcloud dentro de um fork do projeto original, como descrito na versão utilizada para responder todas as questões relacionadas a manutenibilidade (Q3.1 a Q3.3).
- **Dados brutos (CSV):** armazenados em `dados/avaliacao/manutenibilidade/` (`resultados_dinamicos.csv` e `inspecao_estatica.csv`).


### Verificação de duplicidade entre dos códigos ( Q3.3 e M3.2)

Foi feito um relátorio encima dos arquivos EditorUI.js(src/main/webapp/js/diagramly/EditorUi.js),  Editor.js (src/main/webapp/js/diagramly/Editor.js), Graph (src/main/webapp/js/grapheditor/Graph.js) e  Menus.js (src/main/webapp/js/diagramly/Menus.js), para o calculo da porcentagem foi feita a razão entre o número de linhas duplicadas e o numero total de linhas do arquivo, o resultado encontrado foi: 

| Arquivo | Número de linhas duplicadas | Número total | Porcentagem | Status |
| --- | --- | --- | --- | --- |
|EditorUI.js| 0 |  43510   |  0%  |  Adequado  |
|Editor.js| 0  | 15362 | 0% | Adequado |
|Graph|  0 |  54775 |   0% | Adequado |
| Menus.js|  0 |  7421    |  0%|  Adequado|


### Verificação da complexidade cognitiva das funcções ( Q3.1, Q3.2 e M3.2)


Foi feito um relátorio encima dos arquivos relacionados as funções de Rótulos: edição de texto e tratamento HTML: EditorUI.js(src/main/webapp/js/diagramly/EditorUi.js),  mxCellEditor.js (src/main/webapp/mxgraph/src/view/mxCellEditor.js), Graph (src/main/webapp/js/grapheditor/Graph.js) e  purify.min.js (src/main/webapp/js/sanitizer/purify.min.js). Foi feita tambem a análise dos codigos relacionados as funções de Importação: abrir arquivos locais .drawio e .xml: EditorUI.js(src/main/webapp/js/diagramly/EditorUi.js), App.js (src/main/webapp/js/diagramly/App.js),Editor.js (src/main/webapp/js/grapheditor/Editor.js) e mxCodec.js (src/main/webapp/mxgraph/src/io/mxCodec.js). O resultado encontrado foi:

**Para as funções de Rótulos: edição de texto e tratamento HTML**

| Arquivo | Complexidade cognitiva |  Status |
| --- | --- | --- |
|EditorUI.js| 0 |    Adequado  |
| mxCellEditor| 197  | Crítico |
|Graph|  0 | Adequado |
| purify.min.js|  0 | Adequado|

**Para as funções de  Importação: abrir arquivos locais**

| Arquivo | Complexidade cognitiva |  Status |
| --- | --- | --- |
|EditorUI.js| 0 |    Adequado  |
| App.js| 3547 | Crítico |
|Editor.js|  1116 | Crítico  |
| mxCodec.js  |  119 | Crítico |
