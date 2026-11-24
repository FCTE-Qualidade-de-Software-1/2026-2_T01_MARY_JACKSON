# Plano de avaliação

Esta página reúne o plano de avaliação de cada característica: [Segurança (Dupla 1)](#seguranca-dupla-1), [Eficiência de desempenho (Dupla 2)](#eficiencia-de-desempenho-dupla-2) e [Manutenibilidade (Dupla 3)](#manutenibilidade-dupla-3). A obtenção do código avaliado está no [guia do ambiente do draw.io](ambiente-drawio.md), e a execução de cada plano, na [Fase 4](../fase-4/index.md).

## Segurança (Dupla 1)

Esta seção define o protocolo de coleta das métricas **M1.1 a M1.3** da [Fase 2](../fase-2/metricas.md), vinculadas ao objetivo global **G1** (Confidencialidade, Integridade e Resistência). Toda a avaliação é conduzida por um único avaliador, combinando inspeção estática de código-fonte (caixa-branca) e testes dinâmicos de penetração (caixa-preta) em ambiente local isolado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões restringem-se à versão avaliada, à configuração de implantação local e ao modelo de ameaças definido.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio) e da imagem oficial `jgraph/drawio:32.6.10`. |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | Contêiner Docker estático (`httpd:alpine`) montando `src/main/webapp` para os testes de interface web (`Q1.1`, `Q1.2` e `Q1.5`), e contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente a `127.0.0.1:8080:8080` com `EXPORT_URL` configurado para o teste do *servlet* de exportação `ExportProxyServlet` (`/export` e `/service/*`, `Q1.3`). |

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
| Docker (`httpd:alpine` e `jgraph/drawio:32.6.10`) | Hospedagem local da interface web (`src/main/webapp`) para os testes de cliente e execução do servidor Java (Tomcat) com `EXPORT_URL` configurado para validação do `ExportProxyServlet` (`/export` e `/service/*`). |
| Visual Studio Code (VS Code) | Busca e rastreamento de fluxo de dados no código-fonte (`Format.js`, `Graph.js`, `Editor.js` e `ExportProxyServlet.java`) para M1.2 e auditoria de servidor, além da criação temporária dos arquivos `.drawio` de teste. |
| Git | Clonagem do repositório customizado e verificação da integridade da versão (`VERSION` e hash do commit). |
| Navegador Web (janela anônima) | Importação e abertura dos diagramas de teste em sessão limpa para observação visual e de execução no DOM (M1.1 e M1.3). |
| `curl.exe` (PowerShell) | Envio de requisições HTTP de teste (`--path-as-is`) contra as rotas `/service/*` e `/export` no servidor Tomcat para validação de *Path Traversal* no `ExportProxyServlet` (M1.1 / Q1.3). |

### Condições de execução e limitações de ambiente

| Condição | Regra / Observação |
| --- | --- |
| Perfil do navegador | Janela anônima/convidado, sem extensões instaladas, sem histórico e sem outras abas abertas durante a execução. |
| Exposição de rede e vínculo de porta (limitação) | Na primeira rodada com `httpd:alpine` (`TD-01`, `TD-02` e `TD-05` a `TD-07`), a publicação padrão `-p 8080:80` vinculou o serviço em `0.0.0.0:8080` (acessível na rede local), o que fica registrado como limitação da coleta inicial. Na validação do servidor Java (`TD-03` e `TD-04`) e nos casos complementares (`TD-08` e `TD-09`), o mapeamento foi restrito exclusivamente à interface de *loopback* (`127.0.0.1:8080:8080` / `127.0.0.1:8080:80`). |
| Limpeza de estado | Cada caso dinâmico de abertura/importação é executado descartando o diagrama anterior ou recarregando a sessão limpa. |
| Divulgação responsável (protocolo 5.2.4) | Os arquivos `.drawio` contendo vetores de teste são criados em diretório temporário fora dos repositórios Git e excluídos imediatamente após a coleta. Nenhum *payload* literal ou comando de ataque é publicado no repositório, registrando-se apenas a descrição funcional de cada caso e o resultado observado. |

### Artefatos e casos de teste

Os testes dinâmicos baseiam-se em cenários de vulnerabilidades históricas documentadas para o draw.io (injeção de script via importação XML, XSS em rótulos HTML — ref. CVE-2026-46642, *Path Traversal* no proxy de exportação `ExportProxyServlet` — ref. CVE-2026-63416 e variações de evasão em elementos não editáveis — ref. CVE-2026-58504), totalizando **9 casos dinâmicos** (ao menos 2 casos por componente em `M1.1` e 3 variações em `M1.3`).

