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
utilizada a branch `dev` do fork, no commit definido para a avaliação.

``` bash
git checkout <HASH_DO_COMMIT>
```

O identificador do commit deverá ser disponibilizado aos integrantes
para garantir a padronização do ambiente.

## Execução local

Com o repositório clonado, cada integrante poderá executar a avaliação descrita na documentação com uma versão fixa definida. 

## Atualização do código-fonte

Caso seja necessário atualizar a cópia local, execute:

``` bash
git pull origin dev
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
