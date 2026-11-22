# Resultados das análises de manutenibilidade do draw.io

**Consolidação:** 15/11/2026. **Versão local:** 32.6.10.

Este documento reúne os resultados disponíveis da inspeção dos sete arquivos indicados nas imagens e as métricas históricas da campanha anterior. A inspeção identificou responsabilidades, dependências e problemas de delimitação da medição. **Ainda não existem medidas SonarCloud coletadas para o conjunto completo dos sete arquivos.** Por isso, não se atribui classificação quantitativa de manutenibilidade a esse conjunto.

## 1. Objeto da análise atual

As oito imagens identificam sete arquivos únicos, pois `EditorUi.js` aparece duas vezes. O conteúdo local foi inventariado integralmente, sem extração de funções, com hashes SHA-256 registrados em `manifesto.json`. O commit base registrado é `aacddaf44e6b4db468ef3f4f3e3bb56863f1d581`; os hashes identificam o conteúdo efetivamente inspecionado.

| Arquivo | Linhas físicas | Tamanho em bytes | Verificação de sintaxe |
| --- | ---: | ---: | --- |
| `src/main/webapp/js/grapheditor/Graph.js` | 54.775 | 1.624.680 | Aprovada |
| `src/main/webapp/js/diagramly/EditorUi.js` | 43.510 | 1.255.438 | Aprovada |
| `src/main/webapp/mxgraph/src/view/mxCellEditor.js` | 1.150 | 32.401 | Aprovada |
| `src/main/webapp/js/sanitizer/purify.min.js` | 7 | 29.834 | Aprovada |
| `src/main/webapp/js/diagramly/App.js` | 9.756 | 265.666 | Aprovada |
| `src/main/webapp/js/grapheditor/Editor.js` | 5.373 | 204.085 | Aprovada |
| `src/main/webapp/mxgraph/src/io/mxCodec.js` | 807 | 18.693 | Aprovada |

Procedimento executado: `node --check` em cada arquivo. A aprovação significa que a sintaxe foi aceita pelo Node instalado. Não comprova funcionamento da aplicação, segurança, desempenho ou baixa complexidade. Linhas físicas incluem comentários e linhas vazias; não substituem medidas SonarCloud. O tamanho de sete linhas de `purify.min.js` decorre de sua distribuição minificada.

## 2. Resultados da inspeção do código

| Foco | Evidência observada | Implicação para a manutenibilidade |
| --- | --- | --- |
| Leitura de arquivos | `App.loadFileSystemEntry` (`App.js:5556`) encaminha dados para `openFileHandle`; `EditorUi.setFileData` (`EditorUi.js:3665`) participa da instalação do documento. | A compreensão do fluxo exige acompanhar a coordenação entre aplicação, interface e editor. |
| Conversão XML | `Editor.setGraphXml` (`grapheditor/Editor.js:1922`) utiliza `mxCodec`; `mxCodec.decode` (`mxCodec.js:518`) procura codecs em `mxCodecRegistry`. | A conversão depende de despacho para codecs registrados. Os sete arquivos não encerram todas as dependências do fluxo. |
| Atualização do modelo | No ramo `mxGraphModel`, `Editor.setGraphXml` delimita a atualização com `beginUpdate` e `endUpdate` em `finally`. | Existe uma fronteira explícita para finalizar a atualização nesse ramo, inclusive quando ocorre exceção. |
| Edição de rótulos | `mxCellEditor.js` implementa `startEditing` (821) e `stopEditing` (982); `Graph.js` redefine esses métodos nas linhas 46070 e 46703. | A leitura apenas da implementação base ou apenas das redefinições é insuficiente para entender o comportamento efetivo. |
| Aplicação do rótulo | `mxCellEditor.applyValue` (`mxCellEditor.js:282`) chama `graph.labelChanged`; `Graph.js` trata `cellLabelChanged` na linha 38187. | A alteração do texto atravessa métodos e arquivos, exigindo rastreabilidade da cadeia de chamadas. |
| Sanitização | `Graph.sanitizeHtml` (4447), `Graph.sanitizeNode` (4720), hooks de DOMPurify e `Graph.domPurify` (5142) integram a biblioteca `purify.min.js`. | A manutenção envolve tanto a dependência quanto as políticas da aplicação. Inspecionar apenas a biblioteca omite a integração. |
| Exportação | `EditorUi.createDownloadRequest` (4131) usa `downloadRequestBuilder` (4158) e cria requisição para `EXPORT_URL`; `exportSvg` aparece na linha 9307. | O cliente prepara e coordena exportações. A inspeção não cobre a implementação do servidor externo de PDF. |
| Distribuição de responsabilidades | `Graph.js` e `EditorUi.js` concentram diversas funcionalidades e são os maiores arquivos do conjunto. | Convém investigar complexidade por função e dependências antes de escolher refatorações. O tamanho isolado não prova baixa manutenibilidade. |

