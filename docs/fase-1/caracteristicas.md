# Características e priorização

## Eficiência de desempenho

**Nota de ênfase: 4/5.** A nota representa a prioridade desta característica na avaliação, não um resultado medido da qualidade do produto. É uma proposta para o cenário do requisitante e deverá ser validada com as demais prioridades.

**Por que é alta:** abrir arquivos, editar rótulos e exportar PNG, PDF e SVG compõem o fluxo central de criação de diagramas. Atrasos, interrupções ou consumo excessivo de memória podem prejudicar esse trabalho, especialmente em diagramas maiores. Avaliar o desempenho apoia a decisão de adoção e a eventual recomendação de limites de porte.

**Por que não é mais alta:** neste cenário, a proteção dos dados dos clientes recebe a prioridade máxima de Segurança (5/5). Para o desempenho, uma eventual adoção com limites de porte permanece como alternativa a ser julgada com base nas evidências. A nota 4/5 mantém a atenção às três operações sem antecipar que o produto já tenha desempenho adequado.

O recorte mantém as três subcaracterísticas da **ISO/IEC 25010:2023**: **comportamento temporal**, para os tempos de resposta; **utilização de recursos**, delimitada à memória JavaScript do editor; e **capacidade**, limitada ao maior porte aprovado entre os cinco planejados. O [modelo de qualidade](modelo-de-qualidade.md) apresenta a adaptação, e o [escopo](escopo.md) registra os componentes, o ambiente alvo e os limites de validade.

## Manutenibilidade

**Nota de ênfase: 4/5.** A nota representa a prioridade desta característica na avaliação, não um resultado medido da qualidade do produto.

**Por que é alta:** os componentes avaliados envolvem importação e exportação de arquivos e edição de rótulos. Alterações nesses fluxos podem afetar a compatibilidade dos diagramas e o trabalho dos usuários. Avaliar a manutenibilidade ajuda a identificar o esforço para analisar, corrigir e evoluir esses componentes.

**Por que não é mais alta:** a avaliação está delimitada a três componentes do draw.io, não à manutenção do produto inteiro. Além disso, mudanças em formatos de arquivo e na representação dos diagramas podem gerar regressões em outras operações; por isso, a análise precisa considerar testes e compatibilidade, mas sua prioridade permanece abaixo da máxima neste escopo.
