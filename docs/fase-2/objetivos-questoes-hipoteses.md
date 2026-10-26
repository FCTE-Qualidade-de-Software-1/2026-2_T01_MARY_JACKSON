# Objetivos, questões e hipóteses

<!-- O que entra aqui: um objetivo por característica no template GQM (Aula 08, pág. 24), as questões de cada objetivo e uma hipótese por questão. As abstraction sheets das duplas podem entrar aqui (Aula 08, pág. 29). Rubrica F2-C1 a C3. -->
Cada característica priorizada na [Fase 1](../fase-1/caracteristicas.md) gera um objetivo de medição, escrito no template do GQM: **Analisar** o objeto, **para o propósito de** entender, melhorar ou controlar, **com respeito a** um foco de qualidade, **do ponto de vista de** uma parte interessada, **no contexto de** um ambiente. O objeto dos três objetivos é o _draw.io_; os componentes avaliados aparecem nas questões. O propósito é **entender** o nível de qualidade do produto, porque os resultados apoiam a decisão de adoção descrita no [Propósito da avaliação](../fase-1/proposito.md). O ponto de vista de cada objetivo vem das [partes interessadas](../fase-1/partes-interessadas.md) da Fase 1. Versão, instalação e ambiente de execução fazem parte do plano de avaliação (Fase 3).

## Segurança (Dupla 1)

### Objetivo de medição
 
| Elemento | Descrição |
| --- | --- |
| Identificador | G1 |
| Analisar | O software _draw.io_. |
| Para o propósito de | Entender. |
| Com respeito a | Segurança (confidencialidade, integridade e resistência). |
| Do ponto de vista de | Diretoria de TI. |
| No contexto de | adoção do draw.io por uma empresa júnior de software. |

**G1:** Analisar o _draw.io_ para o propósito de entender, com respeito à segurança (confidencialidade, integridade e resistência), do ponto de vista da diretoria de TI, no contexto da disciplina Qualidade de Software 1, no cenário da empresa júnior.

### Questões e hipóteses
 
