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

*Espaço reservado para os dados coletados pela Dupla 2.*

## Manutenibilidade (Dupla 3)

*Espaço reservado para os dados coletados pela Dupla 3.*