# Níveis de pontuação e julgamento

<!-- O que entra aqui: faixas de pontuação de cada métrica e a regra que leva do valor medido ao julgamento, por questão e por objetivo. Rubrica F2-C5. -->

## Eficiência de desempenho (dupla 2)

Os valores de M2.1 a M2.5 são comparados a um limite L, definido por métrica, porte e formato, e julgados pela razão `r = x / L`, em que `x` é a mediana observada. Os limites abaixo são candidatos, ainda não aprovados; a tolerância crescente por porte e a distinção por formato serão avaliadas no piloto e aprovadas pelo requisitante antes da coleta.

| Métrica/unidade            | 50    | 300    | 1.000  | 2.000  | 5.000  |
| -------------------------- | ----- | ------ | ------ | ------ | ------ |
| M2.1 abrir (ms)            | 2.000 | 3.500  | 6.500  | 11.000 | 24.000 |
| M2.2 heap após abrir (MiB) | 120   | 170    | 280    | 440    | 800    |
| M2.3 rótulo (ms)           | 300   | 450    | 700    | 1.100  | 1.800  |
| M2.4 PNG (ms)              | 4.000 | 6.000  | 11.000 | 20.000 | 45.000 |
| M2.4 PDF (ms)              | 7.000 | 10.000 | 20.000 | 35.000 | 75.000 |
| M2.4 SVG (ms)              | 3.000 | 5.000  | 9.000  | 17.000 | 40.000 |
| M2.5 PNG (MiB)             | 180   | 240    | 400    | 650    | 1.100  |
| M2.5 PDF (MiB)             | 180   | 240    | 400    | 650    | 1.100  |
| M2.5 SVG (MiB)             | 170   | 230    | 380    | 620    | 1.050  |

| Métrica         | Nota 5        | Nota 4          | Nota 3          | Nota 2          | Nota 1  |
| --------------- | ------------- | --------------- | --------------- | --------------- | ------- |
| M2.1 a M2.5 (r) | 0 <= r <= 0,5 | 0,5 < r <= 1    | 1 < r <= 1,5    | 1,5 < r <= 2    | r > 2   |
| M2.6 (porte)    | 5.000 formas  | 2.000 formas    | 1.000 formas    | 300 formas      | 50 formas ou nenhum porte aprovado |

A nota de cada métrica de M2.1 a M2.5 é a menor entre seus cenários, com medianas e notas de cada cenário preservadas no registro. Para M2.6, todos os cinco portes devem ser ensaiados, e os casos "50 formas" e "nenhum porte aprovado" são relatados separadamente. Amostras incompletas não demonstram limite de capacidade.

| Questão ou objetivo | Regra de julgamento         |
| ------------------- | --------------------------- |
| Q2.1                | mínimo(M2.1, M2.2)          |
| Q2.2                | M2.3                        |
| Q2.3                | mínimo(M2.4, M2.5)          |
| Q2.4                | M2.6                        |
| G2                  | mínimo(Q2.1, Q2.2, Q2.3, Q2.4) |

Dados ausentes, instrumentos inviáveis ou critérios não aprovados impedem a nota global; informa-se avaliação parcial. Os limites e níveis apresentados são decisões da equipe, não critérios normativos da ISO/IEC 25010.


## Manutenibilidade (Dupla 3)

Os valores de cada métrica são classificados conforme as faixas abaixo e julgados por questão. M3.1 é medida separadamente para importação de arquivos (Q3.1) e edição de rótulos (Q3.2); portanto, cada componente recebe seu próprio julgamento. M3.2 responde à Q3.3.

| Métrica e questão                       | Adequado   | Atenção          | Crítico    |
| --------------------------------------- | ---------- | ---------------- | ---------- |
| M3.1 — Importação de arquivos (Q3.1)    | M3.1 <= 10 | 10 < M3.1 <= 15  | M3.1 > 15  |
| M3.1 — Edição de rótulos (Q3.2)         | M3.1 <= 10 | 10 < M3.1 <= 15  | M3.1 > 15  |
| M3.2 — Exportação PNG, PDF e SVG (Q3.3) | M3.2 <= 5% | 5% < M3.2 <= 10% | M3.2 > 10% |

Os limites apresentados são critérios preliminares propostos para esta avaliação, não valores normativos da ISO/IEC 25010. Os julgamentos são feitos por questão; não foi definido um critério de agregação dos resultados em um julgamento único para o objetivo G3.
