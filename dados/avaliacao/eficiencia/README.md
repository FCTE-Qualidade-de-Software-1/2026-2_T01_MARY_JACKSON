# Evidências de eficiência de desempenho

Dados da coleta de 14/11/2026, realizada no draw.io 32.6.10. A coleta oficial contém 125 tentativas: cinco portes, cinco operações e cinco repetições. Os pilotos são preservados à parte e não entram no cálculo das métricas da coleta oficial.

## Responsáveis

- **Coleta:** Pedro Ian Guedes de Carvalho.
- **Análise dos dados e resultados:** Thiago Gomes Pereira de Abreu. A análise está na seção de eficiência de [Análise dos dados e resultados](../../../docs/fase-4/resultados.md).

## Acesso às evidências

**Pasta no Google Drive:** [Mary Jackson - Eficiência de Desempenho - Evidências da Coleta](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

| Pacote | Conteúdo | Tamanho aproximado |
| --- | --- | --- |
| `eficiencia-coleta-2026-11-14.zip` | 125 traces da coleta oficial, em `dados/avaliacao/eficiencia/brutos/traces/`. | 427 MiB |
| `eficiencia-pilotos-2026-11-14.zip` | 10 traces do piloto automatizado e 4 do manual, em `dados/avaliacao/eficiencia/brutos/piloto/` e `manual/`. | 49 MiB |
| `eficiencia-exportacoes-2026-11-15.zip` | 14 arquivos exportados (PNG, SVG e PDF) da validação das exportações, em `dados/avaliacao/eficiencia/brutos/exportados/`. | 22 MiB |

Os pacotes conservam os nomes dos arquivos e os caminhos a partir da raiz do repositório. Os traces `.json.gz` ficam fora do versionamento Git; as cópias locais restauradas são ignoradas pelo `.gitignore`. Os arquivos exportados na validação também ficam fora do Git, exceto o relatório `validacao.csv`. O arquivo [SHA256SUMS.txt](SHA256SUMS.txt) permite conferir a integridade dos três ZIPs, dos 139 traces e dos 14 arquivos exportados.

O contexto de execução e os registros das medidas estão na seção de eficiência da página [Coleta de dados](../../../docs/fase-4/coleta-de-dados.md).

## Arquivos mantidos no Git

| Caminho relativo a esta pasta | Conteúdo |
| --- | --- |
| `coletar.py` | Automação da coleta. |
| `ler_traces.py` | Extração das medidas dos traces. |
| `validar_exportacoes.py` | Validação dos arquivos exportados (formato e completude do diagrama). |
| `cargas/gerar_cargas.py` | Geração das cinco cargas sintéticas. |
| `cargas/carga-*.drawio` | Cargas de 50, 300, 1.000, 2.000 e 5.000 formas. |
| `brutos/tentativas.csv` | 125 registros da coleta oficial, com nomes dos traces e instantes usados nas medidas. |
| `brutos/piloto/piloto.csv` | Registros do piloto automatizado. |
| `brutos/piloto/manual/piloto_manual.csv` | Registros do piloto manual. |
| `brutos/exportados/validacao.csv` | Resultado da validação dos arquivos exportados, por porte e formato. |
| `SHA256SUMS.txt` | Hashes dos pacotes externos, dos traces e dos arquivos exportados. |

## Restaurar os traces localmente

Baixe os ZIPs pelo link da pasta de evidências. No PowerShell, abra a raiz do repositório e execute os comandos abaixo, ajustando a pasta de download se necessário:

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-coleta-2026-11-14.zip" -DestinationPath .
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-pilotos-2026-11-14.zip" -DestinationPath .
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-exportacoes-2026-11-15.zip" -DestinationPath .
```

A extração recria os caminhos de `dados/avaliacao/eficiencia/brutos/`. Não extraia os pacotes dentro desta pasta de eficiência, pois isso duplicaria a estrutura `dados/avaliacao/eficiencia/`.

## Conferir a integridade

As duas primeiras entradas do [manifesto SHA-256](SHA256SUMS.txt) correspondem aos ZIPs da coleta e dos pilotos, seguidas dos traces. A última seção traz o ZIP da validação das exportações e os arquivos exportados. Os caminhos são relativos à raiz do repositório.

Para conferir os pacotes no PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-coleta-2026-11-14.zip"
Get-FileHash -Algorithm SHA256 -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-pilotos-2026-11-14.zip"
```

Compare cada resultado com a entrada do mesmo nome no manifesto. Para conferir um trace após a extração, execute `Get-FileHash` sobre o caminho indicado na entrada correspondente e compare o resultado.

## Conferir a extração das medidas

Os critérios de leitura estão no [plano de avaliação](../../../docs/fase-3/ambiente-de-execucao.md#leitura-das-medidas). Para executar novamente o leitor sobre a coleta oficial, a partir da raiz do repositório:

```powershell
python dados/avaliacao/eficiencia/ler_traces.py dados/avaliacao/eficiencia/brutos/traces "$env:TEMP\tentativas-eficiencia-conferencia.csv"
```

A saída usa um arquivo separado para preservar `brutos/tentativas.csv`. As tabelas, gráficos e julgamentos da análise devem ser produzidos separadamente, mantendo a rastreabilidade para as tentativas oficiais.

## Análise dos dados e resultados

Execute `python dados/avaliacao/eficiencia/analisar.py` na raiz do repositório para reproduzir a análise. O script preserva os dados brutos e gera `analise/tentativas-classificadas.csv`, `analise/metricas-por-cenario.csv` e `analise/resumo.json`, além de atualizar apenas a seção de eficiência da página de resultados.

Os limites foram ratificados pela Dupla 2 em 15/11/2026, após a coleta, mantendo os valores adotados. O julgamento se restringe ao fluxo instrumentado; o PDF final foi verificado na campanha complementar e não ficou completo sob as opções testadas. A revisão pós-coleta de 15/11/2026 atribui nota temporal 1 a cenários com menos de quatro sucessos por falha do produto e julga memória por medidas completas das operações concluídas. Dados ausentes ou inválidos continuam não conclusivos. O histórico dessa revisão está em `analise/revisao-criterios.json`. O script verifica os hashes dos insumos normalizados para LF e exige revisão se os dados ou critérios mudarem.

O encerramento da análise utiliza também `brutos/exportados/validacao.csv`, integrado pelo PR #57. Esse CSV registra o resultado das verificações, inclusive as falhas. Os arquivos exportados estão no pacote `eficiencia-exportacoes-2026-11-15.zip`, já disponível no Drive. A validação complementar não mede tempos e não substitui as 125 tentativas oficiais.


## Reprodução e auditoria

Na raiz do repositório:

```powershell
python dados/avaliacao/eficiencia/analisar.py
```

O script atualiza os arquivos de `analise/` e substitui somente a seção de eficiência em `docs/fase-4/resultados.md`. Alterações no texto dessa seção também devem ser refletidas no gerador para não serem sobrescritas. Os dados brutos e as seções das outras duplas são preservados.

Arquivos derivados em `analise/`:

- `tentativas-classificadas.csv`: 125 tentativas, com classificação e identificação das falhas;
- `metricas-por-cenario.csv`: 45 resultados, com medidas, limites, razões e notas;
- `resumo.json`: consolidação e hashes SHA-256 dos insumos normalizados para LF;
- `revisao-criterios.json`: regra adotada em 15/11/2026, julgamento anterior e resultados alterados;
- `encerramento-pendencias.json`: ratificação dos limites, origem e hash da validação complementar e alcance da conclusão.

Os hashes SHA-256 dos insumos são normalizados para LF. Se um insumo mudar, revise a alteração antes de atualizar o hash esperado no script e regenerar os resultados. O histórico do julgamento anterior permanece em `revisao-criterios.json`.

### Falhas e tratamento das medidas

As 125 operações concluíram na automação. O julgamento temporal identifica 119 sucessos e seis falhas, detalhadas abaixo:

| Porte | Tentativa SVG | Tempo (ms) | 2L (ms) |
| --- | --- | --- | --- |
| 2.000 | 4 | 40.056,2 | 34.000 |
| 5.000 | 1 | 113.422,1 | 80.000 |
| 5.000 | 2 | 118.537,9 | 80.000 |
| 5.000 | 3 | 110.703,9 | 80.000 |
| 5.000 | 4 | 126.107,8 | 80.000 |
| 5.000 | 5 | 113.646,1 | 80.000 |

No SVG de 2.000 formas, a exclusão temporal da tentativa 4 altera a mediana dos sucessos de 29.471,8 para 29.082,5 ms. As cinco medidas de memória completas são mantidas: mediana de 120,74 MiB. Em 5.000 formas, o SVG recebe nota temporal 1 pelas cinco falhas; não há mediana de sucessos. O tempo mediano bruto de 113.646,1 ms permanece descritivo. As cinco operações concluíram e forneceram heap válido, cuja mediana é 381,90 MiB e nota 5 (`381,90 / 1.050 ≈ 0,364`). A nota de memória não transforma a falha temporal em sucesso. O julgamento anterior foi preservado para auditoria; a revisão foi adotada após a coleta e não altera L.

A pontuação usa a razão entre mediana e limite. Por exemplo, no SVG, `11.911,4 / 9.000 ≈ 1,32349` resulta em nota 3 e `29.082,5 / 17.000 ≈ 1,71074`, em nota 2. A capacidade instrumentada é de 2.000 formas (nota 4), com pelo menos quatro sucessos por operação até `2L`. Até 1.000 formas, cada operação tem 5/5 sucessos; em 2.000 formas, o SVG tem 4/5 e, em 5.000, 0/5. Abrir, editar rótulo, exportar PNG e preparar impressão de PDF têm 5/5 sucessos temporais em todos os portes. Somente até 300 formas todas as medianas atendem a `L`.

### Observações de interpretação

Abertura e rótulos ficam abaixo da metade dos limites candidatos. SVG é a principal restrição: a mediana bruta cresce cerca de 257 vezes para um aumento de 100 vezes nas formas. A conversão de rótulos HTML em imagens, descrita na [coleta](coleta-de-dados.md#observacoes-da-coleta), é uma pista de investigação, não uma causa comprovada por esta análise.

PNG e preparação de PDF atendem aos limites. A variação do PNG em 5.000 formas (1.716,5–3.588,8 ms) foi preservada, sem exclusão arbitrária.

**Memória:** o máximo bruto de heap, 418,30 MiB, pertence a um SVG que falhou temporalmente. A nota 5 de memória resulta da mediana de 381,90 MiB das cinco operações concluídas, não desse máximo isolado. A oscilação pode envolver coleta de lixo, sem evidência suficiente para isolar essa causa.

### Alcance da validação dos arquivos

No PNG, a checagem cobre assinatura e dimensões, não inspeção exaustiva de cada elemento. No SVG gerado, cobre XML e quantidade de rótulos. Nos PDFs, há 10, 10, 20, 40 e 100 páginas nos cinco portes, com 47/50, 282/300, 940/1.000, 1.880/2.000 e 4.700/5.000 rótulos inteiros encontrados. Abrir o arquivo não equivale a preservar todo o diagrama.

O SVG de 5.000 formas não foi obtido nas quatro execuções complementares documentadas, incluindo erros de timeout. Como o caminho de salvamento e as condições diferem da coleta original, esses resultados não são somados às 125 tentativas nem usados para inventar tempos ou reclassificar retroativamente cada tentativa de PDF. A causa do comportamento distinto não foi isolada.

O CSV e o procedimento de validação fundamentam a análise funcional; não foi alegada reabertura independente dos arquivos externos. Os arquivos estão no pacote `eficiencia-exportacoes-2026-11-15.zip`, disponível na pasta do Drive indicada no início deste README. A campanha funcional não mede tempos e não é somada às 125 tentativas oficiais.
