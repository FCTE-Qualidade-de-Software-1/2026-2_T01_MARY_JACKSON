# Escopo e profundidade

## Produto, versão e ambiente alvo

O recorte proposto é o **draw.io web, versão 32.2.0, hospedado em Docker, em ambiente local de testes**, para apoiar o [cenário de adoção em infraestrutura própria](proposito.md). Essa identificação é o alvo do planejamento, sem pressupor que a instalação ou a coleta já tenham ocorrido.

| Elemento | Delimitação e situação |
|---|---|
| Distribuição e versão alvo | Editor web draw.io 32.2.0. A disponibilidade da imagem correspondente e a versão/build executada precisam ser verificadas. |
| Implantação | Docker, em ambiente local de testes; registrar imagem, tag, digest, configuração e versões dos serviços utilizados antes da coleta. |
| Código-fonte | Fixar a tag ou o commit correspondente à versão avaliada e os arquivos de cada componente antes da análise de Manutenibilidade. |
| Navegador e máquina cliente | Definidos no plano de avaliação (Fase 3, Entrega 2). As condições serão mantidas documentadas e comparáveis entre as medições. |
| Máquina servidora e exportação | Definidas no plano de avaliação (Fase 3, Entrega 2). A configuração inicial do contêiner está em [Ambiente Docker do draw.io](../fase-3/ambiente-drawio.md). |
| Diagramas de referência | Cargas sintéticas planejadas de **50, 300, 1.000, 2.000 e 5.000 formas**; registrar geração, estrutura e identificação dos arquivos. |

Conforme a [descrição do produto](produto.md), a Manutenibilidade será avaliada no código-fonte da versão 32.2.0; a Eficiência de desempenho e a Segurança, no editor web dessa versão. A identificação exata do código e da instalação será registrada antes da coleta.

## Componentes incluídos

O fluxo central é **abrir um diagrama, editar um rótulo e exportar**. A abertura corresponde à operação **Abrir de/Dispositivo**, substituindo o documento atual; o comando deve ser confirmado na instalação de referência. Não se inclui neste recorte a inserção de conteúdo em um diagrama já aberto por colagem ou importação adicional.

| Componente e operação | Segurança | Eficiência de desempenho | Manutenibilidade |
|---|---|---|---|
| **Importação:** abrir arquivo local `.drawio`/`.xml`. | Tratamento de arquivos recebidos de terceiros e proteção dos dados na abertura. | Tempo de abertura e memória JavaScript do editor após abrir. | Analisabilidade do código de leitura e conversão. |
| **Rótulos:** alterar o texto de uma forma e observar sua atualização; considerar o tratamento de conteúdo HTML quando aplicável à análise de Segurança. | Tratamento do conteúdo apresentado nos rótulos. | Tempo de resposta da atualização do texto. | Analisabilidade do código de edição e tratamento dos rótulos. |
| **Exportação:** gerar arquivos **PNG, PDF e SVG**, distinguindo os formatos. | Confidencialidade e integridade na geração e nos serviços efetivamente utilizados. | Tempo de geração e memória JavaScript durante a operação. | Modificabilidade do código relacionado às exportações. |

Os mecanismos de exportação podem envolver dependências além do editor. Deve-se identificar o caminho utilizado por cada formato na versão e na configuração fixadas; não se presume que toda a execução ocorra no navegador. A referência para identificar a implantação é o [repositório oficial Docker do draw.io](https://github.com/jgraph/docker-drawio), conferido na revisão correspondente à imagem utilizada.

## Exclusões e motivos

| Item fora do escopo | Motivo e limite do corte |
|---|---|
| Login e integrações com armazenamento em nuvem | Exigem contas e serviços de terceiros e não fazem parte do fluxo com arquivos locais definido para o cenário. |
| Edição colaborativa em tempo real | Acrescenta usuários simultâneos e dependências que não serão examinados neste recorte. |
| Aplicativo desktop e instância pública `app.diagrams.net` | São ambientes diferentes da instalação web própria proposta. |
| Plugins e extensões opcionais | Introduzem comportamentos e configurações além dos componentes selecionados. As formas usadas nas cargas devem permanecer fixas e documentadas. |
| Incorporação em outros sites e proxy de imagens como recursos independentes | Não serão avaliados isoladamente. Se uma dependência participar da exportação escolhida, seu uso deve ser registrado e considerado dentro desse fluxo. |

## Profundidade da avaliação

A avaliação examinará os três componentes, sem pretender certificar o produto inteiro. Para Eficiência, prevê-se observar o comportamento do fluxo em condições controladas; para Manutenibilidade, analisar o código dos componentes; para Segurança, examinar evidências públicas e os mecanismos pertinentes à versão selecionada, sob responsabilidade da Dupla 1. O detalhamento dos procedimentos pertence às fases seguintes.

Não estão previstas busca de vulnerabilidades inéditas, avaliação de todas as funções ou sessões de testes com usuários. A seleção dessas abordagens não pressupõe que a ferramenta seja segura, rápida ou fácil de manter.

## Limites de validade

- As conclusões ficarão vinculadas à versão, ao código, às configurações, às máquinas, ao navegador e às cargas documentados. Fixar apenas a imagem Docker não controla os recursos da máquina cliente.
- O recorte de memória de Eficiência corresponde ao **heap JavaScript do editor**; ele não representa a RAM total do navegador, da máquina ou de um eventual servidor de exportação.
- A capacidade será limitada ao maior porte aprovado **entre os cinco ensaiados**, conforme os critérios posteriores. Não representará um máximo absoluto do produto nem será inferida apenas pelo número de formas.
- As cargas sintéticas não abrangem todas as combinações de conteúdo, conectores, estilos e imagens dos diagramas reais.
- Evidências de Segurança precisam identificar fonte, data, componente e aplicabilidade à versão; números de CVE não verificados não fundamentam conclusões.
- A análise de Manutenibilidade ficará restrita ao código selecionado, sem generalizar seus resultados para todo o repositório.

O [modelo de qualidade](modelo-de-qualidade.md) explica as características selecionadas e os compromissos assumidos por esse recorte.