| ID | Questão / Métrica | Artefato ou Requisição | Cenário Testado | Mecanismo Avaliado |
| --- | --- | --- | --- | --- |
| **TD-01** | Q1.1 (M1.1) | Arquivo `.drawio` temporário | Importação de diagrama contendo tag de script embutida no atributo de texto de uma célula (`html=1`). | Sanitização na importação de arquivos XML. |
| **TD-02** | Q1.2 (M1.1) | Arquivo `.drawio` temporário | Abertura de diagrama com célula HTML contendo imagem e manipulador de evento de erro inline. | Remoção de manipuladores de evento em rótulos HTML. |
| **TD-03** | Q1.3 (M1.1) | Requisição HTTP `GET` (`/service/*`) | Solicitação à rota `/service/*` no servidor Tomcat (`EXPORT_URL` configurado) tentando travessia de diretório até `WEB-INF/web.xml` (ref. CVE-2026-63416). | Bloqueio de travessia de diretório na camada HTTP (Tomcat) e no `ExportProxyServlet`. |
| **TD-04** | Q1.3 (M1.1) | Requisição HTTP `GET` (`/export`) | Solicitação à rota `/export` no servidor Tomcat (`EXPORT_URL` configurado) tentando travessia de diretório com barras codificadas até `WEB-INF/web.xml` (ref. CVE-2026-63416). | Bloqueio de barras codificadas e travessia de caminho no Tomcat e no `ExportProxyServlet`. |
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
4. Aplicar o critério de contagem: contabiliza-se cada ponto de chamada onde o retorno é inserido ou avaliado no DOM (incluindo `Format.js:5683` em `canConvertHtmlToSvg`, que atribui o rótulo ao `.innerHTML`); exclui-se a própria definição do método base (`Graph.js:976`), comentários e checagens puramente lógicas sem manipulação de DOM, obtendo-se o conjunto de trechos válidos (P<sub>t</sub>).
5. Rastrear o fluxo de dados de cada trecho válido até a renderização/medição HTML, verificando a aplicação de `Graph.sanitizeHtml` (via `sanitizeLabel`/DOMPurify) ou `mxUtils.htmlEntities` antes do uso no DOM, contabilizando os trechos protegidos (P<sub>p</sub>).

**Bloco B: Testes dinâmicos base — importação e rótulos (M1.1 / Q1.1 e Q1.2)**

1. Iniciar o contêiner estático e abrir a aplicação em janela anônima.
2. Acionar **Arquivo > Importar de > Dispositivo**, executar os casos `TD-01` e `TD-08` (descartando o diagrama entre execuções) e observar se há execução de script ou renderização limpa da forma.
3. Acionar **Arquivo > Abrir de > Dispositivo**, executar os casos `TD-02` e `TD-09` (incluindo o cenário com célula irmã e célula `editable=0`) e verificar se os manipuladores de evento inline são neutralizados.

**Bloco C: Testes dinâmicos base — proxy de exportação e Path Traversal (M1.1 / Q1.3)**

1. Iniciar o contêiner oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) vinculado estritamente a `127.0.0.1:8080:8080` com a variável de ambiente `EXPORT_URL` apontando para um serviço HTTP local de teste.
2. No PowerShell, executar `curl.exe -i --path-as-is` contra as rotas `/service/*` e `/export` para os cenários `TD-03` e `TD-04`.
3. Registrar o código de status HTTP retornado (`400 Bad Request` no Tomcat) e confirmar no código-fonte (`WEB-INF/web.xml` e `ExportProxyServlet.java`, linhas 99–113) a proteção contra *Path Traversal*, encerrando o contêiner em seguida.

**Bloco D: Testes de resistência e variações de bypass (M1.3 / Q1.5)**

1. Na janela anônima do draw.io, acionar **Arquivo > Abrir de > Dispositivo** e carregar o diagrama com os cenários `TD-05` a `TD-07`.
2. Verificar a ausência de execução automática das células com elemento SVG e quadro embutido.
3. Clicar diretamente sobre o rótulo da célula não editável (`editable=0`) para confirmar a remoção do esquema de script.
4. Excluir o diretório temporário contendo os arquivos `.drawio` de teste e encerrar o contêiner.

### Critérios de leitura e registro das medidas

Conforme a estrutura GQM da Fase 2, a métrica **M1.1** é calculada individualmente por componente avaliado (sem agregação somada entre superfícies distintas):

