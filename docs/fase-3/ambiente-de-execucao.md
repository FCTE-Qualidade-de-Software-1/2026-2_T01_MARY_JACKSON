## Segurança (Dupla 1)

Esta seção define o protocolo de coleta das métricas **M1.1 a M1.3** da [Fase 2](../fase-2/metricas.md), vinculadas ao objetivo global **G1** (Confidencialidade, Integridade e Resistência). Toda a avaliação é conduzida por um único avaliador, combinando inspeção estática de código-fonte (caixa-branca) e testes dinâmicos de penetração (caixa-preta) em ambiente local isolado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões restringem-se à versão avaliada, à configuração de implantação local e ao modelo de ameaças definido.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio) e da imagem oficial `jgraph/drawio:32.6.10`. |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | Contêiner Docker estático (`httpd:alpine`) montando `src/main/webapp` para os testes de interface web (`Q1.1`, `Q1.2` e `Q1.5`), e contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente a `127.0.0.1:8080:8080` para o teste do *servlet* `/proxy` (`Q1.3`). |

### Ambiente e máquina do avaliador

| Item | Configuração |
| --- | --- |
| Processador | AMD Ryzen 3 2200G. |
| Memória RAM | 16 GB. |
| Armazenamento | SSD. |
| Placa de vídeo | AMD Radeon Vega 8 (integrada). |
| Sistema operacional | Windows 11 (64 bits). |
| Navegador | Microsoft Edge (64 bits). |
| Editor e terminal | Visual Studio Code (VS Code) e PowerShell (`curl.exe`). |
| Avaliador | Miquéias (Dupla 1). |

### Ferramentas

| Ferramenta | Uso |
| --- | --- |
| Docker (`httpd:alpine` e `jgraph/drawio:32.6.10`) | Hospedagem local da interface web (`src/main/webapp`) para os testes de cliente e execução do servidor Java (Tomcat) com `ProxyServlet` ativo para validação do endpoint `/proxy`. |
| Visual Studio Code (VS Code) | Busca e rastreamento de fluxo de dados no código-fonte (`Format.js`, `Graph.js`, `Editor.js` e `ProxyServlet.java`) para M1.2 e auditoria de servidor, além da criação temporária dos arquivos `.drawio` de teste. |
| Git | Clonagem do repositório customizado e verificação da integridade da versão (`VERSION` e hash do commit). |
| Navegador Web (janela anônima) | Importação e abertura dos diagramas de teste em sessão limpa para observação visual e de execução no DOM (M1.1 e M1.3). |
| `curl.exe` (PowerShell) | Envio de requisições HTTP de teste contra o endpoint `/proxy` no servidor Tomcat para validação de *Path Traversal* e SSRF (M1.1 / Q1.3). |

### Condições de execução e limitações de ambiente

| Condição | Regra / Observação |
| --- | --- |
| Perfil do navegador | Janela anônima/convidado, sem extensões instaladas, sem histórico e sem outras abas abertas durante a execução. |
| Exposição de rede e vínculo de porta (limitação) | Na primeira rodada com `httpd:alpine` (`TD-01`, `TD-02` e `TD-05` a `TD-07`), a publicação padrão `-p 8080:80` vinculou o serviço em `0.0.0.0:8080` (acessível na rede local), o que fica registrado como limitação da coleta inicial. Na validação do servidor Java (`TD-03` e `TD-04`) e nos casos complementares (`TD-08` e `TD-09`), o mapeamento foi restrito exclusivamente à interface de *loopback* (`127.0.0.1:8080:8080` / `127.0.0.1:8080:80`). |
| Limpeza de estado | Cada caso dinâmico de abertura/importação é executado descartando o diagrama anterior ou recarregando a sessão limpa. |
| Divulgação responsável (protocolo 5.2.4) | Os arquivos `.drawio` contendo vetores de teste são criados em diretório temporário fora dos repositórios Git e excluídos imediatamente após a coleta. Nenhum *payload* literal ou comando de ataque é publicado no repositório, registrando-se apenas a descrição funcional de cada caso e o resultado observado. |

### Artefatos e casos de teste

Os testes dinâmicos baseiam-se em cenários de vulnerabilidades históricas documentadas para o draw.io (injeção de script via importação XML, XSS em rótulos HTML — ref. CVE-2026-46642, *Path Traversal*/SSRF no *servlet* `/proxy` e variações de evasão em elementos não editáveis — ref. CVE-2026-58504), totalizando **9 casos dinâmicos** (ao menos 2 casos por componente em `M1.1` e 3 variações em `M1.3`).

