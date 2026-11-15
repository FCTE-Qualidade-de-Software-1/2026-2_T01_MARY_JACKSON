# Análise dos dados e resultados

Esta página apresenta o cálculo das métricas a partir dos registros da [coleta de dados](coleta-de-dados.md), a atribuição das notas conforme as [métricas](../fase-2/metricas.md) e os [níveis de julgamento](../fase-2/niveis-e-julgamento.md) definidos na Fase 2, além das sugestões de melhoria e da conclusão inicial de cada característica avaliada.

## Segurança (Dupla 1 — Objetivo G1)

### Cálculo das métricas e julgamento (ISO/IEC 25040)

Conforme definido na árvore GQM da Fase 2, a métrica **M1.1** é calculada individualmente por componente avaliado (sem agregação somada entre superfícies distintas):

| Questão / Métrica | Fórmula Aplicada | Resultado | Nota (1–5) | Critério Atingido |
| --- | --- | --- | --- | --- |
| **Q1.1** — Importação XML (**M1.1**) | `Cb,1 / Ct,1 = 1 / 1` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.2** — Rótulos HTML (**M1.1**) | `Cb,2 / Ct,2 = 1 / 1` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.3** — Proxy / Servidor (**M1.1**) | `Cb,3 / Ct,3 = 2 / 2` | **`100%`** | **5** | Bloqueio total (`100%`) |
| **Q1.4** — Sanitização Estática (**M1.2**) | `M1.2 = (Pp / Pt) × 100 = (4 / 4) × 100` | **`100%`** | **5** | Cobertura total dos pontos válidos |
| **Q1.5** — Resistência a Bypasses (**M1.3**) | `M1.3 = (Wb / Wt) × 100 = (3 / 3) × 100` | **`100%`** | **5** | Neutralização de todas as variações |

### Pontuação final, sugestões e conclusão inicial

> **Nota Global (G1) = `min(Q1.1, Q1.2, Q1.3, Q1.4, Q1.5) = min(5, 5, 5, 5, 5) = 5`**

- **Análise:**
  * **Cliente web e inspeção estática (`Q1.1`, `Q1.2`, `Q1.4` e `Q1.5`):** A versão `32.6.10` centraliza a sanitização de rótulos HTML no método sobrescrito `cellRenderer.getLabelValue` (aplicando `DOMPurify` via `sanitizeLabel` quando `html=1`) e aplica escape explícito por `mxUtils.htmlEntities` nos pontos de medição de texto plano renderizados como HTML. O ponto principal de validação da hipótese `H1.4` encontra-se em `Format.js:5683` (`canConvertHtmlToSvg`), onde o rótulo é atribuído ao `.innerHTML` — vetor explorado anteriormente na CVE-2026-58504 mediante células não editáveis (`editable=0`) — mas que na `32.6.10` executa exclusivamente sob `html=1` após sanitização completa.
  * **Servidor Java e *servlet* `/proxy` (`Q1.3`):** Na execução complementar sobre a imagem oficial com servidor Tomcat (`jgraph/drawio:32.6.10`), confirmou-se que o `ProxyServlet` está mapeado (`WEB-INF/web.xml:11-18`) e aplica defesa *secure by default* (`ProxyServlet.java:74-76`), recusando imediatamente qualquer requisição com `HTTP 404` vazio quando a variável de ambiente `ENABLE_DRAWIO_PROXY` não está explicitamente habilitada, além de validar esquemas e bloquear endereços locais/privados via `Utils.validatedAddress` quando ativo.
- **Sugestões de melhoria ao draw.io:**
  * **Testes automatizados de regressão de sanitização:** Incluir na suíte de testes automatizados do cliente web casos cobrindo variações de evasão com elementos vetoriais SVG, quadros embutidos e esquemas de URI de script em células com `editable=0` (incluindo o fluxo de `canConvertHtmlToSvg`), prevenindo regressões em futuras atualizações da biblioteca de sanitização.
  * **Cabeçalhos de *Content Security Policy* (CSP) no deploy estático:** Recomendar na documentação oficial de implantação estática (Apache, Nginx e Docker) uma política CSP restritiva (bloqueando scripts inline e URIs de execução de script) como camada complementar de defesa em profundidade ao `DOMPurify`.
- **Conclusão inicial:** Todas as hipóteses de segurança (`H1.1` a `H1.5`) foram confirmadas. Recomenda-se a **adoção** da versão `32.6.10` sob a perspectiva da característica de Segurança, registrando-se como limitação metodológica que os testes iniciais do cliente web utilizaram vínculo de porta aberto na rede local (`0.0.0.0:8080`), corrigido para `127.0.0.1:8080` na validação do servidor Java e adotado como padrão para as próximas coletas.

## Eficiência de desempenho (Dupla 2)

*Espaço reservado para a análise e resultados da Dupla 2.*

## Manutenibilidade (Dupla 3)

*Espaço reservado para a análise e resultados da Dupla 3.*