# Registro de medições

Cada medição segue o [Plano de medição](plano-de-medicao.md): valor, interpretação e a decisão tomada, que também fica registrada nas [Atas](atas.md).

## Medição 1 (Sprint 1: 14/10 a 19/10/2026), registrada retroativamente

**Linha de base:** as tarefas e estimativas da Sprint 1 no [Planejamento](planejamento.md) (versão 0.6, de 18/10). As issues foram criadas depois da execução das tarefas; por isso, a conclusão foi verificada pela data do commit no repositório (incluindo os commits do PR #13) ou, para o relatório, pelo histórico de versões do Overleaf. As horas vêm de [`dados/gestao/horas.csv`](horas.md).

### Calendário e Progresso: planejado vs. concluído

| Tarefa planejada | Responsável | Estimativa | Evidência | Data | Situação em 19/10 |
|---|---|---|---|---|---|
| Configuração do repositório e milestones | Yasmin | 2,5 h | Repositório: commit 2e53f14; milestones criadas em 20/10 | 16/10 e 20/10 | Parcial |
| Pesquisa e redação de ODS, metas e indicadores | a definir | 2 h | Commit d1e78d1 (Miquéias) | 20/10 | Atrasada |
| Justificativa da característica Segurança | Miquéias | 1 h | Overleaf: `secoes/seguranca.tex` criado por Miquéias; GitPage no commit 4454358 (20/10) | 18/10 | Concluída |
| Reunião de início e Ata 01 | Yasmin e Miquéias | 1 h | Reunião em 14/10; ata no commit c166fb5 | 14/10 e 20/10 | Parcial |
| Revisão da Fase 1 e Ata 02 | Yasmin | 0,5 h | Reunião em 18/10; ata no commit c166fb5 | 18/10 e 20/10 | Parcial |
| Propósito, requisitante, stakeholders e escopo | Pedro Ian | 3 h | Commit 6cd9d56 (PR #13) | 19/10 | Concluída |
| Integração e revisão da Fase 1 | Pedro Ian | 2 h | Commit 6cd9d56, coautoria (PR #13) | 19/10 | Concluída |
| Justificativa e priorização de Eficiência | Pedro Ian | 1 h | Commit 6cd9d56 (PR #13) | 19/10 | Concluída |
| Modelo de qualidade adaptado e matriz de priorização | Thiago | 3 h | Commit 6cd9d56 (PR #13) | 19/10 | Concluída |
| Justificativa de Eficiência e contribuição para a Fase 1 | Thiago | 1 h | Commit 6cd9d56 (PR #13) | 19/10 | Concluída |
| Script de geração de diagramas e teste no DevTools | Thiago | 3 h | Sem evidência no repositório nem no Overleaf [confirmar com Thiago] | — | Sem evidência |
| Descrição do draw.io e diagrama de contexto | Heyttor | 2,5 h | Commits a11a2be, 15f51fa e efadcc8 | 18 e 19/10 | Concluída |
| Template SBC do relatório | Lucas | 1 h | Overleaf: modelo SBC (`sbc-template.sty`, `sbc.bst`) carregado por Lucas; modelo ABNT anterior em 17/10 | 18/10 | Concluída |

**Resumo:** das 13 tarefas planejadas, 8 foram concluídas no prazo (61,5%), 3 ficaram parciais, 1 atrasou e 1 não tem evidência. Em horas estimadas, as tarefas concluídas no prazo somam 14,5 h das 23,5 h planejadas para a sprint (61,7%).

**Trabalho realizado fora da linha de base da Sprint 1** (evidências no Overleaf e no repositório):

| Trabalho | Quem | Data | Previsto para |
|---|---|---|---|
| Introdução do relatório (primeira versão) | Heyttor e Lucas | 17/10 | Sprint 3 |
| GQM de Manutenibilidade no relatório | Lucas | 17/10 e 19/10 | Sprint 2 |
| GQM, fichas e diagrama GQM de Eficiência no relatório | Thiago e Pedro Ian | 18 e 19/10 | Sprint 2 |
| Objetivo GQM de Segurança no relatório | Miquéias | 18 e 19/10 | Sprint 2 |
| Termo de consentimento | Heyttor | 19/10 (commit a695434) | não previsto |
| Nota e justificativa de Manutenibilidade | Lucas | 19/10 (commit eb18de7) | não previsto |
| Estudo das CVEs do draw.io | Yasmin | 18/10 | não previsto |
| Planejamento, estimativas e organização do repositório | Yasmin | 13 a 18/10 | parcialmente previsto |

### Recursos e Custos: estimado vs. realizado

| Dupla | Estimado na Sprint 1 | Registrado até 18/10 | Realizado / estimado |
|---|---|---|---|
| Dupla 1 (Yasmin e Miquéias) | 7 h | 8,17 h (Yasmin) | 116,7% |
| Dupla 2 (Pedro Ian e Thiago) | 13 h | 0 h | 0% |
| Dupla 3 (Heyttor e Lucas) | 3,5 h | 1,33 h (Heyttor) | 38,0% |
| **Total** | **23,5 h (R$ 347,09)** | **9,5 h (R$ 140,31)** | **40,4%** |

Custo calculado com R$ 14,77 por hora ([Registro de horas](horas.md)).

### Desempenho dos Processos: tempo de entrega

Data em que cada tarefa planejada ficou completa (12 tarefas com evidência):

| Data da conclusão | Tarefas |
|---|---|
| 18/10 | 2 (template SBC; justificativa de Segurança no relatório) |
| 19/10 | 6 (cinco tarefas da Fase 1 da Dupla 2; descrição do draw.io) |
| 20/10 | 4 (configuração com milestones, ODS, Atas 01 e 02) |

### Interpretação e decisões

| Indicador | Interpretação | Decisão |
|---|---|---|
| Planejado vs. concluído | A Fase 1 foi entregue no prazo, e parte da Fase 2 e da Introdução já começou no relatório durante a Sprint 1. O atraso ficou nas tarefas de registro: atas, milestones e ODS. A publicação na GitPage chegou depois do relatório. | Criar o GitHub Project, as milestones e uma issue por tarefa; registrar as atas logo após cada reunião; manter a regra de concluir no relatório e depois publicar na GitPage (Ata 03). |
| Estimado vs. realizado | Só dois dos seis membros registraram horas, embora o histórico do Overleaf mostre trabalho de todos. A diferença mostra falta de registro, e não esforço menor. A Dupla 1 passou da estimativa porque as tarefas de gestão não estavam na linha de base. | Cada membro registra as horas com o número da issue; commits de horas usam "Refs #9". As tarefas de gestão passam a constar no planejamento como trabalho não planejado. |
| Tempo de entrega | Todas as tarefas foram concluídas nos dois últimos dias da sprint (18 e 19/10) ou no dia seguinte. | Fazer um ponto de acompanhamento no meio de cada sprint. |

## Medição parcial (20/10/2026, meio da Sprint 2)

| Indicador | Valor | Interpretação | Decisão |
|---|---|---|---|
| Planejado vs. concluído | Issues fechadas: Sprint 1, 8 de 11 (72,7%); Sprint 2, 3 de 11 (27,3%); E1, 11 de 30 (36,7%). | A issue de registro de horas (#9) acompanha o projeto inteiro e foi associada à Sprint 1. A Sprint 2 está abaixo de 50% na metade do prazo. | Mover a #9 para a Sprint 3, fechar as issues já concluídas que ficaram abertas e redistribuir as tarefas da Sprint 2 (Ata 03). |
| Estimado vs. realizado | 12,0 h registradas de 70,5 h estimadas para a E1 (17,0%); R$ 177,24 de R$ 1.041,29. | Três dos seis membros ainda não registraram horas. | Cobrar o registro de todos até a Medição 2. |
| Tempo de ciclo | Não medido | As issues foram criadas depois da execução das tarefas. | Medir na Medição 2, com as tarefas abertas a partir de 20/10. |

## Medição 2 (22/10/2026, fim da Sprint 2)

_A realizar._

## Medição 3 (26/10/2026, Entrega 1)

_A realizar._