| ID | Questão / Métrica | Artefato ou Requisição | Cenário Testado | Mecanismo Avaliado |
| --- | --- | --- | --- | --- |
| **TD-01** | Q1.1 (M1.1) | Arquivo `.drawio` temporário | Importação de diagrama contendo tag de script embutida no atributo de texto de uma célula (`html=1`). | Sanitização na importação de arquivos XML. |
| **TD-02** | Q1.2 (M1.1) | Arquivo `.drawio` temporário | Abertura de diagrama com célula HTML contendo imagem e manipulador de evento de erro inline. | Remoção de manipuladores de evento em rótulos HTML. |
| **TD-03** | Q1.3 (M1.1) | Requisição HTTP `GET` (`/proxy`) | Solicitação ao *servlet* `/proxy` no servidor Tomcat apontando para caminho de arquivo local do sistema operacional. | Bloqueio de leitura de arquivos locais e esquemas não HTTP no `ProxyServlet`. |
| **TD-04** | Q1.3 (M1.1) | Requisição HTTP `GET` (`/proxy`) | Solicitação ao *servlet* `/proxy` no servidor Tomcat tentando acessar descritor interno da aplicação (`WEB-INF/web.xml`). | Bloqueio de acesso a recursos internos e endereços locais no `ProxyServlet`. |
| **TD-05** | Q1.5 (M1.3) | Arquivo `.drawio` temporário (Célula 1) | Rótulo HTML com elemento vetorial SVG aninhado e evento de carregamento inline. | Filtragem de elementos SVG e eventos automáticos. |
| **TD-06** | Q1.5 (M1.3) | Arquivo `.drawio` temporário (Célula 2) | Rótulo HTML em célula bloqueada para edição (`editable=0`) contendo âncora com URI de execução de script. | Neutralização de URIs de script em elementos não editáveis. |
| **TD-07** | Q1.5 (M1.3) | Arquivo `.drawio` temporário (Célula 3) | Rótulo HTML contendo quadro embutido apontando para URI de execução de script. | Remoção de elementos de quadro embutido na renderização. |
| **TD-08** | Q1.1 (M1.1) | Arquivo `.drawio` temporário | Importação de diagrama contendo elemento vetorial SVG com evento de carregamento inline no atributo de texto (`html=1`). | Remoção de elementos vetoriais e eventos ativos durante a importação XML. |
| **TD-09** | Q1.2 (M1.1) | Arquivo `.drawio` temporário | Abertura de diagrama contendo célula irmã regular acompanhada de célula bloqueada (`html=1;editable=0`) com imagem e manipulador de erro inline. | Isolamento de renderização e sanitização de rótulos HTML em células não editáveis. |

### Procedimento

A coleta é dividida em quatro blocos sequenciais:

**Bloco A: Inspeção estática de sanitização (M1.2 / Q1.4)**

1. Abrir o diretório do repositório `H3ytt0r10/drawio` (versão `32.6.10`) no VS Code.
2. Localizar os arquivos `Format.js`, `Graph.js` e `Editor.js` dentro de `src/main/webapp/js/`.
3. Pesquisar todas as ocorrências de `getLabelValue` nos três arquivos.
4. Aplicar o critério de contagem: contabiliza-se cada ponto de chamada onde o retorno é inserido ou avaliado no DOM (incluindo `Format.js:5683` em `canConvertHtmlToSvg`, que atribui o rótulo ao `.innerHTML`); exclui-se a própria definição do método base (`Graph.js:976`), comentários e checagens puramente lógicas sem manipulação de DOM, obtendo-se o conjunto de trechos válidos ($P_t$).
5. Rastrear o fluxo de dados de cada trecho válido até a renderização/medição HTML, verificando a aplicação de `Graph.sanitizeHtml` (via `sanitizeLabel`/DOMPurify) ou `mxUtils.htmlEntities` antes do uso no DOM, contabilizando os trechos protegidos ($P_p$).

**Bloco B: Testes dinâmicos base — importação e rótulos (M1.1 / Q1.1 e Q1.2)**

1. Iniciar o contêiner estático e abrir a aplicação em janela anônima.
2. Acionar **Arquivo > Importar de > Dispositivo**, executar os casos `TD-01` e `TD-08` (descartando o diagrama entre execuções) e observar se há execução de script ou renderização limpa da forma.
3. Acionar **Arquivo > Abrir de > Dispositivo**, executar os casos `TD-02` e `TD-09` (incluindo o cenário com célula irmã e célula `editable=0`) e verificar se os manipuladores de evento inline são neutralizados.

**Bloco C: Testes dinâmicos base — proxy e Path Traversal (M1.1 / Q1.3)**

