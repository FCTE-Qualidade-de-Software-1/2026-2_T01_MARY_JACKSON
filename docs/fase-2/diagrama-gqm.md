## Eficiência de desempenho

O objetivo G2 se desdobra em quatro questões, uma para cada operação do fluxo avaliado e uma para a capacidade, e cada questão é respondida por uma ou duas métricas.

![Diagrama GQM da eficiência de desempenho: o objetivo G2 liga-se às questões Q2.1 a Q2.4, que se ligam às métricas M2.1 a M2.6](../imagens/gqm-eficiencia.png)

*Figura: hierarquia GQM da eficiência de desempenho. O objetivo G2 (nível conceitual) se liga às questões Q2.1 a Q2.4 (nível operacional), e cada questão às suas métricas (nível quantitativo): Q2.1 a M2.1 e M2.2, Q2.2 a M2.3, Q2.3 a M2.4 e M2.5, e Q2.4 a M2.6. Fonte: elaboração da equipe; código-fonte Graphviz em [gqm-eficiencia.dot](../imagens/gqm-eficiencia.dot).*

### Recorte por subcaracterística

Os diagramas abaixo mostram, para cada subcaracterística da eficiência de desempenho, quais questões e métricas a avaliam. Q2.1 e Q2.3 aparecem em mais de um recorte porque medem tanto o tempo quanto a memória.

#### Comportamento temporal

![Recorte do GQM da eficiência para comportamento temporal: Q2.1 com M2.1, Q2.2 com M2.3 e Q2.3 com M2.4](../imagens/gqm-eficiencia-comportamento-temporal.png)

*Figura: comportamento temporal, avaliado pelo tempo de abrir (M2.1), pela latência do rótulo (M2.3) e pelo tempo de exportação (M2.4). Fonte: elaboração da equipe.*

#### Utilização de recursos

![Recorte do GQM da eficiência para utilização de recursos: Q2.1 com M2.2 e Q2.3 com M2.5](../imagens/gqm-eficiencia-utilizacao-de-recursos.png)

*Figura: utilização de recursos, avaliada pelo heap após abrir (M2.2) e pelo pico de heap na exportação (M2.5). Fonte: elaboração da equipe.*

#### Capacidade

![Recorte do GQM da eficiência para capacidade: Q2.4 com M2.6](../imagens/gqm-eficiencia-capacidade.png)

*Figura: capacidade, avaliada pelo maior porte aprovado (M2.6). Fonte: elaboração da equipe.*

As definições estão em [Objetivos, questões e hipóteses](objetivos-questoes-hipoteses.md) e em [Métricas](metricas.md).