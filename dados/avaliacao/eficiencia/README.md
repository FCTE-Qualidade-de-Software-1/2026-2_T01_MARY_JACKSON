# Evidências de eficiência de desempenho

Dados da coleta de 14/11/2026, realizada no draw.io 32.6.10. A coleta oficial contém 125 tentativas: cinco portes, cinco operações e cinco repetições. Os pilotos são preservados à parte e não entram no cálculo das métricas da coleta oficial.

## Responsáveis

- **Coleta:** Pedro Ian Guedes de Carvalho.
- **Análise dos dados e resultados:** Thiago Gomes Pereira de Abreu. A análise está na seção de eficiência de [Análise dos dados e resultados](../../../docs/fase-3/resultados.md).

## Acesso às evidências

**Pasta no Google Drive:** [Mary Jackson - Eficiência de Desempenho - Evidências da Coleta](https://drive.google.com/drive/folders/1jwootYRyhx7-tQTW6iViqpkXdaKxO7FM?usp=sharing).

| Pacote | Conteúdo | Tamanho aproximado |
| --- | --- | --- |
| `eficiencia-coleta-2026-11-14.zip` | 125 traces da coleta oficial, em `dados/avaliacao/eficiencia/brutos/traces/`. | 427 MiB |
| `eficiencia-pilotos-2026-11-14.zip` | 10 traces do piloto automatizado e 4 do manual, em `dados/avaliacao/eficiencia/brutos/piloto/` e `manual/`. | 49 MiB |

Os pacotes conservam os nomes dos arquivos e os caminhos a partir da raiz do repositório. Os traces `.json.gz` ficam fora do versionamento Git; as cópias locais restauradas são ignoradas pelo `.gitignore`. O arquivo [SHA256SUMS.txt](SHA256SUMS.txt) permite conferir a integridade dos dois ZIPs e dos 139 traces.

O contexto de execução e os registros das medidas estão na seção de eficiência da página [Coleta de dados](../../../docs/fase-3/coleta-de-dados.md).

## Arquivos mantidos no Git

| Caminho relativo a esta pasta | Conteúdo |
| --- | --- |
| `coletar.py` | Automação da coleta. |
| `ler_traces.py` | Extração das medidas dos traces. |
| `cargas/gerar_cargas.py` | Geração das cinco cargas sintéticas. |
| `cargas/carga-*.drawio` | Cargas de 50, 300, 1.000, 2.000 e 5.000 formas. |
| `brutos/tentativas.csv` | 125 registros da coleta oficial, com nomes dos traces e instantes usados nas medidas. |
| `brutos/piloto/piloto.csv` | Registros do piloto automatizado. |
| `brutos/piloto/manual/piloto_manual.csv` | Registros do piloto manual. |
| `SHA256SUMS.txt` | Hashes dos pacotes externos e dos traces. |

## Restaurar os traces localmente

Baixe os dois ZIPs pelo link da pasta de evidências. No PowerShell, abra a raiz do repositório e execute os comandos abaixo, ajustando a pasta de download se necessário:

```powershell
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-coleta-2026-11-14.zip" -DestinationPath .
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-pilotos-2026-11-14.zip" -DestinationPath .
```

A extração recria os caminhos de `dados/avaliacao/eficiencia/brutos/`. Não extraia os pacotes dentro desta pasta de eficiência, pois isso duplicaria a estrutura `dados/avaliacao/eficiencia/`.

## Conferir a integridade

As duas primeiras entradas do [manifesto SHA-256](SHA256SUMS.txt) correspondem aos ZIPs. As demais correspondem aos traces, com caminhos relativos à raiz do repositório.

Para conferir os pacotes no PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-coleta-2026-11-14.zip"
Get-FileHash -Algorithm SHA256 -LiteralPath "$env:USERPROFILE\Downloads\eficiencia-pilotos-2026-11-14.zip"
```

Compare cada resultado com a entrada do mesmo nome no manifesto. Para conferir um trace após a extração, execute `Get-FileHash` sobre o caminho indicado na entrada correspondente e compare o resultado.

## Conferir a extração das medidas

Os critérios de leitura estão no [plano de avaliação](../../../docs/fase-3/index.md). Para executar novamente o leitor sobre a coleta oficial, a partir da raiz do repositório:

```powershell
python dados/avaliacao/eficiencia/ler_traces.py dados/avaliacao/eficiencia/brutos/traces "$env:TEMP\tentativas-eficiencia-conferencia.csv"
```

A saída usa um arquivo separado para preservar `brutos/tentativas.csv`. As tabelas, gráficos e julgamentos da análise devem ser produzidos separadamente, mantendo a rastreabilidade para as tentativas oficiais.

## Análise dos dados e resultados

Execute `python dados/avaliacao/eficiencia/analisar.py` na raiz do repositório para reproduzir a análise. O script preserva os dados brutos e gera `analise/tentativas-classificadas.csv`, `analise/metricas-por-cenario.csv` e `analise/resumo.json`, além de atualizar apenas a seção de eficiência da página de resultados.

As notas são exploratórias, pois os limites ainda constam como candidatos. A revisão pós-coleta de 15/11/2026 atribui nota temporal 1 a cenários com menos de quatro sucessos por falha do produto e julga memória por medidas completas das operações concluídas. Dados ausentes ou inválidos continuam não conclusivos. O histórico dessa revisão está em `analise/revisao-criterios.json`. O script verifica os hashes dos insumos normalizados para LF e exige revisão se os dados ou critérios mudarem.