| Métrica / Componente | Entrada / Escopo | Critério de Sucesso (Protegido / Bloqueado) | Valor Registrado |
| --- | --- | --- | --- |
| **M1.1 — Q1.1 (Importação)** | C<sub>t,1</sub> = 2 casos (`TD-01` e `TD-08`). | Ausência de disparo de alerta e remoção de tags/elementos ativos na importação XML. | M1.1<sub>Q1.1</sub> = (C<sub>b,1</sub> / C<sub>t,1</sub>) × 100, em %. |
| **M1.1 — Q1.2 (Rótulos HTML)** | C<sub>t,2</sub> = 2 casos (`TD-02` e `TD-09`). | Neutralização de manipuladores de evento inline em rótulos HTML (incluindo células `editable=0`). | M1.1<sub>Q1.2</sub> = (C<sub>b,2</sub> / C<sub>t,2</sub>) × 100, em %. |
| **M1.1 — Q1.3 (Proxy / Servidor)** | C<sub>t,3</sub> = 2 casos (`TD-03` e `TD-04`). | Rejeição ativa na camada HTTP do servidor Tomcat e no `ExportProxyServlet` sem vazamento de arquivos internos. | M1.1<sub>Q1.3</sub> = (C<sub>b,3</sub> / C<sub>t,3</sub>) × 100, em %. |
| **M1.2 — Q1.4 (Sanitização)** | P<sub>t</sub> = 4 pontos de chamada válidos em `Format.js` e `Graph.js`. | Presença comprovada de sanitização (`DOMPurify`) ou escape (`mxUtils.htmlEntities`) antes da inserção no DOM. | M1.2 = (P<sub>p</sub> / P<sub>t</sub>) × 100, em %. |
| **M1.3 — Q1.5 (Resistência)** | W<sub>t</sub> = 3 variações de evasão (`TD-05` a `TD-07`). | Neutralização integral das tags/atributos ofuscados ou combinados com estilos (`editable=0`). | M1.3 = (W<sub>b</sub> / W<sub>t</sub>) × 100, em %. |

### Critérios de bloqueio, falhas e descartes

Cada caso dinâmico é classificado como **bloqueado** quando o vetor é removido ou escapado pela aplicação sem execução de JavaScript e sem exposição de recursos locais. Considera-se **falha de segurança** (vulnerabilidade explorável) qualquer execução de script no navegador, injeção de elemento ativo no DOM ou retorno `HTTP 200` com conteúdo de arquivo do sistema/servidor. Caso ocorra erro operacional externo ao sistema avaliado (como falha de inicialização do contêiner, ausência do *servlet* alvo ou cache residual de sessão), o teste é **descartado**, o ambiente é ajustado e a execução é repetida.

### Registro dos dados

Os registros da coleta ficam armazenados em `dados/avaliacao/seguranca/`:

| Caminho | Conteúdo |
| --- | --- |
| `resultados_dinamicos.csv` | Registro de cada caso executado (`TD-01` a `TD-09`) com status e comportamento observado. |
| `inspecao_estatica.csv` | Mapeamento das ocorrências de `getLabelValue` por arquivo, linha, classificação (P<sub>t</sub>) e proteção (P<sub>p</sub>). |

Colunas de `resultados_dinamicos.csv`: `data`, `id_teste`, `questao`, `metrica`, `descricao_caso`, `tipo_analise`, `comportamento_observado`, `status`.

### Verificação prévia (Piloto)

Antes da execução formal dos casos, realiza-se uma verificação prévia do ambiente para:

- confirmar a leitura do arquivo `VERSION` (`32.6.10`) e o mapeamento do volume `src/main/webapp` no contêiner estático;
- validar o carregamento da interface web sem dependências externas;
- verificar a presença do mapeamento `/export` e `/service/*` (`ExportProxyServlet`) na imagem oficial com servidor Java/Tomcat (`jgraph/drawio:32.6.10`) com `EXPORT_URL` configurado para a coleta de `Q1.3`.

### Ambiente Complementar — Validação de Defense-in-Depth com CSP

Para avaliar a viabilidade de mitigação complementar contra XSS via cabeçalhos HTTP sem alterar o código-fonte da release `32.6.10`, configurou-se um servidor estático baseado em `httpd:alpine` (`Apache/2.4.71`) servindo o diretório `src/main/webapp` em `http://127.0.0.1:8080`:

- **Cenário Base (Antes):** Contêiner padrão sem configuração de cabeçalhos de segurança:
  ```powershell
  docker run -d --name drawio-sem-csp -p 127.0.0.1:8080:80 -v "${DRAWIO_WEBAPP}:/usr/local/apache2/htdocs:ro" httpd:alpine
  ```
