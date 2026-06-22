# Relatório Técnico
## Problema da Feira — Busca em Espaço de Estados, Agentes Inteligentes e Heurísticas

---

> **Grupo:**  Nome do grupo 
>
> **Integrantes:**  Nomes dos integrantes 
>
> **Repositório:**  URL do repositório privado 
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

 O "Problema da Feira" consiste em um desafio de otimização combinatória sob restrições definidas e estritas de orçamento, cujo propósito é encontrar uma coleção ideal de itens. O objetivo central desta atividade prática é projetar e implementar um agente inteligente estocástico (aleatório, imprevisível), denominado "Alice", que possui a capacidade de selecionar de forma autônoma uma combinação de produtos, e suas respectivas quantidades a partir de um arquivo CSV, de modo que o valor total da cesta de compras atinja exatamente o teto orçamentário alvo ou mitigue ao máximo o erro absoluto em relação a ele. 

No que se refere a teoria da computação e análise de complexidade, o cenário constitui uma variação direta de problemas reais classificados como NP-difíceis (Nondeterministic Polynomial time-hard), que implica que é improvável a existência de um algoritmo puramente determinístico em tempo polinomial para encontrar sua solução exata sob qualquer instância global atual. Na literatura clássica, a alocação de recursos desse gênero é mapeada através do "Problema da Mochila" (Knapsack Problem), que possui variadas vertentes, como a "mochila fracionária", limitada e sem limites. No problema da mochila tradicional, você olha para o Item A, e disso existe uma label binária onde o item é incluído de maneira única ("1") ou descartado ("0"), em outras palavras, ou leva (1) ou deixa (0) aquele item. O problema da feira assemelha-se à variação sem limites, permitindo que múltiplos exemplares de uma mesma denominação de item sejam empilhados de forma recursiva na cesta, onde a escolha atual depende de uma nova sub-escolha do mesmo tipo, fazendo com que haja uma expansão significativa do espaço combinatório, invalidando buscas exaustivas comuns. Significa que, tentar adivinhar a resposta certa testando todas as combinações possíveis na força bruta está fora de cogitação, porque o número de opções é tão absurdamente gigante que nenhum computador do mundo conseguiria terminar o cálculo em tempo útil.

No âmbito da Inteligência Artificial, a resolução desse problema exemplifica a transição de abordagens analíticas rígidas para esse paradigma. Para solucionar a alta complexidade do espaço de estados, artigos e estudos científicos contemporâneos dividem-se entre abordagens exatas de alto custo de hardware, como a programação dinâmica executada em paralelo sobre redes hiper hexa-celulares (HHC), e abordagens baseadas em inteligência computacional e de meta-heurísticas inspiradas na natureza, como o algoritmo de busca de águas-vivas artificiais (Artificial Jellyfish Search), que mimetiza o comportamento biológico desses organismos na busca por nutrientes no oceano. Alinhado a essa segunda vertente de exploração, este projeto estrutura o comportamento do agente através de um ciclo iterativo contínuo focado em perceber o ambiente, gerar candidatos aleatórios por operadores de ação locais (adicionar, remover ou substituir), avaliar o erro pela função heurística h(s)= ∣ORÇAMENTO−TOTAL∣, e decidir sobre a aceitação da melhoria estrita. Este tipo de modelo de IA clássica não apenas reduz drasticamente o tempo de inferência e a latência do sistema, como também atende diretamente às exigências contemporâneas de sustentabilidade (Green AI/IA Verde), evitando o consumo excessivo de energia e hardware.
---

## 2. Modelagem Formal

 Defina formalmente: ambiente, estado, ações, espaço de estados, objetivo e heurística. Use a notação apresentada na contextualização. 

---

## 3. Representação em Grafo

 Explique como o problema se estrutura como grafo implícito: nós, arestas, caminhos e transições. Inclua exemplos concretos com os itens de data/feira.csv. 

---

## 4. Busca Não Informada

 Discuta BFS, DFS e a explosão combinatória do espaço de estados deste problema. Argumente por que busca exaustiva é inviável. 

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

