# Dados de Manutenibilidade

O arquivo `metricas-historicas.csv` transcreve os dados agregados da seção 5 do [relatório fornecido](../../../docs/fase-3/evidencias/resultados-das-analises.md), consolidado em 15/11/2026. Não é uma exportação bruta do SonarCloud nem uma nova coleta. Os IDs das análises são os informados pela fonte; não foram consultados remotamente nesta conferência.

Cada linha identifica a campanha de 08/11/2026, seu componente, numerador, denominador e análise de origem. O resultado é `fator × numerador / denominador`, arredondado para seis casas decimais. Para M3.1, os campos correspondem à complexidade cognitiva total e à quantidade de funções; para M3.2, às linhas duplicadas e às linhas totais do recorte de exportação.

As notas aplicam os [critérios da Fase 2](../../../docs/fase-2/niveis-e-julgamento.md#manutenibilidade-dupla-3): adequado = 5, atenção = 3 e crítico = 1. G3 é o mínimo das três notas, resultando em **3 (Atenção)** para os recortes históricos. A regra numérica foi definida após a coleta, conforme registrado na Fase 2.

A média corrigida de rótulos substitui a média invalidada por sobreposição. A cobertura de PDF é parcial. Os dados não representam os sete arquivos completos inventariados na revisão e não permitem atribuir nota a esse novo escopo. O relatório declara expressamente a ausência dessas medidas.

Os CSVs originais, os logs, os manifestos e os scripts mencionados no relatório não foram fornecidos. Este CSV torna os agregados disponíveis para conferência, sem substituir esses artefatos ou comprovar novamente a execução da coleta.
