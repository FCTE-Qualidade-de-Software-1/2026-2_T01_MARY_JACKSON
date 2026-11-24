# Planejamento de Sprints - Projeto Avaliação da Qualidade do draw.io

> Este documento registra o **planejado**. O realizado (responsáveis, horas reais e datas de conclusão) está nas [issues por sprint](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/milestones), a comparação entre os dois no [Registro de medições](registro-de-medicoes.md) e os gráficos no [Dashboard do PSM](dashboard.md).

## Visão geral

- **Projeto:** Avaliação da Qualidade de Componentes do draw.io
- **Período:** 07/10/2026 a 22/11/2026 (Entrega 1 em 26/10; Entrega 2 em 22/11)
- **Objetivo geral:** avaliar a segurança, a eficiência de desempenho e a manutenibilidade dos componentes de importação de arquivos, rótulos e exportação do draw.io (versão 32.6.10, commit c72c9a9), seguindo o processo de avaliação da ISO/IEC 25040, o método GQM e o acompanhamento do projeto com PSM/CID.
- **Equipe:** três duplas, que dividem integralmente as responsabilidades da dupla.

| Dupla | Integrantes | Responsabilidades |
|---|---|---|
| 1 | Yasmin e Miquéias | Segurança; gestão do projeto (PSM/CID); Introdução e Metodologia; ODS |
| 2 | Pedro Ian e Thiago | Eficiência de desempenho; Fase 1; modelo de qualidade e priorização; GitPage |
| 3 | Heyttor e Lucas | Manutenibilidade; descrição do draw.io e diagrama de contexto; relatório no Overleaf |

## Cronograma

| Sprint | Período | Objetivo | Entregáveis |
|---|---|---|---|
| 1 - Fase 1 | 14/10 a 19/10 | Definir propósito, produto, componentes, stakeholders e características priorizadas | Escopo aprovado; Fase 1 no relatório e na GitPage; linha de base do PSM; Atas 01 e 02 |
| 2 - Fase 2 | 20/10 a 22/10 | Derivar objetivos, questões, hipóteses e métricas (GQM) | Fase 2 no relatório e na GitPage; diagrama GQM; rastreabilidade Fase 1 → Fase 2 |
| 3 - Entrega 1 | 23/10 a 26/10 | Integrar e revisar o relatório e a GitPage e publicar a E1 | Relatório (1ª versão); GitPage até a Fase 2; tabela de contribuição; release E1 |
| 4 - Fases 3 e 4 | 07/11 a 16/11 | Projetar a avaliação (Fase 3) e executá-la: coleta dos dados brutos e análise parcial (Fase 4) | Plano de avaliação na Fase 3; medidas e análise parcial na Fase 4; resultados no artigo; Medição 4 |
| 5 - Entrega 2 | 17/11 a 22/11 | Revisar e publicar a E2 | Relatório final com as Fases 3 e 4; GitPage atualizada; release E2 |

## Estimativa de horas

As estimativas são definidas por cada integrante para as próprias tarefas e formam a linha de base do PSM. Na E2, elas vêm do campo "Estimativa (horas)" de cada issue.

| Entrega | Sprint | Dupla 1 | Dupla 2 | Dupla 3 | Total |
|---|---|---|---|---|---|
| E1 | 1 | 7 | 13 | 3,5 | 23,5 |
| E1 | 2 | 7 | 14 | 7,5 | 28,5 |
| E1 | 3 | 6,5 | 9 | 3 | 18,5 |
| **E1** | **Total** | **20,5** | **36** | **14** | **70,5** |
| E2 | 4 | 20,5 | 9 | 12 | 41,5 |
| E2 | 5 | — | — | — | sem tarefas planejadas |
| **E2** | **Total** | **20,5** | **9** | **12** | **41,5** |

