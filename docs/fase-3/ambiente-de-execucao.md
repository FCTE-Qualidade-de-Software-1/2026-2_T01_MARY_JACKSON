## Segurança (Dupla 1)

Esta seção define o protocolo de coleta das métricas **M1.1 a M1.3** da [Fase 2](../fase-2/metricas.md), vinculadas ao objetivo global **G1** (Confidencialidade, Integridade e Resistência). Toda a avaliação é conduzida por um único avaliador, combinando inspeção estática de código-fonte (caixa-branca) e testes dinâmicos de penetração (caixa-preta) em ambiente local isolado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões restringem-se à versão avaliada, à configuração de implantação estática e ao modelo de ameaças definido.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | Contêiner Docker local (`httpd:alpine`) montando `src/main/webapp`, conforme o [guia do ambiente](ambiente-drawio.md), acessado em `http://localhost:8080`. |

### Ambiente e máquina do avaliador

| Item | Configuração |
| --- | --- |
| Processador | AMD Ryzen 3 2200G. |
| Memória RAM | 16 GB. |
| Armazenamento | SSD. |
| Placa de vídeo | AMD Radeon Vega 8 (integrada). |
| Sistema operacional | Windows 11 (64 bits). |
| Navegador | Microsoft Edge (64 bits). |
| Editor e terminal | Visual Studio Code (VS Code) e PowerShell (`curl.exe`) |
| Avaliador | Miquéias (Dupla 1) |

### Ferramentas

| Ferramenta | Uso |
| --- | --- |
| Docker (`httpd:alpine`) | Hospedagem isolada da aplicação web (`src/main/webapp`) e captura de logs de acesso HTTP (`docker logs`) durante os testes de requisição. |
| Visual Studio Code (VS Code) | Busca e rastreamento de fluxo de dados no código-fonte JavaScript (`Format.js`, `Graph.js` e `Editor.js`) para a M1.2, além da criação dos arquivos `.drawio` de teste. |
| Git | Clonagem do repositório customizado e verificação da integridade da versão (`VERSION` e hash do commit). |
| Navegador Web (janela anônima) | Importação e abertura dos diagramas adulterados em sessão limpa para observação visual e de execução no DOM (M1.1 e M1.3). |
| `curl.exe` (PowerShell) | Envio de requisições HTTP forjadas contra o endpoint `/proxy` para testes de *Path Traversal* (M1.1 / Q1.3). |

### Condições de execução

| Condição | Regra |
| --- | --- |
| Perfil do navegador | Janela anônima/convidado, sem extensões instaladas, sem histórico e sem outras abas abertas durante a execução. |
| Isolamento de rede | Instância servida exclusivamente em `localhost:8080`, sem conexão a serviços externos de armazenamento em nuvem. |
| Limpeza de estado | Cada caso dinâmico de abertura/importação é executado descartando o diagrama anterior ou recarregando a sessão limpa. |
| Divulgação responsável | Os arquivos `.drawio` contendo *payloads* maliciosos são criados em diretório temporário fora dos repositórios Git e excluídos imediatamente após a coleta, registrando-se apenas os resultados e evidências textuais/visuais. |

### Artefatos e vetores de teste

Os testes dinâmicos baseiam-se em vulnerabilidades históricas documentadas para o draw.io (XSS via importação XML, XSS em rótulos HTML — ref. CVE-2026-46642, *Path Traversal* no proxy e variações de evasão — ref. CVE-2026-58504).

| ID | Questão / Métrica | Artefato ou Requisição | Vetor Empregado | Mecanismo Avaliado |
| --- | --- | --- | --- | --- |
| **TD-01** | Q1.1 (M1.1) | `teste_q1_1.drawio` | Atributo `value="&lt;script&gt;alert('XSS_Q1_1')&lt;/script&gt;"` com `html=1` importado via menu. | Sanitização na importação de arquivos XML. |
| **TD-02** | Q1.2 (M1.1) | `teste_q1_2.drawio` | Atributo `value="&lt;img src=x onerror=alert('XSS_Q1_2')&gt;"` em célula de texto (`html=1`). | Remoção de manipuladores de evento (`onerror`) em rótulos HTML. |
| **TD-03** | Q1.3 (M1.1) | Requisição HTTP `GET` | `http://localhost:8080/proxy?url=file:///etc/passwd` | Bloqueio de leitura de arquivos locais via proxy. |
| **TD-04** | Q1.3 (M1.1) | Requisição HTTP `GET` | `http://localhost:8080/proxy?url=http://127.0.0.1:8080/../../WEB-INF/web.xml` | Bloqueio de travessia de diretório (*Path Traversal*). |
| **TD-05** | Q1.5 (M1.3) | `teste_m1_3_bypasses.drawio` (Célula 1) | Tag SVG aninhada: `&lt;svg onload=alert('Bypass_1')&gt;&lt;/svg&gt;` (`html=1`). | Filtragem de elementos SVG e eventos `onload`. |
| **TD-06** | Q1.5 (M1.3) | `teste_m1_3_bypasses.drawio` (Célula 2) | Âncora `&lt;a href="javascript:alert('Bypass_2')"&gt;Clique&lt;/a&gt;` com `html=1;editable=0`. | Neutralização de URIs `javascript:` em elementos não editáveis. |
| **TD-07** | Q1.5 (M1.3) | `teste_m1_3_bypasses.drawio` (Célula 3) | Quadro embutido `&lt;iframe src="javascript:alert('Bypass_3')"&gt;&lt;/iframe&gt;` (`html=1`). | Remoção de tags `<iframe>` na renderização de rótulos. |

### Procedimento

A coleta é dividida em quatro blocos sequenciais:

**Bloco A: Inspeção estática de sanitização (M1.2 / Q1.4)**

