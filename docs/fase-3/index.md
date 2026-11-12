# Fase 3: Projetar a avaliação

<!-- O que entra aqui: plano de avaliação: método, instruções para o avaliador, recursos e cronograma (Aula 07, págs. 18 e 19). Entrega 2. -->

O ambiente de execução previsto para a avaliação é o draw.io web 32.2.0 em Docker local. Consulte o [guia do ambiente Docker](ambiente-drawio.md) para iniciar e operar o contêiner.


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