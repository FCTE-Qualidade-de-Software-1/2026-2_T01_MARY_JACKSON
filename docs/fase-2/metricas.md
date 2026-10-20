# Métricas

<!-- O que entra aqui: para cada métrica: definição, fórmula, fonte, procedimento de coleta e escala. Partir das medidas da ISO/IEC 25023. Rubrica F2-C4. -->

## Segurança (Dupla 1)

## Eficiência de desempenho (Dupla 2)

Foram selecionadas seis métricas para responder às quatro questões estabelecidas. Para cada porte e operação/formato, serão realizadas cinco tentativas válidas; interrupções externas serão registradas e repostas. Para M2.1 a M2.5, calcula-se a mediana das quatro ou cinco tentativas bem-sucedidas com dados completos; menos de quatro sucessos tornam o cenário não conclusivo. Falhas não recebem valores artificiais de tempo ou memória.

### M2.1: Tempo de abertura

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Comportamento temporal. |
| Questão associada | Q2.1. |
| Componente | Importação (abertura de arquivo). |
| Definição | Tempo da confirmação de abertura até o diagrama estável e interativo. |
| Cálculo | `M2.1 = mediana(tf - ti)`, por porte. |
| Fonte | Vídeo/trace; ms. |
| Coleta | Abrir o arquivo de cada porte por Abrir de/Dispositivo, substituindo o documento atual, sem incluir digitação ou navegação humana nos seletores. |

### M2.2: Heap após a abertura

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Utilização de recursos. |
| Questão associada | Q2.1. |
| Componente | Importação (abertura de arquivo). |
| Definição | Heap JS usado 2 s após a estabilização da abertura. |
| Cálculo | `M2.2 = mediana(heap 2 s após a abertura)`, por porte. |
| Fonte | DevTools; MiB. |
| Coleta | Registrar o heap JS na mesma tentativa de M2.1; valores em bytes são convertidos por `MiB = bytes / 2^20`. |

### M2.3: Latência do rótulo

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Comportamento temporal. |
| Questão associada | Q2.2. |
| Componente | Rótulos. |
| Definição | Latência da confirmação do novo rótulo até sua renderização estável. |
| Cálculo | `M2.3 = mediana(tf - ti)`, por porte. |
| Fonte | Vídeo/trace; ms. |
| Coleta | Na forma v0001, alterar o rótulo de Rotulo 0001 para Rotulo A001. |

### M2.4: Tempo de exportação

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Comportamento temporal. |
| Questão associada | Q2.3. |
| Componente | Exportação PNG, PDF e SVG. |
| Definição | Tempo da confirmação final da exportação até o arquivo íntegro disponível. |
| Cálculo | `M2.4 = mediana(tf - ti)`, por porte e formato. |
| Fonte | Vídeo/arquivo; ms. |
| Coleta | Exportar cada formato separadamente e validar o arquivo gerado no formato solicitado. |

### M2.5: Pico de heap na exportação

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Utilização de recursos. |
| Questão associada | Q2.3. |
| Componente | Exportação PNG, PDF e SVG. |
| Definição | Máximo do heap JS na janela de M2.4. |
| Cálculo | `M2.5 = mediana(picos de heap)`, por porte e formato. |
| Fonte | DevTools; MiB. |
| Coleta | Registrar o maior valor do heap JS durante cada exportação de M2.4; valores em bytes são convertidos por `MiB = bytes / 2^20`. |

### M2.6: Maior porte aprovado

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Capacidade. |
| Questão associada | Q2.4. |
| Componente | Fluxo completo (abrir, rótulo e exportar PNG, PDF e SVG). |
| Definição | Maior porte com ao menos 4/5 sucessos em cada operação. |
| Cálculo | `M2.6 = maior porte com >= 4/5 sucessos em cada operação`. |
| Fonte | CSV/arquivos; formas. |
| Coleta | Ensaiar os cinco portes e consolidar os sucessos e falhas registrados nas tentativas de M2.1 a M2.5. |

**Nota:** `tf` e `ti` representam os instantes final e inicial de cada operação; a mediana é calculada sobre as tentativas bem-sucedidas de cada cenário. Os cinco arquivos sintéticos serão identificados por hash, e versão/build, navegador, hardware, cache e opções de exportação serão registrados.

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
