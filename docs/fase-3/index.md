# Fase 3: Projetar a avaliação

<!-- O que entra aqui: plano de avaliação: método, instruções para o avaliador, recursos e cronograma (Aula 07, págs. 18 e 19). Entrega 2. -->

O ambiente de execução previsto para a avaliação é o draw.io web 32.6.10 localmente por meio de um fork feito pelo membro Heyttor Augusto. Consulte o [guia do ambiente local](ambiente-drawio.md) para iniciar e operar o contêiner.


## Eficiência de desempenho (Dupla 2)

Esta seção define como serão coletadas as métricas M2.1 a M2.6 da [Fase 2](../fase-2/metricas.md). Toda a coleta é feita por um único avaliador, em uma única máquina e um único navegador, para que os resultados dos cinco portes sejam comparáveis entre si. Conforme os [limites de validade](../fase-1/escopo.md) da Fase 1, as conclusões ficam vinculadas a essa versão, máquina, navegador e cargas.

### Versão avaliada

| Item | Definição |
| --- | --- |
| Produto | draw.io web, a partir do fork [`H3ytt0r10/drawio`](https://github.com/H3ytt0r10/drawio). |
| Versão | 32.6.10 (arquivo `VERSION` do fork). |
| Commit | `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, o mesmo usado pelas três duplas. |
| Execução | Contêiner local, conforme o [guia do ambiente](ambiente-drawio.md), acessado em `http://localhost:8080/?offline=1`. |

### Máquina cliente e navegador

| Item | Configuração |
| --- | --- |
| Processador | Intel Core i5-1235U (12ª geração), 10 núcleos, 12 processadores lógicos, 1,30 GHz de base. |
| Memória RAM | 16 GB (15,7 GB utilizáveis). |
| Armazenamento | SSD NVMe. |
| Placa de vídeo | Intel Iris Xe (integrada). |
| Sistema operacional | Windows 11, versão 25H2 (build 26200.9974). |
| Navegador | Google Chrome 157.0.8103.79, 64 bits (V8 15.7.112.43). |
| Avaliador | Pedro Ian (Dupla 2). |

Se o Chrome for atualizado durante a coleta, a nova versão é registrada a partir da tentativa em que passou a valer.

### Ferramentas

| Ferramenta | Uso |
| --- | --- |
| Chrome DevTools, painel **Performance**, com a opção **Memory** marcada | Uma gravação por operação. A mesma gravação fornece o tempo (M2.1, M2.3, M2.4) e a curva do heap JS (M2.2, M2.5). Cada gravação é salva como arquivo de trace. |
| Script `gerar_cargas.py` (Python 3) | Gera as cinco cargas sintéticas de forma reprodutível. |
| `Get-FileHash` (PowerShell) | Calcula o SHA-256 das cargas para identificá-las. |
| Planilha CSV | Registro de cada tentativa (ver [Registro dos dados](#registro-dos-dados)). |
| Visualizadores padrão do Windows e o próprio Chrome | Validação dos arquivos PNG, PDF e SVG exportados. |

### Condições de execução

| Condição | Regra |
| --- | --- |
| Perfil do navegador | Janela de convidado do Chrome, sem extensões, sem histórico e sem outras abas abertas. |
| DevTools | Aberto em janela separada, sem limitação de CPU ou de rede. |
| Sessão limpa | Antes de cada sessão, recarregar a página com `Ctrl+Shift+R` e acionar **Coletar lixo** no painel Performance. |
| Máquina | Conectada à energia, modo de energia equilibrado, outros programas fechados e notificações do Windows silenciadas. O percentual de memória em uso no início de cada sessão é registrado. |
| Rede | Instância local com `offline=1`. Sem acesso a serviços em nuvem. |
| Ordem | Portes do menor para o maior; dentro de cada porte, as cinco tentativas são feitas em sequência. |

### Cargas sintéticas

As cargas são geradas pelo script `gerar_cargas.py`. Cada arquivo `.drawio` (XML não compactado) contém N retângulos iguais de 120 x 60 px, dispostos em grade de 50 colunas, sem conectores, imagens ou estilos adicionais. As formas têm identificadores `v0001`, `v0002`, ... e rótulos `Rotulo 0001`, `Rotulo 0002`, ...; a forma `v0001` é a usada na M2.3. A saída é determinística: executar o script novamente gera arquivos com o mesmo SHA-256.

| Porte (formas) | Arquivo | SHA-256 |
| --- | --- | --- |
| 50 | `carga-00050.drawio` | `03d1a23d7dab0002d11be9eff8207e9cdbb5bcd01fa6c862dd564bac8dd7e139` |
| 300 | `carga-00300.drawio` | `229e6dc2f2a4271deb106fe79be3f9f1da14990e560ade53fadf5bc1b459281a` |
| 1.000 | `carga-01000.drawio` | `1e16ccfe0894ec0afa3163cc43e846e1dda9177465ade1684af1a99995234b91` |
| 2.000 | `carga-02000.drawio` | `1de87eea590083ac74e2d59bc86129a50fafd7a8a87396ec8d5cf13bda3d4777` |
| 5.000 | `carga-05000.drawio` | `9c35607e784f835084f3dd505021ab75ddce2c7f3eb870a3f4e0328766096d62` |

### Procedimento

Cada tentativa de um porte é composta por quatro sessões limpas: uma para abertura e rótulo e uma para cada formato de exportação. Separar as exportações evita que a memória de uma operação influencie o pico da seguinte.

**Sessão A: abertura e rótulo (M2.1, M2.2 e M2.3)**

1. Preparar a sessão limpa e iniciar a gravação no painel Performance.
2. Acionar **Arquivo > Abrir de > Dispositivo**, selecionar a carga e confirmar no seletor de arquivos, substituindo o documento atual.
3. Aguardar o diagrama ficar estável e interativo, esperar mais 2 s e parar a gravação.
4. Iniciar nova gravação, selecionar a forma `v0001`, pressionar `F2`, substituir o texto por `Rotulo A001` e confirmar com `Ctrl+Enter`.
5. Aguardar a renderização do novo rótulo e parar a gravação.

**Sessões B, C e D: exportação em PNG, PDF e SVG (M2.4 e M2.5)**

1. Preparar a sessão limpa e abrir a carga (abertura não medida).
2. Acionar **Coletar lixo** e iniciar a gravação.
3. Acionar **Arquivo > Exportar como > (formato)**, manter as opções padrão do draw.io (zoom 100%, sem borda adicional, sem cópia do diagrama embutida) e confirmar.
4. Parar a gravação quando o arquivo estiver disponível nos downloads.
5. Abrir o arquivo exportado e verificar se está íntegro e no formato solicitado.

### Leitura das medidas no trace

| Métrica | Início (`ti`) | Fim (`tf`) | Valor registrado |
| --- | --- | --- | --- |
| M2.1 | Confirmação no seletor de arquivos. | Último quadro renderizado após a última tarefa do thread principal, com o diagrama interativo. | `tf - ti`, em ms. |
| M2.2 | | | Heap JS 2 s após o `tf` de M2.1, em MiB. |
| M2.3 | Tecla `Ctrl+Enter`. | Quadro em que o novo rótulo aparece renderizado e estável. | `tf - ti`, em ms. |
| M2.4 | Clique de confirmação no diálogo de exportação. | Arquivo íntegro disponível nos downloads. | `tf - ti`, em ms. |
| M2.5 | Mesmo `ti` de M2.4. | Mesmo `tf` de M2.4. | Maior valor do heap JS entre `ti` e `tf`, em MiB. |
| M2.6 | | | Consolidado das tentativas de M2.1 a M2.5, conforme a Fase 2. |

Valores do heap em bytes são convertidos por `MiB = bytes / 2^20`.

### Tentativas válidas, falhas e interrupções

Para cada porte e operação são realizadas cinco tentativas válidas. Uma tentativa interrompida por fator externo ao draw.io (notificação, atualização do sistema, outro programa) é descartada, registrada com o motivo e reposta. É considerada **falha** do draw.io a tentativa com erro exibido, travamento da aba, arquivo exportado inválido ou operação que não termina em até duas vezes o limite candidato do cenário (faixa da nota 1 na Fase 2). Falhas contam para a M2.6 e não recebem valores de tempo ou memória. As medianas seguem a regra da Fase 2: quatro ou cinco sucessos com dados completos; menos de quatro torna o cenário não conclusivo.

### Registro dos dados

Os dados ficam em `dados/avaliacao/eficiencia/`:

| Caminho | Conteúdo |
| --- | --- |
| `cargas/` | As cinco cargas e o script `gerar_cargas.py`. |
| `brutos/tentativas.csv` | Uma linha por operação medida. |
| `brutos/traces/` | Traces do DevTools compactados (`.json.gz`), nomeados por porte, operação, formato e tentativa. Arquivos acima de 50 MB ficam na pasta compartilhada da equipe, com link e SHA-256 registrados no CSV. |
| `brutos/exportados/` | Os arquivos exportados de uma tentativa por porte e formato, como amostra da validação. |

Colunas de `tentativas.csv`: `data`, `tentativa`, `porte`, `operacao`, `formato`, `versao_chrome`, `memoria_em_uso_pct`, `tempo_ms`, `heap_mib`, `resultado` (sucesso, falha ou descartada), `observacao`, `trace`.

### Piloto

Antes da coleta oficial é feita uma rodada piloto, com uma tentativa por porte e operação, para:

- confirmar os comandos de abertura e exportação na versão fixada;
- identificar, na aba **Rede** do DevTools, se cada formato é gerado no navegador ou depende de um serviço de exportação, como exige o escopo da Fase 1;
- verificar se os limites candidatos da Fase 2 são plausíveis nesta máquina e submeter eventuais ajustes à aprovação do requisitante;
- estimar a duração total da coleta.

Os resultados do piloto são registrados à parte e não entram no cálculo das métricas.

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
| SonarCloud | Análise estática do código selecionado para coletar a complexidade cognitiva (M3.1) e o percentual de código duplicado (M3.2). |

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

A análise de manutenibilidade utiliza duas medidas: a complexidade cognitiva média por função, calculada separadamente para importação de arquivos e edição de rótulos, e o percentual de código duplicado no conjunto de exportação PNG, PDF e SVG. Os resultados se restringem ao código selecionado, conforme o [escopo da avaliação](../fase-1/escopo.md).

Segundo o relato da dupla, houve uma única falha na configuração do SonarCloud; após a correção, as demais execuções ocorreram sem problemas. <!-- Falar aqui sobre observações encontradas sobre os dados brutos do sonarclolud, se houver. -->

### Procedimento

O procedimento segue as [fichas das métricas](../fase-2/metricas.md#manutenibilidade-dupla-3), com análise estática pelo SonarCloud e julgamento separado para cada questão do GQM.

**Preparação da análise**

1. Utilizar o código do fork `H3ytt0r10/drawio`, versão `32.6.10`, no commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`.
2. Identificar e registrar os arquivos e as funções de importação de arquivos, edição de rótulos e exportação PNG, PDF e SVG que compõem o recorte avaliado.
3. Configurar o projeto no SonarCloud, conferir o escopo e as exclusões da análise e registrar a configuração utilizada, a identificação da execução e o commit analisado.
4. Executar a análise e conferir sua conclusão e a presença das medidas necessárias no relatório. Corrigir eventuais erros de configuração e repetir a execução antes de utilizar os resultados.

**Coleta e cálculo das métricas**

1. Para a **M3.1**, registrar a complexidade cognitiva total (`C`) e a quantidade de funções (`F`) pertencentes a cada componente. Calcular `M3.1 = C / F` separadamente para importação (**Q3.1**) e edição de rótulos (**Q3.2**), considerando todas as funções do recorte, inclusive as que não geram alertas.
2. Para a **M3.2**, analisar conjuntamente o código de exportação PNG, PDF e SVG e registrar as linhas duplicadas (`Ld`) e o total de linhas analisadas (`Lt`). Calcular `M3.2 = (Ld / Lt) × 100`, respondendo à **Q3.3**, sem fazer a média dos percentuais individuais dos arquivos.
3. Registrar os valores brutos, os arquivos e funções considerados e a referência ao relatório na [coleta de dados](coleta-de-dados.md#manutenibilidade-dupla-3), permitindo conferir os cálculos.
4. Comparar os resultados com os [níveis de julgamento da Fase 2](../fase-2/niveis-e-julgamento.md#manutenibilidade-dupla-3): para M3.1, adequado até 10, atenção acima de 10 até 15 e crítico acima de 15; para M3.2, adequado até 5%, atenção acima de 5% até 10% e crítico acima de 10%. Registrar o julgamento de cada questão na [análise dos resultados](resultados.md#manutenibilidade-dupla-3).

### Tentativas válidas, falhas e interrupções

Uma execução é considerada **válida** quando a análise do SonarCloud termina com sucesso, corresponde ao commit e ao escopo definidos e fornece os dados necessários ao cálculo da métrica. Para M3.1, é necessário `F > 0`; para M3.2, `Lt > 0`. A ausência de dados não é registrada como valor zero: o resultado permanece pendente até que a coleta seja completada.

Segundo o relato da dupla, ocorreu **uma única tentativa com falha**, causada por erro na configuração do SonarCloud. Essa tentativa foi desconsiderada para o cálculo das métricas e a análise foi executada novamente após a correção. As demais execuções ocorreram normalmente, sem outras falhas ou interrupções relatadas. O incidente é registrado como falha da configuração da coleta, sem atribuí-lo à qualidade do código do draw.io.

Como a coleta é feita por análise estática, não se aplica a repetição de cinco tentativas nem o cálculo de medianas adotados pela Dupla 2. Uma nova execução é necessária quando houver falha, dados incompletos ou alteração do commit, do escopo ou da configuração; nesse último caso, os resultados devem ser identificados separadamente.

### Registro dos dados

### Piloto

Antes da coleta oficial é feita uma rodada piloto, com uma tentativa por porte e operação, para:

- confirmar os comandos de abertura e exportação na versão fixada;
- identificar, na aba **Rede** do DevTools, se cada formato é gerado no navegador ou depende de um serviço de exportação, como exige o escopo da Fase 1;
- verificar se os limites candidatos da Fase 2 são plausíveis nesta máquina e submeter eventuais ajustes à aprovação do requisitante;
- estimar a duração total da coleta.

Os resultados do piloto são registrados à parte e não entram no cálculo das métricas.
