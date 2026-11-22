# Obtenção e execução do ambiente de avaliação do draw.io

O ambiente de avaliação utiliza o fork
[H3ytt0r10/drawio](https://github.com/H3ytt0r10/drawio), derivado do
repositório oficial do draw.io. Cada integrante deverá clonar esse
repositório para sua máquina local, garantindo que todos utilizem o
código-fonte mantido para a avaliação de qualidade do software.

## Obtenção do código-fonte

Cada integrante deverá ter o Git instalado e executar os seguintes
comandos em um terminal:

``` bash
git clone https://github.com/H3ytt0r10/drawio.git
cd drawio
```

Para garantir que todos utilizem a mesma versão do código, será
utilizado o commit da campanha histórica, registrado no plano de avaliação.

``` bash
git checkout c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3
```

Esse commit corresponde à versão 32.6.10 documentada para a campanha histórica. A inspeção posterior de manutenibilidade informa outro commit base, `aacddaf44e6b4db468ef3f4f3e3bb56863f1d581`; seus registros devem permanecer separados, conforme a [coleta](../fase-4/coleta-de-dados.md#manutenibilidade-dupla-3).

## Execução local

Após fixar o commit, seguir o [protocolo de segurança](ambiente-de-execucao.md#seguranca-dupla-1) ou o [plano de eficiência](ambiente-de-execucao.md#eficiencia-de-desempenho-dupla-2), conforme a característica. Esses protocolos especificam ambientes distintos. A manutenibilidade utiliza análise estática do código, sem exigir que a interface web esteja em execução.

## Atualização do código-fonte

Para obter as referências remotas sem alterar o código da campanha, execute:

``` bash
git fetch origin
```

Entretanto, durante o período de avaliação, os integrantes deverão
permanecer no commit definido para os testes, evitando divergências
entre os ambientes.

## Verificação da versão utilizada

Para conferir se todos estão utilizando o mesmo código-fonte, execute:

``` bash
git rev-parse HEAD
```

O resultado deverá ser idêntico ao hash de commit compartilhado pelo
grupo.
