# Coleta de dados

Esta página documenta a execução prática e a coleta de dados brutos realizados na versão `32.6.10` do draw.io (repositório `H3ytt0r10/drawio`).

## Segurança (Dupla 1 — Objetivo G1)

- **Versão avaliada:** draw.io release `32.6.10` (repositório `H3ytt0r10/drawio`)
- **Ambiente de execução:** Contêiner Docker isolado (`httpd:alpine` em `localhost:8080`), sessão anônima sem acesso à rede externa, VS Code e `curl`.
- **Dados brutos (CSV):** armazenados em `dados/avaliacao/seguranca/` (`resultados_dinamicos.csv` e `inspecao_estatica.csv`).

### Testes dinâmicos de penetração (M1.1 e M1.3)

Em conformidade com as diretrizes de divulgação responsável, os arquivos XML utilizados nos testes foram executados exclusivamente em ambiente local isolado e descartados após a coleta, sem publicação no repositório.

| ID | Questão / Métrica | Vetor / Caso de Teste Executado | Comportamento Observado | Status |
| --- | --- | --- | --- | --- |
| **TD-01** | Q1.1 (M1.1) — Importação XML | Arquivo `.drawio` contendo tag `<script>` no atributo `value` de um `<mxCell>` importado via dispositivo. | Forma importada sem conteúdo textual; tag `<script>` removida durante o *parsing* sem disparo de alerta. | **Bloqueado** |
| **TD-02** | Q1.2 (M1.1) — Rótulos HTML *(ref. CVE-2026-46642)* | Célula com estilo `html=1` e rótulo contendo `<img src=x onerror=...>`. | Exibição apenas do ícone nativo de imagem quebrada; manipulador `onerror` neutralizado pela sanitização. | **Bloqueado** |
| **TD-03** | Q1.3 (M1.1) — Proxy / Path Traversal | Requisição HTTP `GET /proxy?url=file:///etc/passwd` enviada via `curl`. | Resposta `HTTP/1.1 404 Not Found` sem leitura de arquivos do sistema operacional. | **Bloqueado** |
| **TD-04** | Q1.3 (M1.1) — Proxy / Path Traversal | Requisição HTTP `GET /proxy?url=http://127.0.0.1:8080/../../WEB-INF/web.xml` via `curl`. | Resposta `HTTP/1.1 404 Not Found` sem exposição de configurações internas. | **Bloqueado** |
| **TD-05** | Q1.5 (M1.3) — Bypass 1 *(ref. CVE-2026-58504)* | Célula com `html=1` contendo tag `<svg onload=...>`. | Tag `<svg>` e evento `onload` removidos; célula renderizada em branco. | **Bloqueado** |
| **TD-06** | Q1.5 (M1.3) — Bypass 2 *(ref. CVE-2026-58504)* | Célula com `html=1;editable=0` contendo âncora `<a href="javascript:...">Clique</a>`. | Esquema `javascript:` removido; preservado apenas o texto seguro `"Clique"` bloqueado para edição. | **Bloqueado** |
| **TD-07** | Q1.5 (M1.3) — Bypass 3 *(ref. CVE-2026-58504)* | Célula com `html=1` contendo quadro embutido `<iframe src="javascript:...">`. | Elemento `<iframe>` integralmente removido na renderização. | **Bloqueado** |

### Inspeção estática de sanitização (M1.2 / Q1.4)

A varredura pela chamada `getLabelValue` nos arquivos `Format.js`, `Graph.js` e `Editor.js` identificou **9 ocorrências totais**. Após triagem de fluxo de dados até o DOM:

- **6 ocorrências descartadas:**
    * `Format.js` (linha `5678`): comentário explicativo de código.
    * `Format.js` (linha `5683`): verificação booleana via `mxUtils.canConvertHtmlToSvg` sem inserção no DOM.
    * `Graph.js` (linhas `976` e `978`): definição base de `this.cellRenderer.getLabelValue` e chamada ao protótipo pai (que aplica `mxUtils.htmlEntities` ou `sanitizeLabel`/`DOMPurify` quando `isHtmlLabel` está ativo).
    * `Editor.js` (linhas `5374` e `5494`): verificações booleanas via `Editor.containsMath` para cálculo de dimensões.
- **3 trechos válidos (`Pt = 3`) e protegidos (`Pp = 3`):**

| Arquivo | Linha | Fluxo de Renderização / Medição | Mecanismo de Proteção Identificado | Status |
| --- | --- | --- | --- | --- |
| `Graph.js` | `36334` | Medição de fluxo de texto como HTML | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.isHtmlLabel(cell)` (rótulos HTML já vêm sanitizados de `getLabelValue`). | **Protegido** |
| `Graph.js` | `36601` | Preparação de rótulo com `<br>` para cálculo de fonte (`computeAutosizeTextFontSize`) | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.isHtmlLabel(cell)`. | **Protegido** |
| `Graph.js` | `50962` | Medição de fluxo HTML no *live preview* de redimensionamento | Aplica `mxUtils.htmlEntities(value, false)` quando `!this.graph.isHtmlLabel(this.state.cell)`. | **Protegido** |

## Eficiência de desempenho (Dupla 2)

*Espaço reservado para os dados coletados pela Dupla 2.*

## Manutenibilidade (Dupla 3)

*Espaço reservado para os dados coletados pela Dupla 3.*