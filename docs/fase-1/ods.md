# ODS relacionados

<!-- O que entra aqui: Objetivos de Desenvolvimento Sustentável relacionados, com meta, indicador e pertinência ao software. Rubrica Fase 1, critério 7. -->

## Objetivos de Desenvolvimento Sustentável (ODS)

A avaliação de qualidade do *draw.io* pode contribuir, de forma indireta, para três metas da Agenda 2030. Os textos das metas seguem a versão das Nações Unidas publicada pelo IPEA, exceto a meta 9.c, citada na versão adaptada ao Brasil. A contribuição está em apoiar uma decisão de adoção baseada em evidências, e não em mudar o produto: os resultados indicam se a ferramenta pode ser usada com segurança, desempenho adequado e possibilidade de manutenção na infraestrutura da empresa júnior do cenário hipotético da avaliação ([Propósito](proposito.md)).

### ODS 9: Indústria, Inovação e Infraestrutura
*Construir infraestrutura resiliente, promover a industrialização inclusiva e sustentável, e fomentar a inovação.*

* **Meta 9.c (versão Brasil):** Aumentar significativamente o acesso às tecnologias de informação e comunicação e empenhar-se para oferecer acesso universal e a preços acessíveis à internet, até 2020, buscando garantir a qualidade, a privacidade, a proteção de dados e a segurança cibernética ([IPEA](https://www.ipea.gov.br/ods/ods9.html)).
* **Por que a versão Brasil:** a adaptação brasileira acrescenta à meta a qualidade, a proteção de dados e a segurança cibernética, que são os aspectos avaliados neste trabalho. O prazo original da meta (2020) já passou, mas o compromisso com qualidade e segurança das tecnologias de informação continua pertinente.
* **Aplicação no Projeto:** o draw.io é uma ferramenta gratuita e de código aberto (licença Apache 2.0, [repositório do draw.io](https://github.com/jgraph/drawio)), o que amplia o acesso a uma tecnologia de informação usada para documentar sistemas, redes e bancos de dados. Esse acesso só é útil se a ferramenta tiver qualidade: se resistir a vulnerabilidades conhecidas (Segurança), mantiver o desempenho com diagramas maiores (Eficiência de desempenho) e puder ser corrigida pela própria empresa (Manutenibilidade).
* **Indicador no projeto:** resultado das métricas definidas na Fase 2 para as três características. O indicador oficial da meta (9.c.1) mede a cobertura de rede móvel e não se aplica a software; por isso a equipe usa as próprias métricas para acompanhar a contribuição.

### ODS 16: Paz, Justiça e Instituições Eficazes
*Promover sociedades pacíficas e inclusivas para o desenvolvimento sustentável, proporcionar o acesso à justiça para todos e construir instituições eficazes, responsáveis e inclusivas em todos os níveis.*

* **Meta 16.6:** Desenvolver instituições eficazes, responsáveis e transparentes em todos os níveis ([IPEA](https://www.ipea.gov.br/ods/ods16.html)).
* **Aplicação no Projeto:** a empresa júnior guarda em diagramas informações de seus clientes, como a arquitetura dos sistemas que desenvolve. Uma instituição responsável precisa saber se a ferramenta protege essas informações. O histórico do draw.io registra falhas em que abrir um diagrama recebido de terceiros executava código no navegador ([CVE-2026-46642](https://nvd.nist.gov/vuln/detail/CVE-2026-46642)), e os desenvolvedores não corrigem versões antigas: quem hospeda a ferramenta deve mantê-la atualizada ([política de segurança do draw.io](https://github.com/jgraph/drawio/security/policy)). A avaliação dá à diretoria de TI evidências para decidir com responsabilidade se adota a ferramenta e com quais cuidados.
* **Indicador no projeto:** resultado das métricas de Segurança (confidencialidade, integridade e resistência), coletadas na versão 32.2.0 em ambiente local de testes. Os indicadores oficiais da meta (16.6.1 e 16.6.2) tratam de despesas e serviços públicos e não se aplicam a este projeto.

### ODS 8: Trabalho Decente e Crescimento Econômico
*Promover o crescimento econômico sustentado, inclusivo e sustentável, emprego pleno e produtivo, e trabalho decente para todos.*

* **Meta 8.3:** Promover políticas orientadas para o desenvolvimento que apoiem as atividades produtivas, geração de emprego decente, empreendedorismo, criatividade e inovação, e incentivar a formalização e o crescimento das micro, pequenas e médias empresas, inclusive por meio do acesso a serviços financeiros ([IPEA](https://ipea.gov.br/ods/ods8.html)).
* **Aplicação no Projeto:** empresas juniores são iniciativas de empreendedorismo de estudantes, com poucos recursos. Uma ferramenta gratuita e de código aberto reduz o custo das atividades produtivas da empresa, mas só é uma boa escolha se for segura e confiável. A avaliação oferece critérios para que uma organização pequena adote software livre sem assumir riscos que desconhece.
* **Indicador no projeto:** decisão de adoção apoiada pelos resultados (adotar, adotar com ressalvas ou não adotar), conforme o [Propósito](proposito.md). O indicador oficial da meta 8.3 (8.3.1) mede a informalidade do trabalho e não se aplica a este projeto.

## Relação entre os ODS e os objetivos da avaliação

| ODS e meta | Objetivo GQM relacionado | O que os resultados indicam |
|---|---|---|
| ODS 9, meta 9.c | Segurança, Eficiência de desempenho e Manutenibilidade | Se a ferramenta é confiável, mantém o desempenho com diagramas maiores e pode ser corrigida pela própria empresa |
| ODS 16, meta 16.6 | Segurança | Se as informações dos clientes guardadas nos diagramas ficam protegidas contra as falhas já registradas |
| ODS 8, meta 8.3 | Os três objetivos, em conjunto | Se uma organização pequena pode adotar a ferramenta gratuita com segurança, e com quais ressalvas |

As métricas de cada objetivo estão em [Métricas](../fase-2/metricas.md), e a ligação com as prioridades da Fase 1, em [Rastreabilidade](../fase-2/rastreabilidade.md).