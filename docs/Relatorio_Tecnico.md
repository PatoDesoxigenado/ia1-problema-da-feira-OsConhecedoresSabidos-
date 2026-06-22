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

 Explique a heurística h(s) implementada, a política de aceitação adotada e o mecanismo de melhoria iterativa. Discuta as escolhas de projeto realizadas. 

---

## 6. Busca em Caminho

 Explique como o agente registra sua trajetória, o papel dos logs e como isso contribui para interpretabilidade e auditabilidade. 

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
