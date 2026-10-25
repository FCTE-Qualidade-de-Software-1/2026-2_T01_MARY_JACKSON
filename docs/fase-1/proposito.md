# Propósito da avaliação

## Cenário e requisitante

A **diretoria de TI de uma empresa júnior de software da universidade**, em cenário hipotético, considera hospedar o draw.io em infraestrutura própria para produzir diagramas de arquitetura, UML e bancos de dados nos projetos com clientes. A intenção é manter o controle sobre os arquivos e sobre a configuração do serviço.

O objeto proposto é o **draw.io web, em instalação própria**, com os limites descritos no [escopo](escopo.md). A versão e o ambiente de execução da avaliação serão especificados no plano de avaliação da [Fase 3](../fase-3/index.md). O cenário representa uma necessidade de avaliação; não constitui registro de entrevista, aprovação do requisitante ou implantação já realizada.

## Propósito e decisões apoiadas

O propósito é apoiar a decisão de adoção do draw.io, avaliando **Segurança, Eficiência de desempenho e Manutenibilidade** no fluxo **abrir diagramas, editar rótulos e exportar arquivos**. A equipe Mary Jackson atua como avaliadora externa ao desenvolvimento de um produto de terceiros e de código aberto.

| Característica | Decisão que os resultados devem apoiar |
|---|---|
| Segurança | Definir as condições para abrir diagramas recebidos de terceiros e utilizar os mecanismos de exportação configurados na instalação própria. |
| Eficiência de desempenho | Determinar quais portes de diagrama permitem executar o fluxo central e se será necessário recomendar limites de tamanho. |
| Manutenibilidade | Avaliar a viabilidade de analisar, corrigir e adaptar o código dos componentes selecionados, caso a empresa mantenha uma versão própria. |

## Uso pretendido dos resultados

A diretoria de TI poderá decidir entre:

1. **Adotar**, quando as evidências atenderem aos critérios acordados para o cenário.
2. **Adotar com ressalvas**, com restrições justificadas, como limites de porte, cuidados com arquivos externos ou uma política de atualização.
3. **Não adotar**, quando os riscos ou as limitações identificados inviabilizarem o uso pretendido.

O relatório final deverá apresentar evidências, limites de validade e recomendações que permitam distinguir essas alternativas. As notas de ênfase expressam a [prioridade das características](modelo-de-qualidade.md#priorizacao), sem antecipar a decisão de adoção. Os critérios quantitativos e a forma de julgamento serão especificados na Fase 2.

As expectativas de cada participante estão em [requisitante e partes interessadas](partes-interessadas.md).