A agente inteligente projetada, "Alice", é um programa executado em um sistema físico para implementar uma função matemática abstrata. O comportamento da Alice é formalmente descrito por uma função de agente que mapeia qualquer sequência de perceptos observada até o momento para uma ação correspondente a ser executada no ambiente. De acordo com os fundamentos estabelecidos por Russell & Norvig, esse ciclo de interação ocorre de forma contínua através de sensores e atuadores. Por meio de seus sensores, o agente captura o conteúdo do arquivo data/feira.csv e a meta do orçamento estipulado, estabelecendo os perceptos que servem de entrada para as decisões algorítmicas. Em resposta a esse fluxo de percepção, a Alice aciona seus atuadores virtuais para aplicar ações direcionadas no domínio da feira, alterando o estado da cesta de compras por meio de operadores locais e gerando uma trajetória contínua de transições que modifica o universo do problema.  

O conceito de racionalidade aplicado ao projeto afasta-se de inferências lógicas puras e prioriza uma abordagem prática voltada a metas. Um agente racional perfeito e idealizado deve agir para alcançar o melhor resultado absoluto com base nas informações disponíveis. No entanto, em ambientes complexos, a aplicação da racionalidade perfeita exigiria o mapeamento de uma tabela infinita contendo todas as combinações de sequências de perceptos possíveis, o que se mostra computacionalmente inviável diante das severas demandas de hardware e tempo. Por esse motivo, a arquitetura da Alice foi construída sob os preceitos de racionalidade limitada, operando de forma apropriada e eficiente mesmo sob restrições severas de recursos por meio de um limite máximo de iterações, que atua como seu orçamento computacional fixo. Diante da impossibilidade de vasculhar sistematicamente o grafo de decisões, o agente foca suas operações sobre o estado atual através de modificações locais, buscando alcançar a meta sem a necessidade de rastrear a árvore completa de caminhos.  

Diante disso, o algoritmo direciona a busca transformando a minimização do erro em um problema de maximização, definindo a função objetivo como o valor negativo do custo heurístico absoluto. Dessa forma, o agente escala a paisagem de estados em direção ao ponto de menor erro (gradiente descente). O ciclo iterativo gera estados vizinhos por meio de perturbações estocásticas de pequena escala na cesta. Aplicando a estratégia de hill-climbing de primeira escolha (first-choice), a Alice adota imediatamente a primeira modificação gerada que resulte em uma melhoria estrita sobre o estado atual, eliminando a necessidade de avaliar vizinhos alternativos. Embora essa abordagem probabilística pareça caótica a curto prazo, ela opera com complexidade de memória mínima, armazenando apenas o estado corrente e alta eficiência em espaços de busca exponenciais. O comportamento macro do sistema emerge dessa amostragem pseudoaleatória combinada à capacidade de exploração local, mitigando o aprisionamento em máximos locais que costumam paralisar algoritmos gulosos puros em problemas NP-difíceis e convergindo eficientemente para a solução ótima global com baixo custo computacional.

---

## 8. Resultados Experimentais

## 8. Resultados Experimentais

Os testes estatísticos conduzidos em lote pelo módulo `experimento.py` geraram dados quantitativos detalhados sobre o desempenho do algoritmo sob diferentes cenários de simulação. A execução cruzou de forma sistemática três metas orçamentárias distintas, três limites de iterações e diferentes sementes aleatórias, imprimindo no terminal de execução a tabela de métricas agregadas reproduzida a seguir:

| Orçamento | Limite de Iterações | Taxa de Sucesso | Erro Médio | Média de Iterações |
| :--- | :--- | :--- | :--- | :--- |
| R$ 20.00 | 1000 | 100.0 % | 0.00 | 48.4 |
| R$ 20.00 | 5000 | 100.0 % | 0.00 | 48.4 |
| R$ 20.00 | 10000 | 100.0 % | 0.00 | 48.4 |
| R$ 50.00 | 1000 | 100.0 % | 0.00 | 97.2 |
| R$ 50.00 | 5000 | 100.0 % | 0.00 | 97.2 |
| R$ 50.00 | 10000 | 100.0 % | 0.00 | 97.2 |
| R$ 100.00 | 1000 | 100.0 % | 0.00 | 190.6 |
| R$ 100.00 | 5000 | 100.0 % | 0.00 | 190.6 |
| R$ 100.00 | 10000 | 100.0 % | 0.00 | 190.6 |