Esses achados são qualitativos. A inspeção não identificou quantitativamente funções de maior complexidade nem demonstrou ausência ou presença de duplicações segundo os critérios CPD do SonarCloud.

## 3. Resultado da revisão do procedimento de medição

Foram identificadas e corrigidas diferenças entre o objeto pretendido e a configuração de análise:

| Problema | Resultado da revisão | Correção realizada |
| --- | --- | --- |
| Escopo anterior diferente das imagens | A campanha anterior usou 41 recortes e omitiu quatro arquivos indicados nas imagens. | Foi criado inventário dos sete arquivos completos. |
| Arquivos chamados `Editor.js` confundidos | A imagem indica `grapheditor/Editor.js`; a campanha anterior utilizou `diagramly/Editor.js`. | O novo escopo inclui o caminho exato da imagem. |
| Risco de exclusão por tamanho | `Graph.js` e `EditorUi.js` excedem 1.000 KB. | Configurado `sonar.javascript.maxFileSize=10000`. |
| Necessidade de procurar duplicação entre arquivos | Execuções independentes não estabelecem a duplicação cruzada do conjunto na mesma campanha. | Configuração única com os sete caminhos em `sonar.inclusions`. |
| Exclusões e código minificado | A inclusão solicitada de um arquivo não comprova que o analisador produziu suas métricas. | Exclusões locais gerais, JavaScript e CPD esvaziadas; detecção de bundles desativada; inventário remoto ainda precisa ser conferido. |
| Denominador de Q3.3 | Todas as linhas dos sete arquivos incluem funcionalidades além de exportação. | O relatório impede atribuir o percentual global automaticamente à exportação PNG/PDF/SVG. |

A existência do limite padrão e da propriedade de configuração foi conferida na [documentação oficial dos parâmetros do SonarQube Cloud](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/analysis-parameters/parameters-not-settable-in-ui). Os tamanhos locais demonstram risco de exclusão; não comprovam que uma análise passada ignorou esses arquivos. Essa conclusão exigiria seus logs e inventário.

## 4. Situação das métricas do escopo atual

| Medida | Resultado para os sete arquivos completos | Classificação |
| --- | --- | --- |
| Complexidade cognitiva | Não coletada no SonarCloud | Sem julgamento |
| Quantidade de funções | Não coletada no SonarCloud | Sem julgamento |
| Complexidade cognitiva média | Não calculada: numerador e denominador ausentes | Sem julgamento |
| Linhas duplicadas e percentual de duplicação | Não coletados no SonarCloud | Sem julgamento |
| Blocos duplicados entre arquivos | Não coletados no SonarCloud | Sem julgamento |

Ausência de coleta não equivale a zero. Os números à direita das imagens não possuem identificação de métrica ou campanha e não foram utilizados como dados brutos.

Para M3.1, a média deve ser calculada como complexidade cognitiva dividida pela quantidade de funções, com denominador positivo. Para M3.2, utilizar `100 × linhas duplicadas / linhas totais` do recorte correspondente. Não calcular média simples dos percentuais por arquivo nem substituir linhas totais por linhas de código sem comentários.

As faixas adotadas na documentação da campanha histórica são:

| Métrica | Adequado | Atenção | Crítico |
| --- | --- | --- | --- |
| M3.1 — complexidade cognitiva média por componente | ≤ 10 | > 10 e ≤ 15 | > 15 |
| M3.2 — percentual de duplicação da exportação | ≤ 5% | > 5% e ≤ 10% | > 10% |

