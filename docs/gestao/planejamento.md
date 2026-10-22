# Planejamento de Sprints - Projeto Avaliação da Qualidade do draw.io

## Visão Geral do Projeto
> Este documento registra o **planejado**. O que foi realizado (responsáveis, horas reais e datas de conclusão) está nas [issues por sprint](https://github.com/FCTE-Qualidade-de-Software-1/2026-2_T01_MARY_JACKSON/milestones) e a comparação entre os dois está no [Registro de medições](registro-de-medicoes.md).

- **Nome do Projeto:** Avaliação da Qualidade de Componentes do draw.io
- **Data de Início:** 07/10/2026
- **Data de Término:** 26/10/2026 (Entrega 1); Entrega 2 conforme cronograma da disciplina
- **Objetivo Geral:** Avaliar a segurança, a eficiência de desempenho e a manutenibilidade dos componentes de importação de arquivos, rótulos e exportação do draw.io (versão 32.2.0), seguindo o processo de avaliação da ISO/IEC 25040, o método GQM e o acompanhamento do projeto com PSM/CID.
- **Organização da equipe:** três duplas, que dividem integralmente as responsabilidades da dupla.
  - Dupla 1 (Yasmin e Miquéias): Segurança; gestão do projeto (PSM/CID); Introdução e Metodologia; ODS.
  - Dupla 2 (Pedro Ian e Thiago): Eficiência de desempenho; Fase 1 (propósito, stakeholders, escopo); modelo de qualidade e priorização; GitPage.
  - Dupla 3 (Heyttor e Lucas): Manutenibilidade; descrição do draw.io e diagrama de contexto; relatório no Overleaf.

## Estimativa de horas 

As estimativas de horas foram definidas por cada integrante para as próprias tarefas, dentro da sua dupla, e formam a linha de base do PSM.

### Dupla 1

| Sprint | Tarefa | Responsável | Horas estimadas |
|---|---|---|---|
| 1 | Configuração do repositório e milestones | Yasmin | 2.5 |
| 1 | Pesquisa e redação de ODS, metas e indicadores | a definir | 2 |
| 1 | Justificativa da característica Segurança | Miquéias | 1 |
| 1 | Reunião de início + Ata 01 | Yasmin e Miquéias | 1 |
| 1 | Revisão da Fase 1 + Ata 02 | Yasmin | 0.5 |
| 2 | Objetivo, questões e hipóteses de Segurança (GQM) | a definir | 2 |
| 2 | Fichas das métricas de Segurança | a definir | 2.5 |
| 2 | Redação da metodologia do artigo | a definir | 1.5 |
| 2 | Revisão cruzada do GQM das outras duplas + Ata 03 | a definir | 1 |
| 3 | Introdução do artigo | a definir | 2 |
| 3 | Consolidação do PSM (planejado vs. realizado da E1) | Yasmin | 1.5 |
| 3 | Tabela de contribuição e declaração de uso de IA | Yasmin | 1 |
| 3 | Revisão cruzada final (formatação, links, referências) | a definir | 1 |
| 3 | Release E1 e submissão no Moodle | Yasmin | 1 |
| | **Total** | | **20.5** |

Fonte: estimativas definidas pelos integrantes da Dupla 1, ajustadas em 18/10.

### Dupla 2

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
 
Fonte: estimativas definidas pelos integrantes da Dupla 2 (Pedro Ian e Thiago).


### Dupla 3
 
| Sprint | Tarefa | Responsável | Horas estimadas |
|---|---|---|---|
| 1 | Descrição estruturada do draw.io e diagrama de contexto | Heyttor | 2.5 |
| 1 | Template SBC do relatório | Lucas | 1 |
| 2 | Objetivo, questões e hipóteses de Manutenibilidade (GQM) | Heyttor | 2.5 |
| 2 | Piloto do SonarCloud | Heyttor | 2 |
| 2 | Diagrama GQM e controle do limite de páginas | Lucas | 3 |
| 3 | Referencial teórico | Lucas | 3 |
| | **Total** (Heyttor 7 h, Lucas 7 h) | | **14** |
 
Fonte: estimativas definidas pelos integrantes da Dupla 3 (Heyttor e Lucas).
 
**Total estimado da equipe para a E1:** 70,5 h (Dupla 1: 20,5 h; Dupla 2: 36 h; Dupla 3: 14 h).

---

## Sprint 1 - Fase 1: Estabelecer os requisitos da avaliação
- **Duração:** 14/10/2026 a 19/10/2026 (ponto de controle)
- **Objetivo da Sprint:** Definir o propósito, o produto, os componentes avaliados, os stakeholders e as características priorizadas.
- **Tarefas e Atividades:**
  - Planejamento inicial e divisão de tarefas (Dupla 1)
  - Configuração do repositório a partir do template da disciplina (Dupla 1)
  - Estimativa de horas por tarefa: linha de base do PSM (todas as duplas)
  - Proposta de escopo: componentes, versão 32.2.0 e levantamento de CVEs (Dupla 2)
  - Descrição do draw.io e diagrama de contexto (Dupla 3)
  - Justificativa de cada característica com nota de ênfase de 1 a 5 (cada dupla)
  - Propósito, requisitante e stakeholders (Dupla 2)
  - Termo de consentimento para conversa com usuários (Heyttor)
  - Atas 01 e 02 e Medição 1 do PSM (Dupla 1)

- **Entregáveis**
  - Proposta de escopo aprovada
  - Seção Fase 1 iniciada no Overleaf e na GitPage
  - Linha de base do PSM e Atas 01 e 02

- **Informações extras**
  - O projeto começou em 07/10 sem estimativa por tarefa. O planejamento foi feito em 13/10 e o repositório configurado em 16/10, após o previsto. As horas anteriores foram registradas retroativamente.
  - O grupo passou a se organizar por duplas e por conversas assíncronas no WhatsApp; as decisões foram registradas nas atas.
  - O relatório foi iniciado no Overleaf em modelo ABNT e precisa migrar para SBC, ACM ou IEEE (premissa 7 da especificação).

---

## Sprint 2 - Fase 2: Especificar a avaliação (GQM)
- **Duração:** 20/10/2026 a 22/10/2026
- **Objetivo da Sprint:** Derivar, das características da Fase 1, os objetivos, questões, hipóteses e métricas.
- **Tarefas e Atividades:**
  - Objetivo, questões, hipóteses e fichas de métricas de Segurança (Dupla 1)
  - Objetivo, questões, hipóteses e fichas de métricas de Eficiência de desempenho (Dupla 2)
  - Objetivo, questões, hipóteses e fichas de métricas de Manutenibilidade (Dupla 3; rascunho já iniciado no Overleaf)
  - Diagrama GQM (Dupla 3) e tabela de rastreabilidade Fase 1 → Fase 2 (Dupla 2)
  - Metodologia do relatório (Dupla 1)
  - Medição 2 do PSM e revisão cruzada do GQM (todas as duplas)

- **Entregáveis**
  - Seção Fase 2 no relatório e na GitPage
  - Diagrama GQM e tabela de rastreabilidade

- **Informações extras**
  - Horas estimadas: Dupla 1: 7 h; Dupla 2: 14 h; Dupla 3: 7,5 h · Horas reais: ver [Registro de medições](registro-de-medicoes.md)
    - Em 19/10 a professora pediu o GQM no ponto de controle de 21/10. O GQM completo das três características (objetivo, questões, hipóteses, fichas, diagrama GQM e rastreabilidade) foi antecipado para 21/10; metodologia, piloto do SonarCloud e Medição 2 mantidos em 22/10.
---

## Sprint 3 - Entrega 1
- **Duração:** 23/10/2026 a 26/10/2026
- **Objetivo da Sprint:** Integrar e revisar o relatório e a GitPage e publicar a release E1.
- **Tarefas e Atividades:**
  - Introdução do relatório (Dupla 1)
  - Referencial teórico e integração do relatório no Overleaf (Dupla 3)
  - GitPage com as Fases 1 e 2 (Dupla 2)
  - Tabela de contribuição e declaração de uso de IA (Dupla 1)
  - Revisão cruzada final (todas as duplas)
  - Consolidação do PSM: planejado versus realizado (Dupla 1)
  - Release E1 e envio no Moodle (Dupla 1)

- **Entregáveis**
  - Relatório em LaTeX, 1ª versão (Introdução, Referencial teórico, Metodologia, Fase 1 e Fase 2)
  - GitPage atualizada até a Fase 2
  - Tabela de contribuição da equipe
  - Release E1

- **Informações extras**
  - Horas estimadas: Dupla 1: 6,5 h; Dupla 2: 5 h; Dupla 3: 3 h · Horas reais: __ h
  - Apresentação da E1 prevista para quarta-feira, conforme preferência do grupo [confirmar no cronograma do Moodle].

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