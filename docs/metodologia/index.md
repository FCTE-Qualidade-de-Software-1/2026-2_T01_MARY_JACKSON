# Metodologia

A metodologia do projeto é guiada por um fluxo visual que se divide em duas partes: o fluxo sequencial da avaliação e os processos de gestão contínuos.

## Sequência da Avaliação

- **Processo de avaliação:** Baseado nas 4 fases do processo de avaliação de produto da Aula 07 (E1 cobre as Fases 1 e 2; E2, as Fases 3 e 4), adaptado da ISO/IEC 25040.
- **Requisitante e cenário:** Avaliação aplicada ao contexto de uma empresa júnior hipotética.
- **Seleção das características:** Escolha e priorização de 3 características (Segurança, Eficiência, Manutenibilidade) com notas de 1 a 5.
- **Especificação das métricas:** Uso da ISO/IEC 25023 e do modelo GQM (Objetivo, Questões, Hipóteses, Métricas).

## Ao longo de todo o projeto

- **Equipe e Gestão (PSM/CID):** O projeto é organizado em duplas ao longo de 3 sprints, com painel automático gerando dados. O ciclo do PSM tem três etapas: Planejar ([Plano de medição](../gestao/plano-de-medicao.md)), Medir (script horas.py, a partir das issues e do horas.csv) e Decidir ([Registro de medições](../gestao/registro-de-medicoes.md)). Cada medida tem um limite de decisão, aplicado em todas as sprints:
    - **Planejado vs. concluído:** menos de 50% na metade da sprint, redistribuir as tarefas.
    - **Estimado vs. realizado:** razão acima de 1,5, revisar as estimativas.
    - **Tempo de ciclo:** issue sem atualização há mais de 1 dia, contado a partir do início da sprint, cobrar o responsável ou dividir a tarefa (limite revisto na Medição 2).
- **Ferramentas:** GitHub (repositório, issues, Actions), GitPage (MkDocs) e Overleaf. Evidências são versionadas.
- **Uso de IA:** A documentação de apoio está declarada na página "Declaração de uso de IA".

![Diagrama da metodologia do projeto](../imagens/metodologia/diagrama-metodologia.png)

_Figura 1. Metodologia do projeto. Fonte: elaboração da equipe._

## Onde ver cada etapa

- [Fase 1: Estabelecer os requisitos da avaliação](../fase-1/index.md)
- [Fase 2: Especificar a avaliação (GQM)](../fase-2/index.md)
- [Plano de medição (PSM/CID)](../gestao/plano-de-medicao.md)
- [Planejamento das sprints](../gestao/planejamento.md)