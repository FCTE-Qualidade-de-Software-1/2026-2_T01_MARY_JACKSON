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
A nota representa a prioridade desta característica na avaliação, não um resultado medido da qualidade do produto.
Do ponto de vista da diretoria de TI da empresa júnior, a classificação é crítica porque a ferramenta é central no mapeamento da infraestrutura técnica. Sua fragilidade expõe diretamente os dados estratégicos, as topologias de rede e os acessos em nuvem da própria empresa e de seus clientes.

**Por que é alta:** os componentes avaliados (importação, tratamento de rótulos e exportação/proxy) processam entradas de dados externas e atuam como ponte direta entre o ambiente local, o navegador e repositórios corporativos em nuvem (como Google Drive, OneDrive e Confluence). Falhas nesses pontos já viabilizaram ataques do tipo _Stored Cross-Site Scripting_ (XSS) e _Path Traversal_. No XSS, a simples abertura de um diagrama recebido de terceiros executa código no navegador da vítima e pode expor o diagrama aberto, _cookies_ e _tokens_ de sessão ([GHSA-fqhg-287p-c6vf](https://github.com/jgraph/drawio/security/advisories/GHSA-fqhg-287p-c6vf); [GHSA-c76x-r78m-phwx](https://github.com/jgraph/drawio/security/advisories/GHSA-c76x-r78m-phwx)). No _Path Traversal_, requisições manipuladas ao _proxy_ de exportação podiam alcançar recursos internos do servidor ([CVE-2026-63416](https://nvd.nist.gov/vuln/detail/CVE-2026-63416)).

**Por que o risco é maior neste cenário:** os avisos de segurança do draw.io registram que as falhas de XSS nos rótulos afetavam instalações próprias sem uma política de segurança de conteúdo (CSP) restritiva, como a imagem Docker oficial, enquanto o serviço público _app.diagrams.net_ não era explorável por usar essa política ([GHSA-fqhg-287p-c6vf](https://github.com/jgraph/drawio/security/advisories/GHSA-fqhg-287p-c6vf)). Uma empresa júnior que hospede a ferramenta em seus próprios servidores se enquadra no primeiro caso.

**Por que a avaliação se delimita a esses componentes:** embora receba a classificação máxima de importância devido ao alto risco do vetor de ataque, a avaliação foca estritamente nos mecanismos de entrada, sanitização e saída da aplicação draw.io (ambiente web/Docker). A análise não se estende à segurança dos provedores de nuvem terceirizados nem às políticas globais de rede da organização, concentrando o escopo no impacto direto que o comprometimento dessas três frentes causa à confidencialidade e integridade dos dados da empresa júnior.

**Histórico de vulnerabilidades (NVD):** todas foram corrigidas antes da versão 32.2.0, avaliada neste trabalho.

| CVE | Componente | Falha | Corrigida em |
|---|---|---|---|
| [CVE-2026-46642](https://nvd.nist.gov/vuln/detail/CVE-2026-46642) | Rótulos, disparada na importação | _Stored XSS_: uma rotina do painel de formatação de texto usava o rótulo sem sanitização. A falha era disparada ao abrir o arquivo, porque a importação seleciona automaticamente as formas do diagrama. | 29.7.12 |
| [CVE-2026-58504](https://nvd.nist.gov/vuln/detail/CVE-2026-58504) | Rótulos, disparada na importação | _Stored XSS_: contorno da correção anterior, combinando formas com estilos diferentes para alcançar o mesmo ponto do código. | 30.2.5 |
| [CVE-2026-63416](https://nvd.nist.gov/vuln/detail/CVE-2026-63416) | _Proxy_ de exportação | _Path Traversal_: requisições manipuladas podiam alcançar recursos internos do servidor. | 30.2.7 |