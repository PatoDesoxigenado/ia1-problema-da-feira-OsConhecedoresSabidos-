# Relatório Técnico
## Problema da Feira — Busca em Espaço de Estados, Agentes Inteligentes e Heurísticas

---

> **Grupo:**  OsConhecedoresSabidos
>
> **Integrantes:**  Ana Kelry Fernandes Cabral do Nascimento | Luiz Fernando Santos Teixeira | Thafine Jennifer Viana Siqueira | Alerrandro de Moura Martins |
>
> **Repositório:**  [URL do repositório privado](https://github.com/PatoDesoxigenado/ia1-problema-da-feira-OsConhecedoresSabidos-) 
>
> **Data de entrega:** 22 de junho de 2026

---

> A contextualização teórica deste relatório — modelagem formal, relação
> com o AIMA, busca, XAI e sustentabilidade — está disponível em
> [`docs/README.md`](README.md) e deve ser utilizada como base para a redação das
> seções abaixo. O relatório deve ser autoral: não copie a contextualização,
> aplique-a à sua implementação.

---

# Sumário

- [1. Introdução](#1-introdução)
- [2. Modelagem Formal](#2-modelagem-formal)
- [3. Representação em Grafo](#3-representação-em-grafo)
- [4. Busca Não Informada](#4-busca-não-informada)
- [5. Busca Heurística](#5-busca-heurística)
- [6. Busca em Caminho](#6-busca-em-caminho)
- [7. Agente Inteligente](#7-agente-inteligente)
- [8. Resultados Experimentais](#8-resultados-experimentais)
- [9. Discussão Conceitual](#9-discussão-conceitual)
- [10. Conclusão](#10-conclusão)
- [Referências Bibliográficas](#referências-bibliográficas)

---

## 1. Introdução

 Explique o problema, os objetivos da atividade e a relação com IA. 

---

## 2. Modelagem Formal

 Defina formalmente: ambiente, estado, ações, espaço de estados, objetivo e heurística. Use a notação apresentada na contextualização.
 
 O Problema da Feira pode ser formalmente modelado como um problema de busca em espaço de estados, onde os componentes são definidos da seguinte maneira:
 - Ambiente: É estático e determinístico, composto por um dicionário de preços de catálogo P (onde P_Laranja = 0.50, P_Banana = 0.05, etc.) e um limite de Orçamento O definido na execução.
 - Estados: Representação a configuração do momento na cesta de Alice. Se baseia na quantidade de variáveis que ela possui disponível. N = {Laranja : q1, Banana : q2, Melancia : q3, Melão : q4, Manga : q5}
 - Ações: É basicamente o conjunto de operadores que altera de alguma forma o estado atual. Pode se classificar como adicionar, que incrementa a quantidade de algum item na cesta, o remover que decrementa a quantidade de algum item na cesta e temos o substituir que, respectivamente, remove e adiciona algum item.
 - Espaço de Estados: Seria tecnicamente a junção de todas as possibilidades possíveis de combinação na cesta, que teoricamente é infinito, mas computacionalmente falando ele se limita às interações
 
 O objetivo desse agente é buscar um estado que tenha resultado satisfatório em relação a ser idêntico/o mais próximo possível do orçamento.
 Heurística: h(s) = | Orçamento - Total(itens)|

---

## 3. Representação em Grafo

 Explique como o problema se estrutura como grafo implícito: nós, arestas, caminhos e transições. Inclua exemplos concretos com os itens de data/feira.csv. 

Na nossa implementação, o problema da feira estrutura-se como um grafo implícito. Isso significa que os nós e caminhos não são instanciados todos de uma vez na memória; eles são gerados dinamicamente sob demanda sempre que um operador de ação é acionado.
- Nós: Eles representam cada estado único da cesta, iniciando no nó raiz com todos os itens da cesta zerados.
- Arestas: A conexão entre os nós ocorre quando uma ação é executada, assim alterando o estado da cesta, como por exemplo sair do nó raiz estando como: N = {Laranja : 0}, e ao passar por uma ação Adicionar (Laranja), ele ficaria: N = {Laranja : 1}
- Caminhos: É a sequência de nós visitados e de ações tomadas. No nosso modelo, o caminho equivale à trajetória de logs gerada pelo agente até encontrar o objetivo.
Exemplo de Caminho: Um trajeto curto seria s0 -(Adicionar[Melancia])> s1-(Adicionar[Manga])> s2-(Remover[Melancia])> s3.
---

## 4. Busca Não Informada

 Discuta BFS, DFS e a explosão combinatória do espaço de estados deste problema. Argumente por que busca exaustiva é inviável.

No contexto do Problema da Feira, algoritmos de busca não informada são extremamente ineficientes. Por não possuir um limite físico rígido predefinido, expandir os nós de forma sistemática sem nenhuma função de revisar isso, como ocorre em uma Busca em Largura ou Profundidade, resultaria em uma explosão combinatória. O agente esgotaria os recursos computacionais testando alocações de forma totalmente aleatória antes de sequer encontrar um valor que encontrasse uma combinação satisfatória.

---

## 5. Busca Heurística

A busca heurística do agente Alice implementa o algoritmo de *Stochastic Hill-Climbing* — uma variante da subida de encosta que, a cada iteração, sorteia um único estado candidato em vez de avaliar exaustivamente todos os vizinhos.

### 5.1 Heurística adotada

A função heurística do agente é o erro absoluto entre o total da cesta e o orçamento alvo:

`h(s) = |orçamento - total(s)|`

Onde `total(s) = Σ (q_i × p_i)` para todo item `i`, sendo `q_i` a quantidade do item `i` no estado `s` e `p_i` o seu preço. O objetivo do agente é minimizar `h(s)`: quanto mais próximo de zero, melhor. Quando `h(s) = 0`, a cesta utiliza exatamente o orçamento disponível — solução ótima.

### 5.2 Operadores estocásticos

Em cada iteração, o agente sorteia uniformemente um entre três operadores para gerar um candidato:

- **Adicionar item** (`adicionar_item`): incrementa em 1 a quantidade de um item aleatório. Representa a compra de mais uma unidade.
- **Remover item** (`remover_item`): decrementa em 1 a quantidade de um item (se maior que zero). Representa a devolução de uma unidade.
- **Substituir item** (`substituir_item`): remove 1 unidade de um item e adiciona 1 de outro. Representa a troca direta entre dois produtos.

Os itens alvo também são sorteados com `random.choice()`. Quando o operador sorteado é "remover" ou "substituir" mas a cesta está vazia (todos os itens com quantidade zero), a iteração é pulada com um registro no log indicando a impossibilidade da ação — evitando estados inválidos sem interromper a busca.

Essa geração aleatória diferencia o algoritmo do *Steepest-Ascent Hill Climbing*, que avaliaria todos os vizinhos para escolher o melhor. A vantagem da abordagem estocástica é o custo computacional constante por iteração (`O(1)`), permitindo explorar centenas ou milhares de candidatos no mesmo tempo em que a subida mais íngreme avaliaria apenas uma fração deles.

### 5.3 Política de aceitação estrita

A aceitação do candidato segue o critério de melhoria estrita:

`aceita(s, s')` ⇔ `h(s') < h(s)`

Ou seja, o agente **só** transiciona para o candidato se o erro diminuir. Se o erro for igual ou maior, o estado atual é mantido. Essa política produz uma trajetória monoticamente decrescente no erro heurístico — cada transição registrada representa uma melhoria real.

Do ponto de vista de projeto, essa escolha é deliberada: a política estrita é simples, determinística na decisão e garante que o agente nunca regrida. No espaço de estados do Problema da Feira, onde o objetivo é um valor numérico preciso, a estocasticidade dos operadores compensa a rigidez da aceitação — se um candidato não melhora o erro, o próximo pode ser melhor.

### 5.4 Critério de parada

O agente encerra a busca quando:

1. **Erro zero**: `h(s) = 0` — solução ótima encontrada (status `OTIMA`).
2. **Limite de iterações**: o número máximo de iterações (`max_iter`, padrão 10.000) é atingido — solução aproximada (status `APROXIMADA`).

Na prática, para o cenário com orçamento de R$ 20,00, o agente frequentemente converge em aproximadamente 70 iterações, como ilustra o log de execução analisado na Seção 6. A combinação de operadores estocásticos com política estrita demonstra ser eficaz para este problema: a aleatoriedade garante diversidade de exploração, enquanto a aceitação estrita assegura que cada passo é uma melhoria concreta.

---

## 6. Busca em Caminho

### 6.1 Registro da trajetória

A cada iteração, o agente registra uma entrada textual contendo três informações:

1. **Ação executada**: o operador e o(s) item(ns) envolvidos (ex: `adicionar Laranja`, `substituir Melancia por Banana`).
2. **Total acumulado**: valor monetário atual da cesta.
3. **Erro heurístico**: `h(s)` do estado corrente.

Essas entradas são armazenadas em uma lista (`entradas_log`) durante a execução do agente em `solucao.py`. Ao final, o módulo `main.py` persiste essa lista em um arquivo texto em `src/logs/`, com formato:

```
[1] adicionar Laranja | TOTAL=0.50 | ERRO=19.50
[2] adicionar Banana  | TOTAL=0.55 | ERRO=19.45
...
[69] remover Banana   | TOTAL=20.00 | ERRO=0.00
```

O arquivo completo inclui ainda:
- **Cabeçalho**: nome do agente, arquivo CSV de itens, orçamento, limite de iterações, seed do gerador pseudoaleatório e timestamp da execução.
- **Itens disponíveis**: lista completa de itens e preços carregados do ambiente — garante que o contexto da decisão está documentado.
- **Rodapé**: estado final da cesta, total, erro, número de iterações e status (`OTIMA` ou `APROXIMADA`).

O nome do arquivo de log segue o padrão semântico `<agente>__<csv>__orc<orçamento>__seed<seed>__<timestamp>.txt`, permitindo identificar rapidamente os parâmetros de cada execução sem precisar abrir o arquivo.

### 6.2 Log e Inteligência Artificial Explicável (XAI)

O sistema de logs do agente Alice concretiza os quatro pilares da XAI no contexto do Problema da Feira:

- **Transparência**: o código do agente (`solucao.py`) é aberto e cada linha corresponde a um conceito do AIMA — estado, operador, heurística, critério de aceitação. O log documenta tanto o código quanto os parâmetros do ambiente, não havendo nenhuma lógica oculta.

- **Rastreabilidade**: cada decisão individual está registrada em ordem cronológica. É possível percorrer a trajetória iteração por iteração e ver exatamente quando cada item foi adicionado, removido ou substituído. O erro decrescente pode ser observado passo a passo, permitindo identificar, por exemplo, iterações que não produziram melhoria (quando a ação sorteada não reduziu o erro).

- **Interpretabilidade**: os símbolos manipulados pelo agente são entidades do mundo real — "Laranja", "Melancia", "R$ 0,50" — não vetores numéricos abstratos. Qualquer pessoa com conhecimento do domínio da feira pode compreender o significado de cada ação.

- **Reprodutibilidade**: a seed do gerador pseudoaleatório é explicitamente registrada no cabeçalho do log. Com a mesma seed e os mesmos parâmetros, a sequência de ações é exatamente a mesma, permitindo que terceiros reproduzam e verifiquem o comportamento do agente.

### 6.3 Contraste com sistemas caixa-preta

Diferentemente de uma rede neural profunda, onde as "decisões" emergem de bilhões de pesos sinápticos ajustados por gradiente descendente em um espaço latente de alta dimensionalidade — inacessível à inspeção humana direta — o agente Alice expõe **publicamente**:

- Seu estado interno (o dicionário de quantidades)
- Sua função heurística (o cálculo do erro absoluto)
- Seus operadores (cada função nomeada em `solucao.py`)
- Seu critério de aceitação (a comparação de erros)
- Sua trajetória completa (o arquivo de log)

Não há nenhuma opacidade. Um engenheiro pode abrir o log, inspecionar a iteração 42, ver que o agente removeu Banana porque o erro era 0,05 e o total 20,05, compreender a lógica e, se necessário, modificar o comportamento ajustando a heurística ou a política de aceitação. Essa é a essência da IA explicável: o sistema não apenas produz uma solução, mas documenta o processo que a produziu, de forma que um humano possa auditá-lo e, criticamente, confiar nele.

---

## 7. Agente Inteligente

 Explique o ciclo percepção–ação do agente, a noção de racionalidade aplicada, as decisões tomadas e o comportamento emergente observado. 

---

## 8. Resultados Experimentais

 Apresente os resultados obtidos com experimento.py.
 Inclua tabelas, gráficos gerados por visualizacao.py e análise dos logs. Discuta o efeito de seeds, orçamentos e limites de iterações sobre a qualidade da solução. 

---

## 9. Discussão Conceitual

 Relacione a implementação com os conceitos teóricos estudados.
 Discuta as limitações do agente, compare com outras abordagens
 de IA e reflita sobre racionalidade, heurística e emergência. 

---

## 10. Conclusão

 Sintetize os resultados, os principais aprendizados, as dificuldades encontradas e as possíveis extensões do projeto. 

---

## Referências Bibliográficas

> LUGER, George F. *Artificial Intelligence: Structures and Strategies
> for Complex Problem Solving*. 6. ed. Boston: Addison-Wesley/Pearson
> Education, 2009.

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern
> Approach*. 4. ed. Hoboken: Pearson, 2021.
