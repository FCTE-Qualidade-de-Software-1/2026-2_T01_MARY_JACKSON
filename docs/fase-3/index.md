# Fase 3: Projetar a avaliação

<!-- O que entra aqui: plano de avaliação: método, instruções para o avaliador, recursos e cronograma (Aula 07, págs. 18 e 19). Entrega 2. -->

O ambiente de execução previsto para a avaliação é o draw.io web 32.6.10 localmente por meio de um fork feito pelo membro Heyttor Augusto. Consulte o [guia do ambiente local](ambiente-drawio.md) para iniciar e operar o contêiner.


## Eficiência de desempenho (Dupla 2)

Esta seção define como são coletadas as métricas M2.1 a M2.6 da [Fase 2](../fase-2/metricas.md). Toda a coleta é feita em uma única máquina e em um único navegador, para que os resultados dos cinco portes sejam comparáveis entre si. A coleta oficial é automatizada por script, depois de um [piloto](#piloto) manual que validou o procedimento no DevTools e de um piloto automatizado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões ficam vinculadas a essa versão, máquina, navegador e cargas.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | Servidor HTTP estático local (`python -m http.server 8080`) servindo a pasta `src/main/webapp` do fork, acessado em `http://localhost:8080/?offline=1`. Não há servidor de exportação. |

### Máquina cliente e navegador

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

### Ferramentas

| Ferramenta | Uso |
| --- | --- |
| Script `coletar.py` (Python 3 e Playwright) | Abre o Google Chrome instalado na máquina, executa as operações do [procedimento](#procedimento) e grava um trace do Chrome por operação, com as categorias de eventos do painel Performance do DevTools (tarefas do thread principal, eventos, contadores de memória e capturas de tela). |
| Script `ler_traces.py` (Python 3) | Lê os traces, extrai tempo e heap segundo a [leitura das medidas](#leitura-das-medidas) e gera o CSV de tentativas. Apenas lê os traces, sem alterá-los. |
| Script `gerar_cargas.py` (Python 3) | Gera as cinco cargas sintéticas de forma reprodutível. |
| `Get-FileHash` (PowerShell) | Calcula o SHA-256 das cargas para identificá-las. |
| Chrome DevTools, painel Performance | Usado no piloto manual e para conferir qualquer trace: o CSV registra os instantes `ti` e `tf` usados em cada medida. |

### Condições de execução

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

### Procedimento

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

### Tentativas válidas, falhas e interrupções

Para cada porte e operação são realizadas cinco tentativas válidas. Uma tentativa interrompida por fator externo ao draw.io é descartada, registrada com o motivo e reposta. É considerada **falha** do draw.io a tentativa com erro exibido, travamento da aba, arquivo exportado inválido ou operação que não termina em até duas vezes o limite candidato do cenário (faixa da nota 1 na Fase 2). A automação registra em `brutos/traces/falhas.txt` as operações que não concluem em 180 s ou terminam com erro. Como os limites candidatos ainda dependem de aprovação, o CSV guarda o valor medido de todas as tentativas concluídas; na análise, as que passam de duas vezes o limite são tratadas como falha, contam para a M2.6 e não entram nas medianas de tempo dos sucessos. Essa era a regra inicial da coleta. Para a análise, aplica-se a [revisão pós-coleta de 15/11/2026](../fase-2/niveis-e-julgamento.md#revisao-pos-coleta-do-julgamento-15112026): menos de quatro sucessos por falha do produto resulta em nota temporal 1; a memória é julgada pelas medidas completas das operações concluídas, independentemente da falha temporal. Ausência ou invalidade de dados continua não conclusiva.

### Registro dos dados

Os CSVs, scripts e cargas são versionados em `dados/avaliacao/eficiencia/`. Os traces são preservados em pacotes externos e podem ser restaurados nos caminhos abaixo. O acesso aos pacotes, as instruções de restauração e a conferência dos hashes estão em `dados/avaliacao/eficiencia/README.md`. Os pacotes estão disponíveis na [pasta de evidências no Google Drive](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

| Caminho | Conteúdo |
| --- | --- |
| `cargas/` | As cinco cargas e o script `gerar_cargas.py`. |
| `coletar.py` e `ler_traces.py` | Scripts de coleta e de leitura dos traces. |
| `brutos/tentativas.csv` | Uma linha por operação medida na coleta oficial. |
| `brutos/traces/` | Caminho local dos 125 traces da coleta oficial (`.json.gz`), restaurados do pacote externo e ignorados pelo Git. São nomeados por porte, operação, formato e tentativa, como `p05000_exportar-svg_t3.json.gz`. Na coleta, URLs do tipo `data:` (imagens geradas durante a exportação) são truncadas em 200 caracteres para reduzir o tamanho; o restante do trace não é alterado. |
| `brutos/piloto/` | CSV versionado e caminho local dos 10 traces do piloto automatizado, restaurados do pacote externo. |
| `brutos/piloto/manual/` | CSV versionado e caminho local dos 4 traces do piloto manual, restaurados do pacote externo. |
| `README.md` e `SHA256SUMS.txt` | Orientações de acesso e restauração das evidências e manifesto de integridade. |

Colunas de `tentativas.csv`: `data`, `tentativa`, `porte`, `operacao`, `formato`, `versao_chrome`, `memoria_em_uso_pct`, `tempo_ms`, `heap_mib`, `resultado` (sucesso, falha, descartada ou verificar), `observacao`, `trace`, `ti_ms` e `tf_ms` (instantes de início e fim em ms desde o começo do trace, para conferência no DevTools).

### Piloto

O piloto foi feito em duas etapas, e seus resultados não entram no cálculo das métricas.

**Piloto manual (13 e 14/11/2026).** Gravações no painel Performance do DevTools com a carga de 50 formas: abertura, rótulo e exportação em PNG e PDF. Achados:

- Na abertura, o draw.io usa o seletor nativo da API File System Access, e não há evento `change`; o início da medida foi redefinido.
- Na exportação PNG e SVG há dois diálogos depois de **Export**: o "Save as" do draw.io e o seletor do Windows. O fim da medida foi fixado no "Save as".
- No PDF, o draw.io abre uma página de impressão, e o arquivo é gerado pela impressão do Chrome. O arquivo obtido sai com cabeçalho do navegador (data e título), dividido em 10 páginas e com formas cortadas na borda da página.
- A opção "Include a copy of my diagram" vem marcada por padrão e foi mantida.
- Ao abrir um arquivo pelo seletor nativo, o draw.io pode gravar as alterações de volta nesse arquivo. Durante o piloto, a edição do rótulo foi gravada na carga de 50 formas, que passou a ter um trecho de HTML no rótulo da forma `v0001`. A carga foi restaurada a partir do repositório e conferida antes da coleta oficial desse porte; a automação não grava as cargas.
- A leitura manual de cada gravação é demorada e varia conforme o avaliador; para 125 gravações, optou-se pela automação.

**Piloto automatizado (14/11/2026).** Uma tentativa nos portes extremos (50 e 5.000 formas), suficiente para validar o procedimento e verificar a capacidade; os portes intermediários são cobertos pela coleta oficial. Todas as operações foram concluídas. A exportação SVG com 5.000 formas levou cerca de 118 s, quase três vezes o limite candidato (40 s); as demais operações ficaram muito abaixo dos limites candidatos, o que indica que esses limites são folgados para esta máquina. Eventuais ajustes são decisão do grupo com o requisitante.

**Comparação entre piloto manual e automatizado (50 formas).**

| Operação | Manual (ms) | Automatizado (ms) |
| --- | --- | --- |
| Abrir | 288,7 | 73,9 |
| Rótulo | 118,4 | 39,7 |
| Exportar PNG | 269,6 | 101,5 |
| Exportar PDF | 235,8 | 175,6 |

Os valores manuais são sistematicamente maiores, mas da mesma ordem de grandeza. A gravação manual mantém o DevTools aberto e liga a amostragem de JavaScript (eventos `ProfileChunk` presentes no trace manual), o que acrescenta custo à página; a gravação automatizada não liga essa amostragem. Na abertura, a medida manual inclui ainda a entrega do arquivo pelo seletor nativo. Por medir com menor interferência do instrumento e de forma repetível, adota-se a coleta automatizada.

## Manutenibilidade (Dupla 3)

Esta seção define como serão coletadas as métricas M3.1 e M3.2 da [Fase 2](../fase-2/metricas.md). Toda a coleta é feita e avaliada pela dupla, utilizando a mesma versão do programa de avaliação e do programa avaliado. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões ficam vinculadas a essa versão.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | localmente, conforme o [guia do ambiente](ambiente-drawio.md). |

### Máquina cliente e navegador

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

### Ferramentas

| Ferramenta | Uso |
| --- | --- |
| Sonarclaude | Para a avaliação das funções escolhidas dentro do trabalho |

### Condições de execução

| Condição | Regra |
| --- | --- |
| Perfil do navegador | Janela de convidado do Chrome, sem extensões, sem histórico e sem outras abas abertas. |
| DevTools | Aberto em janela separada, sem limitação de CPU ou de rede. |
| Sessão limpa | Antes de cada sessão, recarregar a página com `Ctrl+Shift+R` e acionar **Coletar lixo** no painel Performance. |
| Máquina | Conectada à energia, modo de energia equilibrado, outros programas fechados e notificações do Windows silenciadas. O percentual de memória em uso no início de cada sessão é registrado. |
| Rede | Instância local com `offline=1`. Sem acesso a serviços em nuvem. |
| Ordem | Portes do menor para o maior; dentro de cada porte, as cinco tentativas são feitas em sequência. |

### Observações encontradas

### Procedimento


### Tentativas válidas, falhas e interrupções


### Registro dos dados

### Piloto

Antes da coleta oficial é feita uma rodada piloto, com uma tentativa por porte e operação, para:

- confirmar os comandos de abertura e exportação na versão fixada;
- identificar, na aba **Rede** do DevTools, se cada formato é gerado no navegador ou depende de um serviço de exportação, como exige o escopo da Fase 1;
- verificar se os limites candidatos da Fase 2 são plausíveis nesta máquina e submeter eventuais ajustes à aprovação do requisitante;
- estimar a duração total da coleta.

Os resultados do piloto são registrados à parte e não entram no cálculo das métricas.