As questões e hipóteses foram definidas para orientar a avaliação da segurança dos três componentes selecionados. As questões Q1.1 a Q1.3 verificam as correções das vulnerabilidades conhecidas, uma por componente; Q1.4 e Q1.5 avaliam a qualidade da proteção dos rótulos. A resistência entra porque a correção da CVE-2026-46642 foi contornada por uma variação do ataque ([GHSA-c76x-r78m-phwx](https://github.com/jgraph/drawio/security/advisories/GHSA-c76x-r78m-phwx)). As hipóteses serão verificadas na E2.
 
| Questão | Hipótese |
| --- | --- |
| **Q1.1**<br>Qual a taxa de bloqueio de arquivos de teste com conteúdo malicioso na importação de diagramas? | **H1.1**<br>O componente de importação bloqueia a totalidade dos cenários de teste aplicados (M1.1 = 100%). |
| **Q1.2**<br>Qual a taxa de bloqueio de rótulos de teste com conteúdo malicioso na exibição das formas? | **H1.2**<br>O tratamento de rótulos sanitiza o conteúdo e bloqueia todos os casos de teste aplicados (M1.1 = 100%). |
| **Q1.3**<br>Qual a taxa de bloqueio de requisições de teste com caminhos indevidos ao _proxy_ de exportação? | **H1.3**<br>O _proxy_ de exportação rejeita todas as requisições de teste com caminhos indevidos (M1.1 = 100%). |
| **Q1.4**<br>Qual a proporção de trechos de código que exibem rótulos de formas em HTML com aplicação prévia de sanitização ou escape? | **H1.4**<br>Todos esses trechos aplicam proteção na versão avaliada, ao contrário do trecho que originou a CVE-2026-46642 (M1.2 = 100%). |
| **Q1.5**<br>Qual a taxa de resistência da proteção de rótulos frente a variações de ataques conhecidos, incluindo combinações de formas com estilos distintos? | **H1.5**<br>Nenhuma das variações testadas executa código na abertura do arquivo (M1.3 = 100%). |

## Eficiência de desempenho (Dupla 2)

### Objetivo de medição

| Template GQM | G2 |
| --- | --- |
| Analisar | O _draw.io_. |
| Para o propósito de | Entender. |
| Com respeito a | Eficiência de desempenho (comportamento temporal, utilização de recursos e capacidade). |
| Do ponto de vista de | Usuários finais da empresa júnior (desenvolvedores, analistas e gerentes de projeto). |
| No contexto de | Disciplina Qualidade de Software 1, em cenário hipotético de adoção do _draw.io_ por uma empresa júnior de software. |

**G2:** Analisar o _draw.io_ para o propósito de entender, com respeito à eficiência de desempenho (comportamento temporal, utilização de recursos e capacidade), do ponto de vista dos usuários finais da empresa júnior, no contexto da disciplina Qualidade de Software 1.

### Questões e hipóteses

As questões e hipóteses foram definidas para orientar a avaliação da eficiência de desempenho dos três componentes selecionados. As hipóteses serão verificadas na E2.

| Questão | Hipótese |
| --- | --- |
| **Q2.1**<br>Como o tempo de abertura e o consumo de memória variam à medida que o porte do diagrama aumenta? | **H2.1**<br>Ambos crescem com o porte, mas permanecem dentro dos limites de cada carga (nota 4 ou 5 em M2.1 e M2.2). |
| **Q2.2**<br>Em que medida a edição de rótulos permanece responsiva à medida que o número de formas aumenta? | **H2.2**<br>A latência cresce com o porte, mas atende ao limite de cada carga (nota 4 ou 5 em M2.3). |
| **Q2.3**<br>Como os formatos PNG, PDF e SVG diferem em tempo de exportação e pico de memória? | **H2.3**<br>Os custos variam por formato, e todos atendem aos limites de cada carga (nota 4 ou 5 em M2.4 e M2.5). |
| **Q2.4**<br>Qual o maior porte de diagrama em que o fluxo abrir, editar e exportar é concluído de forma repetível? | **H2.4**<br>Com 5.000 formas, cada uma das cinco operações terá pelo menos quatro sucessos em cinco tentativas válidas (M2.6 = 5.000 formas). |

## Manutenibilidade (Dupla 3)

### Objetivo de medição

| Template GQM | G3 |
| --- | --- |
| Analisar | O _draw.io_. |
| Para o propósito de | Entender. |
| Com respeito a | Manutenibilidade (analisabilidade e modificabilidade). |
| Do ponto de vista de | Equipe Mary Jackson, responsável por realizar a avaliação. |
| No contexto de | Disciplina Qualidade de Software 1, no cenário hipotético de adoção do _draw.io_ por uma empresa júnior de software. |

**G3:** Analisar o _draw.io_ para o propósito de entender, com respeito à manutenibilidade (analisabilidade e modificabilidade), do ponto de vista da equipe Mary Jackson, responsável pela avaliação, no contexto da disciplina Qualidade de Software 1 e do cenário hipotético de adoção por uma empresa júnior de software.

### Questões e hipóteses

As questões e hipóteses foram definidas para orientar a avaliação da manutenibilidade dos três componentes selecionados.

| Questão | Hipótese |
| --- | --- |
| **Q3.1**<br>Em que medida a complexidade do código responsável pela leitura e conversão de arquivos pode dificultar sua compreensão e manutenção? | **H3.1**<br>O código de importação apresenta complexidade cognitiva média inferior ou igual a 10 por função.(M3.1 < 10 ) |
| **Q3.2**<br>Em que medida a complexidade do código responsável pela edição e formatação de rótulos pode dificultar sua compreensão e manutenção? | **H3.2**<br>O código de edição de rótulos apresenta complexidade cognitiva média inferior ou igual a 10 por função.(M3.1 < 10) |
| **Q3.3**<br>Em que medida a duplicação de código entre as implementações de exportação PNG, PDF e SVG pode dificultar futuras modificações? | **H3.3**<br>O percentual de código duplicado no escopo de exportação é inferior ou igual a 5%.(M3.2 < 5%) |