- **Cenário Endurecido (Depois):** Contêiner com `mod_headers` habilitado e injeção da diretiva `Content-Security-Policy` via `csp.conf`:
  ```apache
  Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self';"
  ```
- **Verificação de Scripts Inline:** A inspeção do `index.html` da release `32.6.10` confirmou a ausência de blocos `<script>` *inline*, permitindo omitir `'unsafe-inline'`, `'unsafe-hashes'` e exceções por hash (`sha256-...`) em `script-src`.

## Eficiência de desempenho (Dupla 2)

Esta seção define como são coletadas as métricas M2.1 a M2.6 da [Fase 2](../fase-2/metricas.md). Toda a coleta é feita em uma única máquina e em um único navegador, para que os resultados dos cinco portes sejam comparáveis entre si. A coleta oficial é automatizada por script, depois de um [piloto](#piloto-eficiencia) manual que validou o procedimento no DevTools e de um piloto automatizado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões ficam vinculadas a essa versão, máquina, navegador e cargas.

### Versão avaliada {#versao-avaliada-eficiencia}

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, referência da campanha histórica das três duplas. |
| Execução | Servidor HTTP estático local (`python -m http.server 8080`) servindo a pasta `src/main/webapp` do fork, acessado em `http://localhost:8080/?offline=1`. Não há servidor de exportação. |

### Máquina cliente e navegador {#maquina-cliente-e-navegador-eficiencia}

| Item | Configuração |
| --- | --- |
| Processador | Intel Core i5-1235U (12ª geração), 10 núcleos, 12 processadores lógicos, 1,30 GHz de base. |
| Memória RAM | 16 GB (15,7 GB utilizáveis). |
| Armazenamento | SSD NVMe. |
| Placa de vídeo | Intel Iris Xe (integrada). |
| Sistema operacional | Windows 11, versão 25H2 (build 26200.9974). |
| Navegador | Google Chrome 157.0.8103.79, 64 bits (V8 15.7.112.43). |
| Avaliador responsável | Pedro Ian (Dupla 2). |

Se o Chrome for atualizado durante a coleta, a nova versão é registrada a partir da tentativa em que passou a valer.

### Ferramentas {#ferramentas-eficiencia}

| Ferramenta | Uso |
| --- | --- |
| Script `coletar.py` (Python 3 e Playwright) | Abre o Google Chrome instalado na máquina, executa as operações do [procedimento](#procedimento-eficiencia) e grava um trace do Chrome por operação, com as categorias de eventos do painel Performance do DevTools (tarefas do thread principal, eventos, contadores de memória e capturas de tela). |
| Script `ler_traces.py` (Python 3) | Lê os traces, extrai tempo e heap segundo a [leitura das medidas](#leitura-das-medidas) e gera o CSV de tentativas. Apenas lê os traces, sem alterá-los. |
| Script `validar_exportacoes.py` (Python 3, Playwright e pypdf) | Exporta e salva um arquivo de cada formato por porte e verifica se o arquivo é válido e se contém o diagrama completo (ver [validação das exportações](#validacao-das-exportacoes)). Não mede tempo. |
| Script `gerar_cargas.py` (Python 3) | Gera as cinco cargas sintéticas de forma reprodutível. |
| `Get-FileHash` (PowerShell) | Calcula o SHA-256 das cargas para identificá-las. |
| Chrome DevTools, painel Performance | Usado no piloto manual e para conferir qualquer trace: o CSV registra os instantes `ti` e `tf` usados em cada medida. |

### Condições de execução {#condicoes-de-execucao-eficiencia}

| Condição | Regra |
| --- | --- |
| Perfil do navegador | Perfil novo e temporário criado pela automação a cada sessão, sem extensões e sem histórico, equivalente à janela de convidado. Idioma da interface `en-US`. |
| Janela | Chrome com janela visível, área da página de 1366 x 768 px, sem interação do avaliador durante a coleta. |
| Sessão limpa | Cada sessão começa em um perfil novo. Antes de cada gravação, a automação aciona a coleta de lixo do JavaScript (`HeapProfiler.collectGarbage`). |
| Máquina | Conectada à energia, outros programas fechados, sincronização do OneDrive pausada e notificações do Windows silenciadas. O percentual de memória em uso é registrado no início da coleta. |
| Rede | Instância local com `offline=1`. Sem acesso a serviços em nuvem. |
| Ordem | Portes do menor para o maior; dentro de cada porte, as cinco tentativas são feitas em sequência. |

### Cargas sintéticas

As cargas são geradas pelo script `gerar_cargas.py`. Cada arquivo `.drawio` (XML não compactado) contém N retângulos iguais de 120 x 60 px, dispostos em grade de 50 colunas, sem conectores, imagens ou estilos adicionais. As formas têm identificadores `v0001`, `v0002`, ... e rótulos `Rotulo 0001`, `Rotulo 0002`, ...; a forma `v0001` é a usada na M2.3. A saída é determinística: executar o script novamente gera arquivos com o mesmo SHA-256. Os valores abaixo valem para os arquivos como estão no repositório (fim de linha LF); no Windows, o Git pode converter o fim de linha da cópia local para CRLF, o que muda o SHA-256 calculado por `Get-FileHash` sem alterar o conteúdo do diagrama.

| Porte (formas) | Arquivo | SHA-256 |
| --- | --- | --- |
| 50 | `carga-00050.drawio` | `03d1a23d7dab0002d11be9eff8207e9cdbb5bcd01fa6c862dd564bac8dd7e139` |
| 300 | `carga-00300.drawio` | `229e6dc2f2a4271deb106fe79be3f9f1da14990e560ade53fadf5bc1b459281a` |
| 1.000 | `carga-01000.drawio` | `1e16ccfe0894ec0afa3163cc43e846e1dda9177465ade1684af1a99995234b91` |
| 2.000 | `carga-02000.drawio` | `1de87eea590083ac74e2d59bc86129a50fafd7a8a87396ec8d5cf13bda3d4777` |
| 5.000 | `carga-05000.drawio` | `9c35607e784f835084f3dd505021ab75ddce2c7f3eb870a3f4e0328766096d62` |

### Procedimento {#procedimento-eficiencia}

Cada tentativa de um porte é composta por quatro sessões, cada uma em um perfil novo: uma para abertura e rótulo e uma para cada formato de exportação. Separar as exportações evita que a memória de uma operação influencie o pico da seguinte. Ao detectar o fim de cada operação, o script grava a marca `fim_operacao` no trace, usada na leitura do instante final.

**Sessão A: abertura e rótulo (M2.1, M2.2 e M2.3)**

1. Acionar a coleta de lixo e iniciar a gravação.
2. Acionar **File > Open from > Device...** e selecionar a carga, substituindo o documento atual.
3. Aguardar as formas da carga no documento, gravar a marca, esperar 3 s e parar a gravação.
4. Iniciar nova gravação, clicar na forma `v0001`, pressionar `F2`, `Ctrl+A`, digitar `Rotulo A001` e confirmar com `Ctrl+Enter`.
5. Aguardar o novo rótulo no documento, gravar a marca, esperar 2 s e parar a gravação.

**Sessões B, C e D: exportação em PNG, PDF e SVG (M2.4 e M2.5)**

1. Abrir a carga (abertura não medida) e acionar **File > Export as > (formato)...**, mantendo as opções padrão do draw.io (zoom 100%, tamanho Diagram e a opção "Include a copy of my diagram" marcada, como vem por padrão).
2. Acionar a coleta de lixo e iniciar a gravação.
3. Clicar em **Export**.
4. PNG e SVG: aguardar o diálogo "Save as", que indica o arquivo gerado. PDF: aguardar a chamada de impressão (ver adaptação 2 abaixo). Gravar a marca, esperar 1,5 s e parar a gravação.

**Adaptações necessárias à automação**

1. **Seletor de arquivos.** No Chrome, o draw.io usa o seletor nativo da API File System Access, que não aceita automação. A automação desativa essa API na página, e o draw.io passa a usar o seletor `<input type="file">`, que também faz parte do produto. A leitura e a renderização do diagrama são as mesmas; muda apenas a forma de entregar o arquivo à página.
2. **PDF.** Sem servidor de exportação, o draw.io prepara uma página de impressão em nova janela e chama `print()`; o arquivo PDF seria produzido pela impressão do próprio Chrome. A automação substitui `print()` por uma função que apenas grava a marca `fim_operacao`. Assim, M2.4 e M2.5 de PDF medem a preparação da página de impressão pelo draw.io, e a geração do arquivo pelo navegador, que não é do draw.io, fica fora da medida.
3. **Salvamento em disco.** O salvamento depende de diálogos com o avaliador (o "Save as" do draw.io e o seletor do Windows) e não é medido. A exportação termina quando o draw.io conclui a geração e exibe o diálogo "Save as".

### Validação das exportações

A coleta mede o tempo até o draw.io concluir a exportação, sem salvar os arquivos. Por isso, a integridade dos arquivos é verificada à parte, depois da coleta, pelo script `validar_exportacoes.py`. Para cada porte, ele exporta e salva um arquivo de cada formato e registra, separadamente, se o arquivo abre (formato válido) e se o diagrama está completo nele. A validação não mede tempo, e as condições de execução da coleta não se aplicam a ela.

| Formato | Como o arquivo é obtido | Verificação |
| --- | --- | --- |
| PNG | Diálogo "Save as" com a opção Download, pois a API de salvamento do navegador é desativada para permitir a automação. | Assinatura do formato e dimensões da imagem, comparadas com a área ocupada pelas formas da carga; uma imagem cortada teria outras dimensões. |
| SVG | Como no PNG. | XML válido e quantidade de rótulos `Rotulo NNNN` distintos igual ao número de formas da carga. |
| PDF | Página de impressão preparada pelo draw.io, convertida em PDF pelo mecanismo de impressão do Chrome, o mesmo do "Salvar como PDF", em papel tamanho carta. | Assinatura do formato, número de páginas e quantidade de rótulos que aparecem inteiros em alguma página. |

PNG e SVG podem ser exportados com a janela do navegador visível (opção `--janela`); o PDF é gerado sem janela, único modo em que o Chrome permite gerar o PDF por automação.

### Leitura das medidas

As medidas consideram as tarefas de pelo menos 1 ms do thread principal da página do draw.io. São ignoradas as tarefas que apenas tratam movimento do mouse ou tecla sendo solta, que são ações de entrada e não processamento da operação, e as tarefas da própria automação.

| Métrica | Início (`ti`) | Fim (`tf`) | Valor registrado |
| --- | --- | --- | --- |
| M2.1 | Início da tarefa que trata o evento `change` do seletor de arquivos. | Fim da última tarefa iniciada antes da marca `fim_operacao` (formas no documento). | `tf - ti`, em ms. |
| M2.2 | | | Heap JS usado 2 s após o `tf` de M2.1 (última amostra até `tf + 2 s`), em MiB. |
| M2.3 | Início da tarefa que trata a última tecla pressionada (o `Enter` de `Ctrl+Enter`). | Fim da última tarefa iniciada antes da marca (novo rótulo no documento). | `tf - ti`, em ms. |
| M2.4 | Início da tarefa que trata o clique em **Export**. | Fim da última tarefa iniciada antes da marca (diálogo "Save as" ou chamada de impressão). | `tf - ti`, em ms. |
| M2.5 | Mesmo `ti` de M2.4. | Mesmo `tf` de M2.4. | Maior valor do heap JS usado entre `ti` e `tf`, em MiB. |
| M2.6 | | | Consolidado das tentativas de M2.1 a M2.5, conforme a Fase 2. |

Valores do heap em bytes são convertidos por `MiB = bytes / 2^20`. Nos traces manuais do piloto, que não têm a marca, o fim é o término da sequência de processamento iniciada em `ti`, encerrada no primeiro intervalo de mais de 250 ms sem tarefas, e o início da abertura é a primeira tarefa após o fechamento do seletor nativo.

### Tentativas válidas, falhas e interrupções {#tentativas-validas-falhas-e-interrupcoes-eficiencia}

Para cada porte e operação são realizadas cinco tentativas válidas. Uma tentativa interrompida por fator externo ao draw.io é descartada, registrada com o motivo e reposta. É considerada **falha** do draw.io a tentativa com erro exibido, travamento da aba, arquivo exportado inválido ou operação que não termina em até duas vezes o limite candidato do cenário (faixa da nota 1 na Fase 2). A automação registra em `brutos/traces/falhas.txt` as operações que não concluem em 180 s ou terminam com erro. Os limites foram ratificados pela Dupla 2 em 15/11/2026, após a coleta, mantendo os valores originais. O CSV guarda o valor medido de todas as tentativas concluídas; na análise, as que passam de duas vezes o limite são tratadas como falha, contam para a M2.6 e não entram nas medianas de tempo dos sucessos. Essa era a regra inicial da coleta. Para a análise, aplica-se a [revisão pós-coleta de 15/11/2026](../fase-2/niveis-e-julgamento.md#revisao-pos-coleta-do-julgamento-15112026): menos de quatro sucessos por falha do produto resulta em nota temporal 1; a memória é julgada pelas medidas completas das operações concluídas, independentemente da falha temporal. Ausência ou invalidade de dados continua não conclusiva.

### Registro dos dados {#registro-dos-dados-eficiencia}

Os CSVs, scripts e cargas são versionados em `dados/avaliacao/eficiencia/`. Os traces são preservados em pacotes externos e podem ser restaurados nos caminhos abaixo. O acesso aos pacotes, as instruções de restauração e a conferência dos hashes estão em `dados/avaliacao/eficiencia/README.md`. Os pacotes estão disponíveis na [pasta de evidências no Google Drive](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

| Caminho | Conteúdo |
| --- | --- |
| `cargas/` | As cinco cargas e o script `gerar_cargas.py`. |
| `coletar.py` e `ler_traces.py` | Scripts de coleta e de leitura dos traces. |
| `brutos/tentativas.csv` | Uma linha por operação medida na coleta oficial. |
| `brutos/traces/` | Caminho local dos 125 traces da coleta oficial (`.json.gz`), restaurados do pacote externo e ignorados pelo Git. São nomeados por porte, operação, formato e tentativa, como `p05000_exportar-svg_t3.json.gz`. Na coleta, URLs do tipo `data:` (imagens geradas durante a exportação) são truncadas em 200 caracteres para reduzir o tamanho; o restante do trace não é alterado. |
| `brutos/piloto/` | CSV versionado e caminho local dos 10 traces do piloto automatizado, restaurados do pacote externo. |
| `brutos/piloto/manual/` | CSV versionado e caminho local dos 4 traces do piloto manual, restaurados do pacote externo. |
| `brutos/exportados/` | `validacao.csv` versionado e caminho local dos 14 arquivos exportados na validação, restaurados do pacote externo. |
| `README.md` e `SHA256SUMS.txt` | Orientações de acesso e restauração das evidências e manifesto de integridade. |

Colunas de `tentativas.csv`: `data`, `tentativa`, `porte`, `operacao`, `formato`, `versao_chrome`, `memoria_em_uso_pct`, `tempo_ms`, `heap_mib`, `resultado` (sucesso, falha, descartada ou verificar), `observacao`, `trace`, `ti_ms` e `tf_ms` (instantes de início e fim em ms desde o começo do trace, para conferência no DevTools).

### Piloto {#piloto-eficiencia}

Antes da coleta oficial, validar o procedimento manualmente e por automação, conferir as cargas e os marcos de início e fim das operações. Os dados do piloto devem ser registrados separadamente e excluídos das métricas oficiais. Os [resultados do piloto](../fase-4/coleta-de-dados.md#resultados-do-piloto-de-eficiencia) documentam os achados e as adaptações adotadas.

## Manutenibilidade (Dupla 3)

Esta seção define como serão coletadas as métricas M3.1 e M3.2 da [Fase 2](../fase-2/metricas.md). Toda a coleta é feita e avaliada pela dupla, utilizando a mesma versão do programa de avaliação e do programa avaliado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões ficam vinculadas a essa versão.

### Versão avaliada {#versao-avaliada-manutenibilidade}

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, referência da campanha histórica das três duplas. |
| Execução | localmente, conforme o [guia do ambiente](ambiente-drawio.md). |

### Máquina cliente e navegador {#maquina-cliente-e-navegador-manutenibilidade}

| Item | Configuração |
| --- | --- |
| Processador | Intel Core Ultra 7 155H, 16 núcleos e 22 processadores lógicos. |
| Memória RAM | 16 GB (15,5 GB utilizáveis). |
| Armazenamento | SSD NVMe Samsung MZVL4512HBLU-00B, 512 GB. |
| Placa de vídeo | Intel Arc Graphics (integrada). |
| Sistema operacional | Windows 11 Home Single Language, versão 26H2 (build 26300.9974), 64 bits. |
| Navegador | Google Chrome 157.0.8103.79, 64 bits. |
| Avaliador | Lucas Gabriel (Dupla 3). |

Se o Chrome for atualizado durante a coleta, a nova versão é registrada a partir da tentativa em que passou a valer.

### Ferramentas {#ferramentas-manutenibilidade}

| Ferramenta | Uso |
| --- | --- |
| SonarCloud | Análise estática do código selecionado para coletar a complexidade cognitiva (M3.1) e o percentual de código duplicado (M3.2). |

### Condições de execução {#condicoes-de-execucao-manutenibilidade}

| Condição | Regra |
| --- | --- |
| Objeto analisado | Fixar o commit e registrar os caminhos dos arquivos e funções de cada componente. Campanhas com outro commit ou escopo devem ser identificadas separadamente. |
| Ferramenta | Registrar a configuração do SonarCloud, inclusões, exclusões, versão do analisador quando disponível e ID da análise. |
| Rede | A coleta remota exige acesso ao SonarCloud. A restrição offline dos testes de desempenho não se aplica a essa análise estática. |
| Validade | Conferir o inventário efetivamente processado e a presença dos numeradores e denominadores. Ausência de dados não equivale a zero. |
| Repetição | Reexecutar em caso de falha ou mudança de configuração, commit ou escopo. Não se aplicam cinco tentativas por porte, medianas nem coleta de lixo do navegador. |

### Procedimento {#procedimento-manutenibilidade}

O procedimento segue as [fichas das métricas](../fase-2/metricas.md#manutenibilidade-dupla-3), com análise estática pelo SonarCloud e julgamento separado para cada questão do GQM.

**Preparação da análise**

1. Utilizar o código do fork `H3ytt0r10/drawio`, versão `32.6.10`, no commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`.
2. Identificar e registrar os arquivos e as funções de importação de arquivos, edição de rótulos e exportação PNG, PDF e SVG que compõem o recorte avaliado.
3. Configurar o projeto no SonarCloud, conferir o escopo e as exclusões da análise e registrar a configuração utilizada, a identificação da execução e o commit analisado.
4. Executar a análise e conferir sua conclusão e a presença das medidas necessárias no relatório. Corrigir eventuais erros de configuração e repetir a execução antes de utilizar os resultados.

**Coleta e cálculo das métricas**

1. Para a **M3.1**, registrar a complexidade cognitiva total (`C`) e a quantidade de funções (`F`) pertencentes a cada componente. Calcular `M3.1 = C / F` separadamente para importação (**Q3.1**) e edição de rótulos (**Q3.2**), considerando todas as funções do recorte, inclusive as que não geram alertas.
2. Para a **M3.2**, analisar conjuntamente o código de exportação PNG, PDF e SVG e registrar as linhas duplicadas (`Ld`) e o total de linhas analisadas (`Lt`). Calcular `M3.2 = (Ld / Lt) × 100`, respondendo à **Q3.3**, sem fazer a média dos percentuais individuais dos arquivos.
3. Registrar os valores brutos, os arquivos e funções considerados e a referência ao relatório na [coleta de dados](../fase-4/coleta-de-dados.md#manutenibilidade-dupla-3), permitindo conferir os cálculos.
4. Comparar os resultados com os [níveis de julgamento da Fase 2](../fase-2/niveis-e-julgamento.md#manutenibilidade-dupla-3): para M3.1, adequado até 10, atenção acima de 10 até 15 e crítico acima de 15; para M3.2, adequado até 5%, atenção acima de 5% até 10% e crítico acima de 10%. Registrar o julgamento de cada questão na [análise dos resultados](../fase-4/resultados.md#manutenibilidade-dupla-3).

### Tentativas válidas, falhas e interrupções {#tentativas-validas-falhas-e-interrupcoes-manutenibilidade}

Uma execução é considerada **válida** quando a análise do SonarCloud termina com sucesso, corresponde ao commit e ao escopo definidos e fornece os dados necessários ao cálculo da métrica. Para M3.1, é necessário `F > 0`; para M3.2, `Lt > 0`. A ausência de dados não é registrada como valor zero: o resultado permanece pendente até que a coleta seja completada.

Como a coleta é feita por análise estática, não se aplica a repetição de cinco tentativas nem o cálculo de medianas adotados pela Dupla 2. Uma nova execução é necessária quando houver falha, dados incompletos ou alteração do commit, do escopo ou da configuração; nesse último caso, os resultados devem ser identificados separadamente.

### Registro dos dados {#registro-dos-dados-manutenibilidade}

O [relatório consolidado fornecido](../fase-4/evidencias/resultados-das-analises.md) foi preservado neste repositório. A [coleta](../fase-4/coleta-de-dados.md#manutenibilidade-dupla-3) registra o inventário e a situação das medidas; os [resultados](../fase-4/resultados.md#manutenibilidade-dupla-3) apresentam os cálculos históricos e seus limites. Os demais artefatos citados no relatório são referências ao ambiente de origem e não foram fornecidos aqui.

### Piloto {#piloto-manutenibilidade}

Antes da coleta, executar uma análise de verificação para conferir o processamento dos arquivos incluídos, os limites de tamanho, as exclusões e as medidas retornadas. Validar o detector de duplicação com código de duplicação conhecida em campanha separada. Esse código de controle não integra o denominador da avaliação real. Preservar os registros do piloto separadamente das medidas oficiais.