Essas faixas são critérios da equipe. Não representam uma classificação já obtida para o conjunto atual nem um limite individual de complexidade por função.

## 5. Métricas históricas disponíveis — outro escopo

A coleta de 08/11/2026, na versão 32.6.10 e revisão `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, produziu os resultados abaixo para **recortes de funções**. Eles são preservados para rastreabilidade e não devem ser apresentados como resultados dos sete arquivos completos.

| Questão e componente histórico | Dados registrados | Cálculo | Resultado | Julgamento histórico |
| --- | --- | --- | ---: | --- |
| Q3.1 — Importação | Complexidade = 275; funções = 25 | 275 / 25 | 11,000000 | Atenção |
| Q3.2 — Rótulos, após correção da sobreposição | Complexidade = 1057; funções = 116 | 1057 / 116 | 9,112069 | Adequado |
| Q3.3 — Exportação PNG/PDF/SVG | Linhas duplicadas = 28; linhas totais = 2846 | 100 × 28 / 2846 | 0,983837% | Adequado |

IDs das análises históricas:

- Importação: `55180c38-c24b-48d4-adc7-41c45969d11a`.
- Rótulos corrigidos: `4853c608-87f3-477c-ae03-18d6f2fab544`.
- Exportação: `932752e9-e32c-4e9f-877f-b208641f4374`.

A média original de rótulos, 9,512820512820513, foi invalidada como resultado final por sobreposição de trechos. O registro corrigido é o apresentado na tabela. As classificações históricas se restringem à seleção operacional daquela coleta e aos limites documentados, incluindo cobertura parcial do fluxo de PDF. Não sustentam uma conclusão sobre o produto inteiro ou a versão de referência 32.2.0.

## 6. Conclusão e limites dos resultados

A análise atual confirmou a participação dos sete arquivos nos fluxos de leitura, representação XML, edição de rótulos, sanitização e exportação. A principal dificuldade qualitativa observada é a necessidade de acompanhar responsabilidades e redefinições distribuídas entre arquivos e camadas. Também foi identificada uma configuração de tamanho que poderia excluir os dois maiores arquivos, agora corrigida para uma nova coleta.

**Não há evidência quantitativa suficiente para classificar a manutenibilidade dos sete arquivos completos nem para confirmar H3.3 nesse novo escopo.** As medidas históricas são válidas apenas como registros dos recortes que efetivamente foram medidos. Para uma nova conclusão quantitativa, é necessário executar a coleta conjunta, confirmar o processamento remoto, conferir o inventário, preservar medidas e parâmetros e inspecionar os blocos duplicados. Para Q3.3, delimitar adicionalmente o código de exportação e seu denominador.

Se uma coleta válida retornar 0%, registrar que não foi detectada duplicação nas condições medidas. Validar o detector com duplicação conhecida em campanha piloto separada, sem acrescentar código sintético ao denominador da medição real. Esse controle ainda não foi executado.

## 7. Evidências e reprodução

Artefatos locais consultados:

- `resultados/arquivos-imagens/manifesto.json`: caminhos, hashes, tamanhos, linhas e sintaxe dos sete arquivos.
- `resultados/arquivos-imagens/README.md`: análise detalhada e correções decorrentes da revisão da conversa fornecida.
- `resultados/arquivos-imagens/sonar-project.properties`: configuração conjunta corrigida.
- `resultados/sonarcloud-manutencao/resultados.json`: métricas históricas usadas na seção 5.
- `resultados/sonarcloud-manutencao/RELATORIO_MANUTENIBILIDADE.md`: método, snapshots e limitações da campanha histórica.

Reprodução do inventário e da validação de sintaxe, na raiz do repositório:

```powershell
python tests/sonarcloud-manutencao/analisar_arquivos_imagens.py
```

O launcher da coleta remota está em `tests/sonarcloud-manutencao/executar_arquivos_imagens.ps1`. A execução depende de projeto e organização reais e de credencial disponível no ambiente. A preparação da configuração não deve ser confundida com coleta de novas medidas.
