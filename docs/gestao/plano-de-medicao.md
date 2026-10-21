# Plano de medição

A gestão do projeto usa uma métrica por categoria pedida na especificação (Seção 2), escolhidas na Tabela 5 do CID Measurement Framework, Parte 1. Cada métrica responde a uma necessidade de informação, como no modelo de informação do PSM (Aula 09). Os resultados ficam no [Registro de medições](registro-de-medicoes.md) e as decisões nas [Atas](atas.md).

## Calendário e Progresso

| Indicador | Necessidade de informação | Fórmula | Fonte | Critério de decisão |
|---|---|---|---|---|
| Planejado vs. concluído (*Committed vs. Completed*, CID Parte 1, Tabela 5, linha 1, p. 19) | Vamos cumprir o marco da sprint? | Tarefas concluídas ÷ tarefas planejadas na sprint × 100 | [Planejamento](planejamento.md), milestones e GitHub Project | Menos de 50% concluído na metade da sprint: redistribuir tarefas ou remarcar o marco |

## Recursos e Custos

| Indicador | Necessidade de informação | Fórmula | Fonte | Critério de decisão |
|---|---|---|---|---|
| Estimado vs. realizado (*Estimate vs. Actual Effort*, CID Parte 1, Tabela 5, linha 8, p. 20) | As estimativas de esforço e custo estão certas? | Horas realizadas ÷ horas estimadas; custo = horas × R$ 14,77 | `dados/gestao/horas.csv` e estimativas do [Planejamento](planejamento.md) | Razão acima de 1,5: revisar as estimativas das tarefas restantes |

## Desempenho dos Processos

| Indicador | Necessidade de informação | Fórmula | Fonte | Critério de decisão |
|---|---|---|---|---|
| Tempo de ciclo (*Cycle Time*, CID Parte 1, Tabela 5, linha 32, p. 24) | As tarefas andam ou ficam paradas? | Data de fechamento − data de abertura da issue, em dias | Datas registradas pelo GitHub em cada issue | Issue aberta há mais de 3 dias sem andamento: cobrar o responsável ou dividir a tarefa |

Os limites dos critérios de decisão foram definidos pela equipe para o prazo curto da E1 e podem ser revistos nas próximas medições.

## Calendário das medições

| Medição | Data | Momento |
|---|---|---|
| 1 | 18/10/2026 | Fim da Sprint 1 |
| 2 | 22/10/2026 | Fim da Sprint 2 |
| 3 | 26/10/2026 | Entrega 1 |