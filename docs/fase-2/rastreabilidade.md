# Rastreabilidade

<!-- Rubrica F2-C11: o objetivo de medição (com respeito a e ponto de vista) deve derivar das características priorizadas e dos stakeholders da Fase 1. -->

Esta página mostra como cada objetivo GQM da Fase 2 deriva da Fase 1: da característica priorizada (com sua nota de importância), do stakeholder que dá o ponto de vista e da decisão do requisitante que a avaliação apoia. Os detalhes da Fase 1 estão em [Propósito](../fase-1/proposito.md), [Requisitante e partes interessadas](../fase-1/partes-interessadas.md) e [Características e priorização](../fase-1/caracteristicas.md).

## Fase 1 → objetivos GQM

| Característica (Fase 1) | Importância | Decisão do requisitante | Do ponto de vista de | Com respeito a | Objetivo | Questões | Métricas |
|---|:-:|---|---|---|:-:|---|---|
| Segurança | 5/5 | Liberar ou não a abertura de diagramas de terceiros e o servidor de exportação próprio | Diretoria de TI da empresa júnior | Confidencialidade, integridade e resistência | G1 | Q1.1 a Q1.5 | M1.1 a M1.3 |
| Eficiência de desempenho | 4/5 | Se a ferramenta aguenta os diagramas grandes dos projetos ou se é preciso limitar o tamanho | Usuários finais da empresa júnior | Comportamento temporal, utilização de recursos e capacidade | G2 | Q2.1 a Q2.4 | M2.1 a M2.6 |
| Manutenibilidade | 4/5 | Se é viável manter uma versão própria e aplicar correções | Equipe Mary Jackson, avaliadora | Analisabilidade e modificabilidade | G3 | Q3.1 a Q3.3 | M3.1 e M3.2 |

## Componentes do escopo → questões

Cada componente definido no [escopo](../fase-1/escopo.md) é coberto por uma questão de cada característica.

| Componente | Segurança | Eficiência | Manutenibilidade |
|---|---|---|---|
| Importação (abrir arquivo) | Q1.1 | Q2.1 | Q3.1 |
| Rótulos (texto das formas) | Q1.2, Q1.4 e Q1.5 | Q2.2 | Q3.2 |
| Exportação (PNG, PDF e SVG) | Q1.3 | Q2.3 | Q3.3 |
| Fluxo completo | | Q2.4 | |

## Detalhamento por objetivo

### G1: Segurança

| Questão | Componente | Subcaracterística | Métrica |
|---|---|---|---|
| Q1.1 Em que medida o componente de importação de arquivos previne a execução de _scripts_ maliciosos embutidos durante a abertura de diagramas? | Importação | Confidencialidade e integridade | M1.1 (CVE-2026-46642 e CVE-2026-58504) |
| Q1.2 Qual o percentual de rótulos de formas, inclusive os oriundos de diagramas de terceiros, que são devidamente sanitizados antes da exibição? | Rótulos | Confidencialidade e integridade | M1.1 (CVE-2026-46642 e CVE-2026-58504) |
| Q1.3 Em que medida o servidor _proxy_ de exportação restringe requisições de acesso não autorizado a caminhos de diretórios? | Exportação | Confidencialidade e integridade | M1.1 (CVE-2026-63416) |
| Q1.4 Qual a proporção de trechos de código que exibem rótulos de formas em HTML com aplicação prévia de sanitização ou escape? | Rótulos | Confidencialidade e integridade | M1.2 |
| Q1.5 Qual a taxa de resistência da proteção de rótulos frente a variações de ataques conhecidos, incluindo combinações de formas com estilos distintos? | Rótulos | Resistência | M1.3 | M1.1 (CVE-2026-46642 e CVE-2026-58504) |
| Q1.3 O proxy de exportação restringe o acesso não autorizado a caminhos de diretórios? | Exportação | Confidencialidade e integridade | M1.1 (CVE-2026-63416) |
| Q1.4 Todos os trechos que exibem o rótulo como HTML aplicam sanitização ou escape antes? | Rótulos | Confidencialidade e integridade | M1.2 |
| Q1.5 A proteção dos rótulos resiste a variações dos ataques conhecidos? | Rótulos | Resistência | M1.3 |

### G2: Eficiência de desempenho

| Questão | Componente | Subcaracterística | Métrica |
|---|---|---|---|
| Q2.1 (R-ED-01) Como o tempo de abertura e o consumo de memória variam à medida que o porte do diagrama aumenta? | Importação | Comportamento temporal e utilização de recursos | M2.1 Tempo de abertura e M2.2 Heap após a abertura |
| Q2.2 (R-ED-02) Em que medida a edição de rótulos permanece responsiva à medida que o número de formas aumenta? | Rótulos | Comportamento temporal | M2.3 Latência do rótulo |
| Q2.3 (R-ED-03) Como os formatos PNG, PDF e SVG diferem em tempo de exportação e pico de memória? | Exportação | Comportamento temporal e utilização de recursos | M2.4 Tempo de exportação e M2.5 Pico de heap na exportação |
| Q2.4 (R-ED-04) Qual o maior porte de diagrama em que o fluxo abrir, editar e exportar é concluído de forma repetível? | Fluxo completo | Capacidade | M2.6 Maior porte aprovado |

Os códigos R-ED indicam a necessidade da Fase 1 que originou cada questão.

### G3: Manutenibilidade

| Questão | Componente | Subcaracterística | Métrica |
|---|---|---|---|
| Q3.1 Em que medida a complexidade do código responsável pela leitura e conversão de arquivos pode dificultar sua compreensão e manutenção? | Importação | Analisabilidade | M3.1 Complexidade cognitiva média por função |
| Q3.2 Em que medida a complexidade do código responsável pela edição e formatação de rótulos pode dificultar sua compreensão e manutenção? | Rótulos | Analisabilidade | M3.1 Complexidade cognitiva média por função |
| Q3.3 Em que medida a duplicação de código entre as implementações de exportação PNG, PDF e SVG pode dificultar futuras modificações? | Exportação | Modificabilidade | M3.2 Percentual de código duplicado |


Se alguma prioridade, stakeholder ou necessidade da Fase 1 for revista, as questões, hipóteses, fichas e critérios relacionados devem ser atualizados antes da coleta.