1. Abrir o diretório do repositório `H3ytt0r10/drawio` (versão `32.6.10`) no VS Code.
2. Localizar os arquivos `Format.js`, `Graph.js` e `Editor.js` dentro de `src/main/webapp/js/`.
3. Pesquisar todas as ocorrências da chamada `getLabelValue` nos três arquivos.
4. Descartar comentários, declarações de protótipo e chamadas usadas exclusivamente para verificações booleanas ou métricas sem inserção no DOM, obtendo o conjunto de trechos válidos ($P_t$).
5. Rastrear o fluxo de dados de cada trecho válido até a renderização/medição HTML, verificando a aplicação de `Graph.sanitizeHtml` (via `sanitizeLabel`/DOMPurify) ou `mxUtils.htmlEntities` antes do uso no DOM, contabilizando os trechos protegidos ($P_p$).

**Bloco B: Testes dinâmicos base — importação e rótulos (M1.1 / Q1.1 e Q1.2)**

1. Iniciar o contêiner `drawio-teste` e abrir `http://localhost:8080` em janela anônima.
2. Acionar **Arquivo > Importar de > Dispositivo**, selecionar `teste_q1_1.drawio` e observar se há execução de alerta ou renderização limpa da forma.
3. Acionar **Arquivo > Abrir de > Dispositivo**, descartar o diagrama anterior, selecionar `teste_q1_2.drawio` e verificar se o evento `onerror` é neutralizado.

**Bloco C: Testes dinâmicos base — proxy e Path Traversal (M1.1 / Q1.3)**

1. No PowerShell, executar `curl.exe -i` contra os dois endpoints de teste (`TD-03` e `TD-04`).
2. Registrar o código de status HTTP retornado (esperando `400`, `403` ou `404` sem corpo de arquivo interno) e confirmar o registro no servidor via `docker logs drawio-teste`.

**Bloco D: Testes de resistência e variações de bypass (M1.3 / Q1.5)**

1. Na janela anônima do draw.io, acionar **Arquivo > Abrir de > Dispositivo** e carregar `teste_m1_3_bypasses.drawio`.
2. Verificar a ausência de execução automática das células 1 (`<svg onload>`) e 3 (`<iframe>`).
3. Clicar diretamente sobre o rótulo `"Clique"` da célula 2 para confirmar a remoção do esquema `javascript:`.
4. Excluir o diretório temporário contendo os arquivos `.drawio` de teste e encerrar o contêiner.

### Critérios de leitura e registro das medidas

| Métrica | Entrada / Escopo | Critério de Sucesso (Protegido / Bloqueado) | Valor Registrado |
| --- | --- | --- | --- |
| **M1.1** | $C_t = 4$ casos base (`TD-01` a `TD-04`). | Ausência de disparo de `alert()`, ausência de injeção de script ativo no DOM e rejeição HTTP (`403`/`404`) sem vazamento de arquivos. | $M1.1 = (C_b / C_t) \times 100$, em $\%$. |
| **M1.2** | $P_t$ trechos válidos de renderização/medição HTML em `Format.js`, `Graph.js` e `Editor.js`. | Presença comprovada de sanitização (`DOMPurify`) ou escape (`mxUtils.htmlEntities`) em todos os ramos antes da inserção no DOM. | $M1.2 = (P_p / P_t) \times 100$, em $\%$. |
| **M1.3** | $W_t = 3$ variações de evasão (`TD-05` a `TD-07`). | Neutralização integral das tags/atributos ofuscados ou combinados com estilos (`editable=0`), sem execução de código. | $M1.3 = (W_b / W_t) \times 100$, em $\%$. |

### Critérios de bloqueio, falhas e descartes

Cada caso dinâmico é classificado como **bloqueado** quando o vetor é removido ou escapado pela aplicação sem execução de JavaScript e sem exposição de recursos locais. Considera-se **falha de segurança** (vulnerabilidade explorável) qualquer execução de caixa de diálogo (`alert`), injeção de elemento ativo malicioso no DOM ou retorno `HTTP 200` com conteúdo de arquivo do sistema/servidor. Caso ocorra erro operacional externo ao sistema avaliado (como falha de inicialização do contêiner ou cache residual de sessão), o teste é **descartado**, o ambiente é reiniciado e a execução é repetida.

### Registro dos dados

Os registros da coleta ficam armazenados em `dados/avaliacao/seguranca/`:

| Caminho | Conteúdo |
| --- | --- |
| `brutos/resultados_dinamicos.csv` | Registro de cada vetor executado (`TD-01` a `TD-07`) com status e comportamento observado. |
| `brutos/inspecao_estatica.csv` | Mapeamento das ocorrências de `getLabelValue` por arquivo, linha, classificação ($P_t$) e proteção ($P_p$). |
| `brutos/evidencias_seguranca_G1.txt` | Saída consolidada do terminal contendo versão, inspeção do Docker, respostas HTTP do `curl` e logs do Apache. |

Colunas de `resultados_dinamicos.csv`: `data`, `id_teste`, `questao`, `metrica`, `vetor`, `tipo_analise`, `status_http_ou_visual`, `resultado` (`bloqueado`, `falha` ou `descartado`), `observacao`.

### Verificação prévia (Piloto)

Antes da execução formal dos vetores, realiza-se uma verificação prévia do ambiente para:

- confirmar a leitura do arquivo `VERSION` (`32.6.10`) e o mapeamento do volume `src/main/webapp` no contêiner `drawio-teste`;
- validar o carregamento da interface web em `http://localhost:8080` sem dependências externas;
- confirmar a arquitetura estática da implantação (servidor Apache sem *servlet* Java `/proxy` ativo) e a sintaxe de busca no VS Code.