**Previsão calibrada para a E2:** prevista na Medição 3 (multiplicar a linha de base da E2 pela razão da E1, de 1,34 a 1,82), mas não aplicada: as estimativas da Sprint 4 só foram registradas a partir de 11/11, com parte do trabalho já feita, e a Sprint 5 não teve tarefas planejadas. A comparação entre estimado e realizado da E2 está na [Medição 4](registro-de-medicoes.md).

As tarefas e horas de cada integrante estão abaixo (clique para abrir).

<details markdown="1">
<summary>E1 · Dupla 1 (Yasmin e Miquéias): 20,5 h</summary>

| Sprint | Tarefa | Responsável | Horas estimadas |
|---|---|---|---|
| 1 | Configuração do repositório e milestones | Yasmin | 2.5 |
| 1 | Pesquisa e redação de ODS, metas e indicadores | Miquéias | 2 |
| 1 | Justificativa da característica Segurança | Miquéias | 1 |
| 1 | Reunião de início + Ata 01 | Yasmin | 1 |
| 1 | Revisão da Fase 1 + Ata 02 | Yasmin | 0.5 |
| 2 | Objetivo, questões e hipóteses de Segurança (GQM) | Miquéias | 2 |
| 2 | Fichas das métricas de Segurança | Yasmin | 2.5 |
| 2 | Redação da metodologia do artigo | Miquéias | 1.5 |
| 2 | Revisão cruzada do GQM das outras duplas + Ata 03 | Yasmin | 1 |
| 3 | Introdução do artigo |  Miquéias | 2 |
| 3 | Consolidação do PSM (planejado vs. realizado da E1) | Yasmin | 1.5 |
| 3 | Tabela de contribuição e declaração de uso de IA | Yasmin | 1 |
| 3 | Revisão cruzada final (formatação, links, referências) | Yasmin | 1 |
| 3 | Release E1 e submissão no Moodle | Yasmin | 1 |
| | **Total** | | **20.5** |

Fonte: estimativas dos integrantes da Dupla 1, ajustadas em 18/10.

</details>

<details markdown="1">
<summary>E1 · Dupla 2 (Pedro Ian e Thiago): 36 h</summary>

| Sprint | Tarefa | Responsável | Horas estimadas |
|---|---|---|---|
| 1 | Propósito, requisitante, stakeholders e escopo da avaliação | Pedro Ian | 3 |
| 1 | Integração e revisão da Fase 1 | Pedro Ian | 2 |
| 1 | Justificativa e priorização de Eficiência | Pedro Ian | 1 |
| 1 | Modelo de qualidade adaptado e matriz de priorização | Thiago | 3 |
| 1 | Justificativa de Eficiência e contribuição para a Fase 1 | Thiago | 1 |
| 1 | Script de geração de diagramas e teste de viabilidade no DevTools | Thiago | 3 |
| 2 | Objetivo, questões e hipóteses de Eficiência (GQM) | Pedro Ian | 2 |
| 2 | Objetivo, questões e hipóteses de Eficiência (GQM) | Thiago | 2 |
| 2 | Fichas das métricas (metade) | Pedro Ian | 2 |
| 2 | Fichas das métricas (metade) | Thiago | 3 |
| 2 | Tabela de rastreabilidade Fase 1 → Fase 2 | Thiago | 2 |
| 2 | Revisão da rastreabilidade | Pedro Ian | 1 |
| 2 | Revisão cruzada do GQM | Pedro Ian | 1 |
| 2 | Revisão cruzada do GQM | Thiago | 1 |
| 3 | Estruturação e publicação da GitPage das Fases 1 e 2 | Pedro Ian | 3 |
| 3 | Integração e ajustes dos arquivos LaTeX | Thiago | 2 |
| 3 | Revisão final e correções | Pedro Ian | 2 |
| 3 | Revisão final e correções | Thiago | 2 |
| | **Total** (Pedro Ian 17 h, Thiago 19 h) | | **36** |

Fonte: estimativas dos integrantes da Dupla 2.

