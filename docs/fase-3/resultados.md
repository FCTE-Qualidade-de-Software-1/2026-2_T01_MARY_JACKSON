# Análise dos dados e resultados

Esta página apresenta o cálculo das métricas a partir dos registros da [coleta de dados](coleta-de-dados.md), a atribuição das notas conforme as [métricas](../fase-2/metricas.md) e os [níveis de julgamento](../fase-2/niveis-e-julgamento.md) definidos na Fase 2, além das sugestões de melhoria e da conclusão inicial de cada característica avaliada.

## Segurança (Dupla 1 — Objetivo G1)

### Cálculo das métricas e julgamento (ISO/IEC 25040)

| Questão / Métrica | Fórmula Aplicada | Resultado | Nota (1–5) | Critério Atingido |
| --- | --- | --- | --- | --- |
| **Q1.1** — Importação XML (**M1.1**) | `Cb / Ct = 1 / 1` | `100%` | **5** | Bloqueio total (`100%`) |
| **Q1.2** — Rótulos HTML (**M1.1**) | `Cb / Ct = 1 / 1` | `100%` | **5** | Bloqueio total (`100%`) |
| **Q1.3** — Proxy / Traversal (**M1.1**) | `Cb / Ct = 2 / 2` | `100%` | **5** | Bloqueio total (`100%`) |
| **M1.1 Consolidada** | `M1.1 = (4 / 4) × 100` | **`100%`** | **5** | Nenhuma vulnerabilidade explorável |
| **Q1.4** — Sanitização Estática (**M1.2**) | `M1.2 = (Pp / Pt) × 100 = (3 / 3) × 100` | **`100%`** | **5** | Cobertura total dos pontos válidos |
| **Q1.5** — Resistência a Bypasses (**M1.3**) | `M1.3 = (Wb / Wt) × 100 = (3 / 3) × 100` | **`100%`** | **5** | Neutralização de todas as variações |

### Pontuação final, sugestões e conclusão inicial

> **Nota Global (G1) = `min(Q1.1, Q1.2, Q1.3, Q1.4, Q1.5) = min(5, 5, 5, 5, 5) = 5`**

* **Análise:** A arquitetura da versão `32.6.10` centraliza a sanitização de rótulos HTML no método sobrescrito `cellRenderer.getLabelValue` (utilizando `DOMPurify` via `sanitizeLabel`) e assegura o escape explícito por `mxUtils.htmlEntities` nos pontos de medição de texto plano renderizados como HTML. Ademais, a implantação estática da aplicação web não expõe o *servlet* `/proxy`, eliminando a superfície de ataque de *Path Traversal* testada.
* **Sugestões de melhoria ao draw.io:**
    * **Testes automatizados de regressão de sanitização:** Incluir na suíte de testes automatizados do cliente web casos cobrindo vetores de *bypass* com tags alternativas (`<svg onload>`, `<iframe>`) e esquemas `javascript:` em âncoras com `editable=0`, evitando regressões em futuras atualizações da biblioteca de sanitização.
    * **Cabeçalhos de *Content Security Policy* (CSP) no deploy estático:** Recomendar na documentação oficial de implantação estática (Apache, Nginx e Docker) uma política CSP restritiva (bloqueando *inline scripts* e URIs `javascript:`) como camada complementar de defesa em profundidade ao `DOMPurify`.
* **Conclusão inicial:** Todas as hipóteses de segurança (`H1.1` a `H1.5`) foram confirmadas. Recomenda-se a **adoção** da versão `32.6.10` sob a perspectiva da característica de Segurança, ressalvando-se que a avaliação se restringe ao cliente web estático e aos vetores modelados no escopo.

## Eficiência de desempenho (Dupla 2)

*Espaço reservado para a análise e resultados da Dupla 2.*

## Manutenibilidade (Dupla 3)

*Espaço reservado para a análise e resultados da Dupla 3.*