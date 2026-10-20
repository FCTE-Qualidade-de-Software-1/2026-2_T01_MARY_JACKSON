# Fase 1: Estabelecer os requisitos da avaliação

A Fase 1 define por que avaliar o draw.io, quem utilizará os resultados e quais partes do produto serão examinadas. O cenário é uma empresa júnior de software hipotética que considera hospedar o editor web em infraestrutura própria. O recorte compreende **abrir diagramas, editar rótulos e exportar**, sob as características de Segurança, Eficiência de desempenho e Manutenibilidade da **ISO/IEC 25010:2023**.

| Página | Conteúdo |
|---|---|
| [Propósito da avaliação](proposito.md) | Cenário, decisões de adoção e uso pretendido dos resultados. |
| [Requisitante e partes interessadas](partes-interessadas.md) | Papéis, expectativas e necessidades de eficiência. |
| [Produto e componentes avaliados](produto.md) | Descrição do draw.io e dos componentes escolhidos, sob responsabilidade da Dupla 3. |
| [Modelo de qualidade](modelo-de-qualidade.md) | Adaptação da ISO/IEC 25010:2023, diagrama, prioridades e escolhas de escopo. |
| [Características e priorização](caracteristicas.md) | Justificativas das notas de ênfase de cada característica. |
| [Escopo e profundidade](escopo.md) | Versão e ambiente alvo, componentes, exclusões e limites de validade. |
| [ODS relacionados](ods.md) | Relação com os ODS, sob responsabilidade da Dupla 1. |

## Situação e alinhamentos necessários

O ambiente alvo desta proposta é o **draw.io web, versão 32.2.0, hospedado em Docker, em ambiente local de testes**. A [descrição do produto](produto.md) ainda menciona a distribuição desktop 32.2.0. A Dupla 3 deve conciliar essa descrição com a decisão do grupo; a imagem Docker e a versão efetivamente executada precisam ser verificadas antes da coleta.

As prioridades propostas são **Segurança 5/5, Eficiência de desempenho 4/5 e Manutenibilidade 4/5**. Elas orientam o esforço da avaliação e ainda dependem de validação no cenário do requisitante; não são resultados sobre a qualidade do produto. A justificativa detalhada de Segurança e o conteúdo de ODS permanecem sob responsabilidade da Dupla 1.

Esta contribuição preenche os requisitos da Fase 1 atribuídos à **Dupla 2: Thiago Gomes e Pedro Ian Guedes de Carvalho**, preservando o conteúdo de Manutenibilidade da Dupla 3. As necessidades aqui registradas servirão de entrada para a [Fase 2](../fase-2/index.md), que detalhará objetivos, questões, métricas e critérios de julgamento. A coleta e a interpretação dos resultados ocorrerão nas fases posteriores.

## Materiais de origem

- `fase1-dupla2.md`: proposta da Dupla 2 para os requisitos da avaliação.
- `Ponto de controle de quarta o que falta.pdf`: distribuição das responsabilidades e ajustes para o ponto de controle de 21/10/2026.
- `2026-2 Trabalho final completo v1.pdf`: plano completo do trabalho; esta contribuição se restringe à Fase 1.
- `ISO-IEC-25010-2023.pdf` e [registro oficial da ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html): referência do modelo de qualidade de produto.
- Conteúdo atual de Manutenibilidade neste repositório e seções de Segurança e Manutenibilidade do Overleaf fornecido pela equipe: alinhamento das subcaracterísticas selecionadas.