</details>

<details markdown="1">
<summary>E1 · Dupla 3 (Heyttor e Lucas): 14 h</summary>

| Sprint | Tarefa | Responsável | Horas estimadas |
|---|---|---|---|
| 1 | Descrição estruturada do draw.io e diagrama de contexto | Heyttor | 2.5 |
| 1 | Template SBC do relatório | Lucas | 1 |
| 2 | Objetivo, questões e hipóteses de Manutenibilidade (GQM) | Heyttor | 2.5 |
| 2 | Piloto do SonarCloud | Heyttor | 2 |
| 2 | Diagrama GQM e controle do limite de páginas | Lucas | 3 |
| 3 | Referencial teórico | Lucas | 3 |
| | **Total** (Heyttor 7 h, Lucas 7 h) | | **14** |

Fonte: estimativas dos integrantes da Dupla 3.

</details>

<details markdown="1">
<summary>E2 · Sprint 4: tarefas por dupla (41,5 h)</summary>

| Sprint | Tarefa | Dupla | Horas estimadas |
|---|---|---|---|
| 4 | Melhorias do painel e Dashboard do PSM (#38) | Dupla 1 | 3 |
| 4 | Preparar o ambiente local de coleta (#39) | Dupla 3 | 1 |
| 4 | Configurar o SonarCloud (#40, substitui a #22) | Dupla 3 | 2 |
| 4 | Plano de avaliação (Fase 3) no artigo e na GitPage (#41) | Todas (D1 1; D2 1; D3 1,5) | 3,5 |
| 4 | Coleta dos dados brutos de Segurança (#42) | Dupla 1 | 4 |
| 4 | Coleta dos dados brutos de Eficiência de Desempenho (#43) | Dupla 2 | 3 |
| 4 | Coleta dos dados brutos de Manutenibilidade (#44) | Dupla 3 | 2 |
| 4 | Análise dos dados de Segurança (#45) | Dupla 1 | 5 |
| 4 | Análise dos dados de Eficiência de Desempenho (#46) | Dupla 2 | 2 |
| 4 | Análise dos dados de Manutenibilidade (#47) | Dupla 3 | 2 |
| 4 | Resultados e conclusão inicial no artigo (#48) | Todas (2 cada) | 6 |
| 4 | Planejamento da E2 e linha de base (#49) | Dupla 1 | 2 |
| 4 | Consulta da metade da Sprint 4 e Medição 4 (#50) | Dupla 1 | 1 |
| 4 | Atas da Sprint 4 (#51) | Dupla 1 | 2 |
| 4 | Revisão das horas da Sprint 4 (#52) | Todas (D1 0,5; D2 1; D3 1) | 2,5 |
| 4 | Fixar a versão avaliada no Pages e no relatório (#53) | Dupla 3 | 0,5 |
| | **Total** (Dupla 1: 20,5 h; Dupla 2: 9 h; Dupla 3: 12 h) | | **41,5** |

Fonte: campo "Estimativa (horas)" de cada issue; nas issues de todas as duplas, a divisão registrada nos comentários. A estimativa da #48 foi registrada depois da Medição 4. A Sprint 5 não teve tarefas planejadas (ver Ocorrências por sprint).

</details>

## Ocorrências por sprint

**Sprint 1**

- O projeto começou em 07/10 sem estimativa por tarefa. O planejamento foi feito em 13/10 e o repositório configurado em 16/10, após o previsto; as horas anteriores foram registradas retroativamente.
- O grupo passou a se organizar por duplas e por conversas assíncronas no WhatsApp, com as decisões registradas nas atas.
- O relatório foi iniciado no Overleaf em modelo ABNT e precisou migrar para SBC, ACM ou IEEE (premissa 7 da especificação).

**Sprint 2**

- Em 19/10 a professora pediu o GQM no ponto de controle de 21/10. O GQM completo das três características foi antecipado para 21/10; metodologia, piloto do SonarCloud e Medição 2 ficaram em 22/10.

**Sprint 3**

- E1 entregue em 26/10 (release v1.0-E1), com 9 de 17 issues da sprint concluídas na Medição 3. A #22 e a #30 não foram concluídas, e a #26 foi concluída na entrega, mas só fechada em 10/11.

**Sprint 4**

- A sprint começou em 07/11, mas as issues só foram criadas em 11/11. As horas de 07 a 10/11 foram registradas retroativamente nas issues, e o tempo de ciclo da Sprint 4 conta a partir de 11/11.
- A #22 (Piloto do SonarCloud) e a #30 (Revisão cruzada final) não foram concluídas na E1 e foram fechadas como não planejadas. A #22 foi substituída pela issue de configuração do SonarCloud da Sprint 4 (#40); a revisão cruzada não foi replanejada, porque a Sprint 5 não teve tarefas planejadas.

**Sprint 5**

- No Ponto de Controle 2 (16/11), a professora considerou o trabalho encaminhado e não pediu correções no artigo nem na GitPage. Por isso, a Sprint 5 não teve tarefas planejadas nem issues criadas: cada integrante concluiu e revisou a própria parte conforme a disponibilidade, sem linha de base de horas.
- A equipe decidiu elaborar um relatório de auditoria de TI real com os resultados da avaliação, voltado à diretoria de TI do cenário do G1.
- O relatório não foi concluído até a entrega da E2 (24/11/2026) e fica registrado como trabalho futuro no artigo.

---
## Histórico de versão 
| Versão | Data | Descrição  |  Autor(a) |
|--------|------|------------|-----------|
| 0.1 | 13/10/2026 | Proposta inicial de cronograma e divisão por membros, elaborada com apoio do Claude (declarado no registro de uso de IA) | Yasmin |
| 0.2 | 14/10/2026 | Grupo incluiu as medições de PSM no cronograma e trocou a divisão por membros por três duplas | Equipe |
| 0.3 | 16/10/2026 | Duplas passam a dividir integralmente suas responsabilidades; planejamento adaptado ao template da disciplina | Yasmin |
| 0.4 | 18/10/2026 | Registro do que foi realizado na Sprint 1, do atraso na configuração do repositório e reorganização das datas das Sprints 2 e 3 | Yasmin |
| 0.5 | 18/10/2026 | Inclusão da estimativa de horas por tarefa da Dupla 1 e da estimativa de Pedro Ian (linha de base do PSM) | Yasmin |
| 0.6 | 18/10/2026 | Inclusão da estimativa de horas por tarefa de Dupla 2 e 3 atualizadas | Yasmin
| 0.7 | 20/10/2026 | Antecipação do GQM completo (objetivo, questões, hipóteses, fichas, diagrama GQM e rastreabilidade) para o ponto de controle de 21/10, a pedido da professora | Yasmin |
| 0.8 | 21/10/2026 | Correção das horas estimadas por sprint das Duplas 2 e 3 e da origem das estimativas | Yasmin |
| 0.9 | 22/10/2026 | Registro dos responsáveis das tarefas da Dupla 1 marcadas como "a definir", conforme a divisão combinada entre Yasmin e Miquéias | Yasmin |
| 1.0 | 11/11/2026 | Inclusão da Entrega 2 conforme as issues criadas em 11/11 e reorganização da página: cronograma e estimativas resumidos em tabelas, tarefas por integrante recolhidas e ocorrências por sprint | Yasmin |
| 1.1 | 21/11/2026 | Encerramento do planejamento: estimativas da Sprint 4 conforme as issues, Sprint 5 sem tarefas planejadas após o Ponto de Controle 2 e decisão de elaborar o relatório de auditoria de TI | Yasmin |
| 1.2 | 24/11/2026 | Registro do relatório de auditoria de TI como não concluído na E2 | Yasmin |