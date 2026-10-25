# Métricas

<!-- O que entra aqui: para cada métrica: definição, fórmula, fonte, procedimento de coleta e escala. Partir das medidas da ISO/IEC 25023. Rubrica F2-C4. -->

## Segurança (Dupla 1)

Foram selecionadas três métricas para responder às cinco questões estabelecidas. A primeira é aplicada separadamente aos componentes de importação, rótulos e _proxy_ de exportação; a segunda, ao código que exibe os rótulos; e a terceira, às variações dos ataques conhecidos. M1.1 e M1.3 são coletadas por testes em ambiente local, e M1.2, por inspeção do código-fonte. As métricas seguem a forma de proporção (`X = A / B`) adotada pela ISO/IEC 25023 para as medidas de segurança (seção 8.6, p. 26–27, versão de trabalho de 2011 disponibilizada na disciplina): M1.1 e M1.3 foram adaptadas de *Access controllability* (8.6.1, p. 27) e seguem a recomendação de testes de penetração da Nota 1 da seção 8.6 (p. 26); M1.2 foi adaptada de *Data corruption prevention* (8.6.2, p. 27), contando trechos protegidos em vez de danos ocorridos. Karnouskos et al. (2018, p. 5, Seção F) descrevem essas medidas da norma e mostram que algumas podem ser verificadas antes da implantação, por lista de verificação. As ferramentas de apoio à coleta serão definidas no plano de avaliação da Fase 3.

### M1.1 — Taxa de bloqueio de casos de teste das vulnerabilidades conhecidas

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Confidencialidade e integridade. |
| Questões associadas | Q1.1, Q1.2 e Q1.3. |
| Componentes | Importação, rótulos e _proxy_ de exportação, analisados separadamente. |
| Definição | Percentual de casos de teste maliciosos bloqueados pelo componente, construídos a partir dos cenários descritos nos avisos de segurança das CVE-2026-46642, CVE-2026-58504 e CVE-2026-63416. |
| Cálculo | `M1.1 = (Cb / Ct) x 100` |
| Fonte | Registro dos testes e console do navegador; avisos de segurança do GitHub ([GHSA-fqhg-287p-c6vf](https://github.com/jgraph/drawio/security/advisories/GHSA-fqhg-287p-c6vf), [GHSA-c76x-r78m-phwx](https://github.com/jgraph/drawio/security/advisories/GHSA-c76x-r78m-phwx)) e NVD ([CVE-2026-63416](https://nvd.nist.gov/vuln/detail/CVE-2026-63416)). |
| Coleta | No ambiente de teste local definido no plano de avaliação (Fase 3), sem acesso à rede externa, executar os casos de teste de cada componente, cada um em sessão limpa do navegador. O repositório registra a descrição de cada caso e o resultado, sem publicar os arquivos de ataque. |

### M1.2 — Cobertura da proteção dos rótulos

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Integridade. |
| Questão associada | Q1.4. |
| Componente | Rótulos. |
| Definição | Percentual de trechos que aplicam sanitização ou escape antes de exibir o rótulo como HTML. |
| Cálculo | `M1.2 = (Pp / Pt) x 100` |
| Fonte | Código-fonte da tag v32.2.0. |
| Coleta | Localizar as chamadas `getLabelValue` em `Format.js`, `Graph.js` e `Editor.js` e verificar se o valor passa por `Graph.sanitizeHtml` ou `mxUtils.htmlEntities`; registrar arquivo e linha de cada trecho. |

### M1.3 — Taxa de bloqueio de variações dos ataques conhecidos

| Campo | Descrição |
| --- | --- |
| Subcaracterística | Resistência: grau em que o produto ou sistema mantém o funcionamento enquanto está sob ataque de um agente malicioso (ISO/IEC 25010:2023, conforme ISO 25000 Portal). |
| Questão associada | Q1.5. |
| Componentes | Importação e rótulos. |
| Definição | Percentual de variações dos ataques das CVE-2026-46642 e CVE-2026-58504 bloqueadas. |
| Cálculo | `M1.3 = (Wb / Wt) x 100` |
| Fonte | Registro dos testes e console do navegador. |
| Coleta | No ambiente de teste local definido no plano de avaliação (Fase 3), sem acesso à rede externa, executar variações do conteúdo do rótulo e da combinação de estilos das formas (HTML ou texto simples, editável ou não), cada uma em sessão limpa do navegador. O repositório registra a descrição de cada variação e o resultado, sem publicar os arquivos de ataque. |

**Nota:** `Cb` representa os casos de teste bloqueados e `Ct` o total de casos de teste aplicados ao componente; `Pp`, os trechos protegidos e `Pt`, o total de trechos que exibem o rótulo como HTML; `Wb`, as variações bloqueadas e `Wt`, o total de variações testadas.

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
