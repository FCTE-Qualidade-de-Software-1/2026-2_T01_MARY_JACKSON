# Objetivos, questões e hipóteses

<!-- O que entra aqui: um objetivo por característica no template GQM (Aula 08, pág. 24), as questões de cada objetivo e uma hipótese por questão. As abstraction sheets das duplas podem entrar aqui (Aula 08, pág. 29). Rubrica F2-C1 a C3. -->


## Segurança (Dupla 1)

### Objetivo de medição
 
| Elemento | Descrição |
| --- | --- |
| Identificador | G1 |
| Objeto | Componentes de importação de arquivos, tratamento de rótulos e _proxy_ de exportação do _draw.io_. |
| Propósito | Avaliar a segurança dos componentes selecionados. |
| Foco | Confidencialidade, integridade e resistência. |
| Ponto de vista | Diretoria de TI da empresa júnior. |
| Contexto | _Draw.io_ web, versão 32.2.0, hospedado em Docker, em ambiente local de testes. |

### Questões e hipóteses
 
As questões e hipóteses foram definidas para orientar a avaliação da segurança dos três componentes selecionados. As questões Q1.1 a Q1.3 verificam as correções das vulnerabilidades conhecidas, uma por componente; Q1.4 e Q1.5 avaliam a qualidade da proteção dos rótulos. A resistência entra porque a correção da CVE-2026-46642 foi contornada por uma variação do ataque ([GHSA-c76x-r78m-phwx](https://github.com/jgraph/drawio/security/advisories/GHSA-c76x-r78m-phwx)). As hipóteses serão verificadas na E2.
 
| Questão | Hipótese |
| --- | --- |
| **Q1.1**<br>O componente de importação de arquivos bloqueia a execução de _scripts_ maliciosos embutidos na abertura de diagramas? | **H1.1**<br>O sistema de importação impede a execução automática de _scripts_ no momento da carga inicial do arquivo (M1.1 = 100%). |
| **Q1.2**<br>O tratamento de rótulos das formas sanitiza adequadamente o texto dos rótulos, inclusive o de diagramas recebidos de terceiros? | **H1.2**<br>A camada de apresentação limpa os caracteres especiais e _tags_ HTML nos rótulos e metadados, impedindo a persistência de injeções de código (M1.1 = 100%). |
| **Q1.3**<br>O servidor _proxy_ de exportação restringe solicitações de acesso não autorizado a caminhos de diretórios? | **H1.3**<br>O _proxy_ valida e restringe as rotas nas requisições de saída, impedindo ataques de _Path Traversal_ (M1.1 = 100%). |
| **Q1.4**<br>Nos componentes avaliados, todos os trechos do código que exibem o rótulo de uma forma como HTML aplicam sanitização ou escape antes? | **H1.4**<br>Todos esses trechos aplicam proteção na versão 32.2.0, ao contrário do trecho que originou a CVE-2026-46642 (M1.2 = 100%). |
| **Q1.5**<br>A proteção dos rótulos resiste a variações dos ataques conhecidos, incluindo combinações de formas com estilos diferentes, como no contorno registrado na CVE-2026-58504? | **H1.5**<br>Nenhuma das variações testadas executa código na abertura do arquivo (M1.3 = 100%). |

## Eficiência de desempenho (Dupla 2)

### Objetivo de medição

| Elemento | Descrição |
| --- | --- |
| Identificador | G2 |
| Objeto | Fluxo de abrir diagramas, editar rótulos e exportar (PNG, PDF e SVG) do _draw.io_ 32.2.0. |
| Propósito | Avaliar tempo, memória e capacidade. |
| Foco | Comportamento temporal, utilização de recursos e capacidade. |
| Ponto de vista | Usuários que produzem diagramas e avaliadores. |
| Contexto | Editor web em ambiente documentado e cinco cargas sintéticas definidas (50, 300, 1.000, 2.000 e 5.000 formas). |

### Questões e hipóteses

As questões e hipóteses derivam das necessidades R-ED-01 a R-ED-04 da [Fase 1](../fase-1/partes-interessadas.md). As hipóteses serão verificadas na E2.

| Questão | Hipótese |
| --- | --- |
| **Q2.1**<br>Como a abertura se comporta em tempo e memória quando o porte aumenta? | **H2.1**<br>Ambos crescem com a carga, respeitando os limites aprovados. |
| **Q2.2**<br>A edição de rótulos permanece responsiva com mais formas? | **H2.2**<br>A latência cresce, mas atende ao limite de cada carga. |
| **Q2.3**<br>Como PNG, PDF e SVG diferem em tempo e pico de memória? | **H2.3**<br>Os custos variam por formato e atendem aos limites por carga. |
| **Q2.4**<br>Qual o maior porte com fluxo completo repetível? | **H2.4**<br>Com 5.000 formas, cada uma das cinco operações terá pelo menos quatro sucessos em cinco tentativas válidas. |

## Manutenibilidade (Dupla 3)

### Objetivo de medição

| Elemento | Descrição |
| --- | --- |
| Identificador | G3 |
| Objeto | Código-fonte dos componentes de importação de arquivos, edição de rótulos e exportação PNG/PDF/SVG do _draw.io_. |
| Propósito | Avaliar a manutenibilidade dos componentes selecionados. |
| Foco | Analisabilidade e modificabilidade. |
| Ponto de vista | Desenvolvedores responsáveis pela manutenção do software. |
| Contexto | Manutenção e evolução dos componentes selecionados do _draw.io_, versão 32.2.0. |

### Questões e hipóteses

As questões e hipóteses foram definidas para orientar a avaliação da manutenibilidade dos três componentes selecionados.

| Questão | Hipótese |
| --- | --- |
| **Q3.1**<br>Em que medida a complexidade do código responsável pela leitura e conversão de arquivos pode dificultar sua compreensão e manutenção? | **H3.1**<br>O código de importação apresenta complexidade cognitiva média inferior ou igual a 10 por função. |
| **Q3.2**<br>Em que medida a complexidade do código responsável pela edição e formatação de rótulos pode dificultar sua compreensão e manutenção? | **H3.2**<br>O código de edição de rótulos apresenta complexidade cognitiva média inferior ou igual a 10 por função. |
| **Q3.3**<br>Em que medida a duplicação de código entre as implementações de exportação PNG, PDF e SVG pode dificultar futuras modificações? | **H3.3**<br>O percentual de código duplicado no escopo de exportação é inferior ou igual a 5%. |