1. Iniciar o contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente a `127.0.0.1:8080:8080`.
2. No PowerShell, executar `curl.exe -i` contra o endpoint `/proxy` para os cenários `TD-03` e `TD-04`.
3. Registrar o código de status HTTP retornado e confirmar no código-fonte (`WEB-INF/web.xml` e `ProxyServlet.java`) o comportamento do *servlet* implantado, encerrando o contêiner em seguida.

**Bloco D: Testes de resistência e variações de bypass (M1.3 / Q1.5)**

1. Na janela anônima do draw.io, acionar **Arquivo > Abrir de > Dispositivo** e carregar o diagrama com os cenários `TD-05` a `TD-07`.
2. Verificar a ausência de execução automática das células com elemento SVG e quadro embutido.
3. Clicar diretamente sobre o rótulo da célula não editável (`editable=0`) para confirmar a remoção do esquema de script.
4. Excluir o diretório temporário contendo os arquivos `.drawio` de teste e encerrar o contêiner.

### Critérios de leitura e registro das medidas

Conforme a estrutura GQM da Fase 2, a métrica **M1.1** é calculada individualmente por componente avaliado (sem agregação somada entre superfícies distintas):

| Métrica / Componente | Entrada / Escopo | Critério de Sucesso (Protegido / Bloqueado) | Valor Registrado |
| --- | --- | --- | --- |
| **M1.1 — Q1.1 (Importação)** | $C_{t,1} = 2$ casos (`TD-01` e `TD-08`). | Ausência de disparo de alerta e remoção de tags/elementos ativos na importação XML. | $M1.1_{Q1.1} = (C_{b,1} / C_{t,1}) \times 100$, em $\%$. |
| **M1.1 — Q1.2 (Rótulos HTML)** | $C_{t,2} = 2$ casos (`TD-02` e `TD-09`). | Neutralização de manipuladores de evento inline em rótulos HTML (incluindo células `editable=0`). | $M1.1_{Q1.2} = (C_{b,2} / C_{t,2}) \times 100$, em $\%$. |
| **M1.1 — Q1.3 (Proxy / Servidor)** | $C_{t,3} = 2$ casos (`TD-03` e `TD-04`). | Rejeição ativa pelo `ProxyServlet` no servidor Tomcat sem vazamento de arquivos internos. | $M1.1_{Q1.3} = (C_{b,3} / C_{t,3}) \times 100$, em $\%$. |
| **M1.2 — Q1.4 (Sanitização)** | $P_t = 4$ pontos de chamada válidos em `Format.js` e `Graph.js`. | Presença comprovada de sanitização (`DOMPurify`) ou escape (`mxUtils.htmlEntities`) antes da inserção no DOM. | $M1.2 = (P_p / P_t) \times 100$, em $\%$. |
| **M1.3 — Q1.5 (Resistência)** | $W_t = 3$ variações de evasão (`TD-05` a `TD-07`). | Neutralização integral das tags/atributos ofuscados ou combinados com estilos (`editable=0`). | $M1.3 = (W_b / W_t) \times 100$, em $\%$. |

### Critérios de bloqueio, falhas e descartes

Cada caso dinâmico é classificado como **bloqueado** quando o vetor é removido ou escapado pela aplicação sem execução de JavaScript e sem exposição de recursos locais. Considera-se **falha de segurança** (vulnerabilidade explorável) qualquer execução de script no navegador, injeção de elemento ativo no DOM ou retorno `HTTP 200` com conteúdo de arquivo do sistema/servidor. Caso ocorra erro operacional externo ao sistema avaliado (como falha de inicialização do contêiner, ausência do *servlet* alvo ou cache residual de sessão), o teste é **descartado**, o ambiente é ajustado e a execução é repetida.

### Registro dos dados

Os registros da coleta ficam armazenados em `dados/avaliacao/seguranca/`:

| Caminho | Conteúdo |
| --- | --- |
| `resultados_dinamicos.csv` | Registro de cada caso executado (`TD-01` a `TD-09`) com status e comportamento observado. |
| `inspecao_estatica.csv` | Mapeamento das ocorrências de `getLabelValue` por arquivo, linha, classificação ($P_t$) e proteção ($P_p$). |

Colunas de `resultados_dinamicos.csv`: `data`, `id_teste`, `questao`, `metrica`, `descricao_caso`, `tipo_analise`, `comportamento_observado`, `status`.

### Verificação prévia (Piloto)

Antes da execução formal dos casos, realiza-se uma verificação prévia do ambiente para:

- confirmar a leitura do arquivo `VERSION` (`32.6.10`) e o mapeamento do volume `src/main/webapp` no contêiner estático;
- validar o carregamento da interface web sem dependências externas;
- verificar a presença do mapeamento `/proxy` (`ProxyServlet`) na imagem oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) para a coleta de `Q1.3`.