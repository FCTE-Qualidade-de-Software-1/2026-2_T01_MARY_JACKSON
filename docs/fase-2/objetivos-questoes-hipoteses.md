# Objetivos, questões e hipóteses

<!-- O que entra aqui: um objetivo por característica no template GQM (Aula 08, pág. 24), as questões de cada objetivo e uma hipótese por questão. As abstraction sheets das duplas podem entrar aqui (Aula 08, pág. 29). Rubrica F2-C1 a C3. -->

_Em elaboração._

## Segurança (Dupla 1)

## Eficiência de desempenho (Dupla 2)

## Manutenibilidade (Dupla 3)

### Objetivo de medição

| Elemento | Descrição |
| --- | --- |
| Identificador | G3 |
| Objeto | Código-fonte dos componentes de importação de arquivos, edição de rótulos e exportação PNG/PDF/SVG do _draw.io_. |
| Propósito | Avaliar a manutenibilidade dos componentes selecionados. |
| Foco | Analisabilidade e modificabilidade. |
| Ponto de vista | Desenvolvedores responsáveis pela manutenção do software. |
| Contexto | Manutenção e evolução dos componentes selecionados do _draw.io_, versão 32.2.0. |

### Questões e hipóteses

As questões e hipóteses foram definidas para orientar a avaliação da manutenibilidade dos três componentes selecionados.

| Questão | Hipótese |
| --- | --- |
| **Q3.1**<br>Em que medida a complexidade do código responsável pela leitura e conversão de arquivos pode dificultar sua compreensão e manutenção? | **H3.1**<br>O código de importação apresenta complexidade cognitiva média inferior ou igual a 10 por função. |
| **Q3.2**<br>Em que medida a complexidade do código responsável pela edição e formatação de rótulos pode dificultar sua compreensão e manutenção? | **H3.2**<br>O código de edição de rótulos apresenta complexidade cognitiva média inferior ou igual a 10 por função. |
| **Q3.3**<br>Em que medida a duplicação de código entre as implementações de exportação PNG, PDF e SVG pode dificultar futuras modificações? | **H3.3**<br>O percentual de código duplicado no escopo de exportação é inferior ou igual a 5%. |
