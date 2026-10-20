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

## Segurança


**Nota de ênfase: 5/5 (Crítica)**
Do ponto de vista da diretoria de TI da empresa júnior, a classificação é crítica porque a ferramenta é central no mapeamento da infraestrutura técnica. Sua fragilidade expõe diretamente os dados estratégicos, as topologias de rede e os acessos em nuvem da própria empresa e de seus clientes.

**Por que é alta:** os componentes avaliados (importação, tratamento de rótulos e exportação/proxy) processam entradas de dados externas e atuam como ponte direta entre o ambiente local, o navegador e repositórios corporativos em nuvem (como Google Drive, OneDrive e Confluence). Falhas de segurança nesses pontos — como Stored XSS e Path Traversal — possuem impacto severo, pois a abertura de um único arquivo malicioso pode permitir o roubo de tokens de sessão, o vazamento da arquitetura de rede e a movimentação lateral do atacante na infraestrutura da empresa.

**Por que a avaliação se delimita a esses componentes:** embora receba a classificação máxima de importância devido ao alto risco do vetor de ataque, a avaliação foca estritamente nos mecanismos de entrada, sanitização e saída da aplicação draw.io (ambiente web/Docker). A análise não se estende à segurança dos provedores de nuvem terceirizados nem às políticas globais de rede da organização, concentrando o escopo no impacto direto que o comprometimento dessas três frentes causa à confidencialidade e integridade dos dados da empresa júnior.

**Evidências de Riscos (Base NVD):**
A criticidade e a necessidade de avaliações rigorosas são evidenciadas pelas recentes vulnerabilidades documentadas e corrigidas nos componentes da ferramenta:
* **CVE-2026-46642:** Vulnerabilidade de *Stored XSS* na importação de arquivos, permitindo a execução automática de *scripts* maliciosos no momento da carga inicial do diagrama.
* **CVE-2026-58504:** Vulnerabilidade de *Stored XSS* devido a falhas na sanitização de rótulos e formatação de texto das formas.
* **CVE-2026-63416:** Vulnerabilidade de *Path Traversal* no servidor *proxy* de exportação, permitindo requisições de acesso não autorizado a diretórios locais.