Os dados consolidados indicam que a taxa de soluções ótimas atingiu o patamar de 100.0% em todas as combinações de parâmetros operacionais, resultando em um erro médio nulo (0.00). Essa convergência absoluta comprova a eficiência da heurística implementada em alinhar a composição da cesta ao teto financeiro estabelecido, sem sofrer influência negativa das perturbações aleatórias. A distribuição homogênea desse sucesso em todo o espectro de testes está documentada visualmente nas saídas geradas pelo script `visualizacao.py`, conforme exibido na Figura 1 e na Figura 2.

[Figura 1: Distribuição do erro final h(s) por orçamento](../src/data/graficos/03_histograma_erro.png)

[Figura 2: Taxa de soluções ótimas por orçamento e limite de iterações](../src/data/graficos/04_taxa_otimas.png)

A avaliação da eficiência computacional aponta que o orçamento-alvo exerce um impacto linear direto sobre o esforço do agente. Enquanto a meta de R$ 20.00 requereu uma média estável de 48.4 iterações, o cenário de R$ 50.00 demandou 97.2 ciclos, e a configuração máxima de R$ 100.00 necessitou de 190.6 passos. Essa variação decorre da profundidade do estado objetivo dentro do grafo implícito: quanto maior a meta financeira, maior o volume de itens acumulados ou substituídos na cesta, o que exige um número expandido de transições de estado para que a descida do gradiente heurístico alcance a otimalidade. Em contrapartida, as alterações aplicadas nos limites máximos de iterações (1.000, 5.000 e 10.000) não geraram flutuações nas métricas, uma vez que o mecanismo estocástico de primeira escolha (*first-choice*) resolveu todas as instâncias do problema muito antes de tangenciar o menor teto computacional estipulado.

A análise dinâmica do comportamento do agente ao longo do tempo foi realizada por meio do rastreamento de uma das trajetórias armazenadas na pasta de logs. A Figura 3 ilustra a evolução da curva de convergência para o cenário de R$ 30.00 sob a semente 42, iniciando a busca em um erro absoluto de 30.00 com a cesta vazia. O gráfico evidencia quedas abruptas na distância heurística intercaladas por patamares horizontais de estabilização, os quais registram momentos em que o sorteio probabilístico gerou candidatos inválidos rejeitados pela política de aceitação, alcançando o erro zero em definitivo na iteração 56.

[Figura 3: Curva de convergência de h(s) ao longo das iterações](../src/data/graficos/01_convergencia.png)

A influência da estocasticidade no tempo de resposta do sistema torna-se evidente ao sobrepor o desempenho de múltiplas sementes no mesmo cenário. Conforme ilustrado na comparação de convergência da Figura 4, a semente 100 obteve uma trajetória acelerada e livre de retenções severas, solucionando a alocação de recursos por volta da iteração 41. Em contrapartida, a semente 2026 enfrentou zonas de platô mais extensas ao longo da paisagem de estados, necessitando de 67 ciclos para consolidar o resultado ideal. Essa oscilação de percurso valida a robustez adaptativa da engenharia do agente inteligente, visto que, apesar de as decisões locais pseudoaleatórias variarem os caminhos explorados a curto prazo, a filtragem lógica estruturada baseada no gradiente do erro heurístico garante a convergência inescapável para o ótimo global.

[Figura 4: Comparação de curvas de convergência entre três seeds distintas](../src/data/graficos/02_comparacao_seeds.png)

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

> MAHAFZAH, Basel A.; AL-TAWIL, Marwan; KRUNZ, Marwan. 0/1 Knapsack problem on hyper hexa-cell interconnection network. Cluster > Computing, v. 29, n. 2, 2026.

> LUGER, George F. *Artificial Intelligence: Structures and Strategies
> for Complex Problem Solving*. 6. ed. Boston: Addison-Wesley/Pearson
> Education, 2009.

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern
> Approach*. 4. ed. Hoboken: Pearson, 2021.

> YILDIZDAN, G.; BAŞ, E. A novel binary artificial jellyfish search algorithm for solving 0-1 knapsack problems. *Neural
> Processing Letters*, v. 55, n. 7, p. 8605–8671, 2023.



