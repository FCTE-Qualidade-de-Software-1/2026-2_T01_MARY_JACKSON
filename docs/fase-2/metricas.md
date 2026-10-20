# Métricas

<!-- O que entra aqui: para cada métrica: definição, fórmula, fonte, procedimento de coleta e escala. Partir das medidas da ISO/IEC 25023. Rubrica F2-C4. -->

## Segurança (Dupla 1)

## Eficiência de desempenho (Dupla 2)

## Manutenibilidade (Dupla 3)

Foram selecionadas duas métricas para responder às três questões estabelecidas. A primeira será aplicada separadamente aos componentes de importação de arquivos e edição de rótulos; a segunda, ao código responsável pela exportação de arquivos. A coleta será realizada por análise estática utilizando o SonarCloud.

### M3.1 — Complexidade cognitiva média por função

| Campo               | Descrição                                                                                                                                                                      |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Subcaracterística   | Analisabilidade.                                                                                                                                                               |
| Questões associadas | Q3.1 e Q3.2.                                                                                                                                                                   |
| Componentes         | Importação de arquivos e edição de rótulos, analisados separadamente.                                                                                                          |
| Definição           | Média da complexidade cognitiva das funções pertencentes ao componente analisado.                                                                                              |
| Cálculo             | `M3.1 = C / F`                                                                                                                                                                 |
| Fonte               | SonarCloud.                                                                                                                                                                    |
| Coleta              | Identificar as funções pertencentes a cada componente e registrar a complexidade cognitiva total e a quantidade de funções, separadamente para importação e edição de rótulos. |

### M3.2 — Percentual de código duplicado

| Campo             | Descrição                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Subcaracterística | Modificabilidade.                                                                                                              |
| Questão associada | Q3.3.                                                                                                                          |
| Componente        | Código de exportação PNG, PDF e SVG.                                                                                           |
| Definição         | Percentual de linhas duplicadas em relação ao total de linhas analisadas no código de exportação.                              |
| Cálculo           | `M3.2 = (Ld / Lt) x 100`                                                                                                       |
| Fonte             | SonarCloud.                                                                                                                    |
| Coleta            | Analisar conjuntamente os arquivos de exportação e registrar a quantidade de linhas duplicadas e o total de linhas analisadas. |

**Nota:** `C` representa a complexidade cognitiva total das funções analisadas; `F`, a quantidade de funções; `Ld`, as linhas duplicadas; e `Lt`, o total de linhas analisadas no escopo de exportação.
