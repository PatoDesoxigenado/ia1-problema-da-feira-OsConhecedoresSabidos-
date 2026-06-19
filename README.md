# Problema da Feira
## Busca em Espaço de Estados, Agentes Inteligentes e Heurísticas

---

# Identificação do Grupo

> Preencha os dados do grupo antes da entrega.

**Nome do grupo:**

<!-- Escolha um nome para o grupo -->

**Integrantes:**

| Nome completo | Usuário GitHub | Questão do seminário |
|---|---|---|
| Luiz Fernando | [@PatoDesoxigenado](https://github.com/usuario) | 23 |
| Ana Kelry | [@kelryana](https://github.com/usuario) | 28 |
| Alerrandro Martins | [@Alerrandr0z0](https://github.com/usuario) | 44 |
| Thafine Jennifer | [@thafine](https://github.com/usuario) | 39 |

> A coluna "Questão do seminário" será preenchida após a atribuição pelo professor, uma semana antes da entrega.

---

# Sumário

- [1. Visão Geral da Atividade](#1-visão-geral-da-atividade)
- [2. Entrega e Avaliação](#2-entrega-e-avaliação)
- [3. Configuração do Repositório](#3-configuração-do-repositório)
- [4. Dependências](#4-dependências)
- [5. Mensagens de Commit](#5-mensagens-de-commit)
- [6. Objetivos da Atividade](#6-objetivos-da-atividade)
- [7. Estrutura do Projeto](#7-estrutura-do-projeto)
- [8. O Que Já Está Implementado](#8-o-que-já-está-implementado)
- [9. O Que Deve Ser Implementado](#9-o-que-deve-ser-implementado)
- [10. Execução](#10-execução)
- [11. Saída Esperada](#11-saída-esperada)
- [12. Relatório Técnico](#12-relatório-técnico)
- [13. Questionário Conceitual e Seminário](#13-questionário-conceitual-e-seminário)
- [14. Rubricas de Avaliação](#14-rubricas-de-avaliação)
- [15. Referências Bibliográficas](#15-referências-bibliográficas)

---

# 1. Visão Geral da Atividade

Esta atividade está organizada em **três unidades avaliativas**, todas entregues por meio de um único repositório Git privado.

| Unidade | Componente | Modalidade | Peso |
|---|---|---|---|
| 1ª Unidade | Implementação | Grupo | 100% |
| 2ª Unidade | Relatório Técnico | Grupo | 100% |
| 3ª Unidade | Questionário Conceitual | Grupo | 60% |
| 3ª Unidade | Seminário (apresentação de questão) | Individual | 40% |

O grupo deverá:

- implementar o comportamento heurístico do agente em [`./src/solucao.py`](./src/solucao.py);
- produzir o relatório técnico em [`./docs/Relatorio_Tecnico.md`](./docs/Relatorio_Tecnico.md);
- responder o questionário conceitual em [`./docs/Questionario.md`](./docs/Questionario.md);
- participar do seminário conceitual, com cada integrante apresentando individualmente uma questão do questionário.

> **Importante:** o trabalho é realizado em grupo, mas a apresentação do seminário é avaliada individualmente. Cada membro apresenta uma questão diferente. A nota do seminário é computada por aluno.

A contextualização teórica da atividade — modelagem formal, relação com o AIMA, busca, XAI (eXplanable Artifitial Intelligence) e sustentabilidade — está disponível em [`/docs/README.md`](/docs/README.md)


---

# 2. Entrega e Avaliação

## Datas

| Evento | Data | Horário |
|---|---|---|
| Entrega final (release no GitHub) | 22 de junho de 2026 | até 18h |
| Seminário conceitual | 25 de junho de 2026 | 7h |

Entregas fora do prazo não serão aceitas.

## Como entregar

A entrega se dá pela criação de uma **release** no repositório privado do grupo no GitHub:

> GitHub → Releases → Create a new release
>
> - Tag: `v1.0`
> - Título: `Entrega Final — Problema da Feira`

## Composição da nota — 3ª Unidade

| Parte | Descrição | Peso |
|---|---|---|
| Questionário conceitual | Respostas em  [`./docs/Questionario.md`](./docs/Questionario.md) | 60% (grupo) |
| Seminário | Apresentação individual de uma questão | 40% (individual) |

---

# 3. Configuração do Repositório

### 1. Crie um repositório privado no GitHub

Crie um repositório **privado** em sua conta do GitHub. Sugestão de nome:

```text
<nome-do-grpo>-ia1-problema-da-feira
```

### 2. Clone o repositório base

```bash
git clone https://github.com/AlyssonOliveira/ia1-problema-da-feira
cd ia1-problema-da-feira
```

### 3. Adicione o repositório privado como remote

```bash
git remote rename origin upstream
git remote add origin https://github.com/<seu-usuario>/<nome-do-grupo>-ia1-problema-da-feira.git
git push -u origin main
```

### 4. Conceda acesso ao professor

Adicione o professor como colaborador com permissão de **leitura** (*read*):

> GitHub → Settings → Collaborators → Add people
>
> Usuário do professor: **`AlyssonOliveira`**

### 5. Desenvolva no repositório privado

Todo o desenvolvimento deve ser feito no repositório privado. O repositório original **não deve ser modificado**.

### 6. Abra uma issue no repositório original

Após configurar o repositório privado e conceder acesso ao professor, o grupo
deverá abrir uma **issue** no repositório original da atividade informando que
o trabalho foi iniciado.

> Repositório original → aba **Issues** → **New issue**

A issue deve seguir o modelo abaixo:

**Título:**

```text
[Grupo] <Nome do grupo>
```

**Corpo:**

```text
## Identificação do grupo

**Nome do grupo:** <nome>

**Repositório privado:** https://github.com/<usuario>/<repositorio>

**Integrantes:**

| Nome completo | Usuário GitHub |
|---|---|
| <Nome> | @<usuario> |
| <Nome> | @<usuario> |
| <Nome> | @<usuario> |
| <Nome> | @<usuario> |
```

Esta issue serve como registro oficial de que o grupo iniciou a atividade e
permite ao professor verificar o acesso ao repositório privado antes da
entrega final.

### 7. Crie a release para entrega

Até **22 de junho de 2026 às 18h**, crie a release conforme descrito na seção anterior.

---

# 4. Dependências

Este projeto utiliza apenas a biblioteca padrão do Python, com exceção do
[`src/visualizacao.py`](src/visualizacao.py), que requer o `matplotlib`.

O grupo deverá manter o arquivo [`src/requirements.txt`](src/requirements.txt) em `src/` (já presente no repositório)
listando todas as bibliotecas externas utilizadas. O arquivo deve ser
atualizado sempre que uma nova dependência for adicionada ao projeto.

## Instalação

```bash
pip install -r src/requirements.txt
```

## Estado inicial do `requirements.txt`

Enquanto apenas o [`src/visualizacao.py`](src/visualizacao.py) utilizar dependência externa, o arquivo
deve conter:

```text
matplotlib>=3.7
```

## Regras práticas

- Nunca commitar um ambiente virtual (`.venv/`, `venv/`) — ele já está no
  `.gitignore`.
- Versões mínimas (`>=`) são preferíveis a versões fixas (`==`) em projetos
  acadêmicos, pois reduzem conflitos entre ambientes dos membros do grupo.
- Ao adicionar uma nova biblioteca, registrar imediatamente no
  [`src/requirements.txt`](src/requirements.txt) com um commit do tipo `chore`:

```text
chore: adicionar <biblioteca> ao requirements.txt
```

---

# 5. Mensagens de Commit

Este repositório adota a convenção **Conventional Commits** para padronizar
o histórico de desenvolvimento. O professor utilizará o histórico de commits
para acompanhar a progressão do trabalho e gerar o `CHANGELOG.md` da entrega.

## Formato

```text
<tipo>(<escopo>): <descrição curta no imperativo>
```

## Tipos permitidos

| Tipo | Quando usar |
|---|---|
| `feat` | nova funcionalidade implementada |
| `fix` | correção de comportamento incorreto |
| `refactor` | reestruturação de código sem mudança de comportamento |
| `test` | adição ou correção de testes |
| `docs` | alterações em documentação (READMEs, relatório, questionário) |
| `chore` | tarefas auxiliares (dependências, configuração, `.gitignore`) |
| `style` | formatação, indentação, sem alteração de lógica |

## Exemplos

```text
feat(solucao): implementar operador adicionar item
feat(solucao): implementar heurística h(s) = |orçamento - total|
feat(solucao): implementar política de aceitação por melhoria estrita
fix(solucao): corrigir cálculo do total quando quantidade é zero
refactor(solucao): extrair geração de candidatos para função própria
docs(relatorio): adicionar seção de resultados experimentais
docs(questionario): responder questões 1 a 5
chore: adicionar arquivo .gitkeep em src/logs/
```

## Regras práticas

- A descrição deve estar em **português**, no **imperativo** ("implementar",
  "corrigir", "adicionar" — não "implementado" nem "implementando").
- Uma linha por commit; sem ponto final.
- Commits atômicos: cada commit representa uma única alteração coerente.
- Não commitar arquivos gerados (`__pycache__/`, `src/logs/`).

---

# 6. Objetivos da Atividade

Ao final da atividade, o estudante deverá ser capaz de:

* modelar problemas como espaço de estados;
* representar problemas como grafos;
* compreender agentes inteligentes;
* implementar busca heurística estocástica;
* compreender busca local e busca em caminho;
* analisar heurísticas;
* discutir racionalidade limitada;
* compreender interpretabilidade e auditabilidade;
* analisar criticamente paradigmas de IA.

---

# 7. Estrutura do Projeto

```text
problema_da_feira/
├── docs
│   ├── README.md                   ← relatório técnico (a produzir)
│   └── Questionario.md             ← questionário conceitual (a responder)
├── src
│   ├── data
│   │   └── feira.csv
│   ├── logs/                       ← gerado automaticamente em execução
│   ├── main.py
│   ├── solucao.py                  ← implementação do agente (a completar)
│   ├── experimento.py              ← análise experimental (a implementar)
│   ├── visualizacao.py             ← geração de gráficos (a implementar)
│   ├── run.sh
│   └── README.md                   ← guia técnico de implementação
│   ├── requirements.txt            ← dependências do projeto (a manter)
├── .gitignore
└── README.md                       ← este arquivo
```

---

# 8. O Que Já Está Implementado

A infraestrutura fornecida em [`src/main.py`](src/main.py) já implementa:

* leitura do ambiente via CSV;
* parsing dos itens e preços;
* estrutura do agente e do estado;
* geração automática de logs em [`src/logs/`](src/logs/);
* formatação da saída;
* pipeline completo de execução.

---

# 9. O Que Deve Ser Implementado

### [`src/solucao.py`](`src/solucao.py) — comportamento do agente

* cálculo do total da cesta;
* função heurística `h(s)`;
* operadores de ação (adicionar, remover, substituir item);
* geração de candidatos;
* política de aceitação;
* melhoria iterativa;
* registro de ações em `entradas_log`.

Consulte [`src/README.md`](src/README.md) para detalhes técnicos sobre cada componente.

### [`src/experimento.py`](src/experimento.py) — análise experimental quantitativa

Script que executa o agente repetidamente com diferentes combinações de parâmetros (orçamento, limite de iterações, seed) e coleta métricas agregadas: taxa de soluções ótimas, erro médio, desvio padrão, número de iterações. Os resultados devem ser exportados para `src/data/resultados_experimento.csv` e utilizados na seção de resultados experimentais do relatório técnico.

### [`src/visualizacao.py`](src/visualizacao.py) — geração de gráficos

Script que lê os arquivos de log gerados pelo agente e o CSV produzido pelo `experimento.py` e gera gráficos para o relatório técnico. Gráficos esperados:

* curva de convergência de `h(s)` ao longo das iterações;
* comparação de curvas entre execuções com seeds distintas;
* distribuição do erro final entre execuções de um mesmo experimento;
* taxa de soluções ótimas por configuração de parâmetros.

> **Dependência:** [`src/visualizacao.py`](src/visualizacao.py) requer a biblioteca `matplotlib`.
> Registrar em [`src/requirements.txt`](src/requirements.txt) e instalar com `pip install -r src/requirements.txt`.

---

# 10. Execução

A partir do diretório `src/`:

```bash
# Execução simples
python3 main.py data/feira.csv 20.00

# Com limite de iterações e seed
python3 main.py data/feira.csv 20.00 10000 42

# Execuções experimentais automatizadas
./run.sh
```

---

# 11. Saída Esperada

```text
Laranja: 3
Banana: 10
Melancia: 3
Melão: 2
Manga: 2
TOTAL: 20.00
ERRO: 0.00
ITERACOES: 612
STATUS: OTIMA
LOG: src/logs/alice__feira__orc20_00__seed42__20260614_153022.txt
```

---

# 12. Relatório Técnico

O relatório deverá ser entregue em [`docs/Relatorio_Tecnico.md`](docs/Relatorio_Tecnico.md) e deverá conter:

1. introdução;
2. modelagem formal;
3. representação em grafos;
4. busca não informada;
5. busca heurística;
6. busca em caminho;
7. agentes inteligentes;
8. resultados experimentais;
9. discussão conceitual;
10. conclusão.

---

# 13. Questionário Conceitual e Seminário

### Parte 1 — Questionário (60% da 3ª Unidade — grupo)

As questões estão em [`docs/Questionario.md`](docs/Questionario.md). O grupo deverá preencher as respostas diretamente no arquivo, abaixo de cada enunciado.

### Parte 2 — Seminário (40% da 3ª Unidade — individual)

Uma semana antes da entrega, cada estudante receberá a atribuição de **uma questão** para apresentar individualmente no formato de seminário em **25 de junho de 2026**.

A apresentação deve priorizar explicação conceitual, argumentação técnica e relação com o projeto implementado. O seminário **não** consiste em leitura literal das respostas.

---

# 14. Rubricas de Avaliação

## 1ª Unidade — Implementação (grupo)

| Critério | Pontos |
|---|---:|
| Modelagem formal do problema | 1,5 |
| Representação do espaço de estados | 1,0 |
| Implementação da heurística | 1,5 |
| Implementação dos operadores de ação | 1,5 |
| Política de aceitação e melhoria iterativa | 1,5 |
| Registro de trajetória e logs | 1,0 |
| Clareza e organização do código | 1,0 |
| Funcionamento geral do agente | 1,0 |
| **Total** | **10,0** |

## 2ª Unidade — Relatório Técnico (grupo)

| Critério | Pontos |
|---|---:|
| Introdução e contextualização | 1,0 |
| Modelagem formal | 2,0 |
| Discussão sobre grafos e busca | 2,0 |
| Discussão heurística | 1,5 |
| Discussão sobre agentes | 1,0 |
| Análise experimental | 1,5 |
| Qualidade técnica do texto | 1,0 |
| **Total** | **10,0** |

## 3ª Unidade — Questionário + Seminário

**Questionário (60% — grupo):** nota atribuída ao grupo com base na qualidade coletiva das respostas.

**Seminário (40% — individual):**

| Critério | Pontos |
|---|---:|
| Clareza conceitual | 3,0 |
| Domínio técnico | 2,5 |
| Capacidade de análise crítica | 2,0 |
| Relação com o projeto implementado | 1,5 |
| Organização e comunicação | 1,0 |
| **Total** | **10,0** |

---

# 15. Referências Bibliográficas

> LUGER, George F. *Artificial Intelligence: Structures and Strategies for Complex Problem Solving*. 6. ed. Boston: Addison-Wesley/Pearson Education, 2009.

> RUSSELL, Stuart J.; NORVIG, Peter. *Artificial Intelligence: A Modern Approach*. 4. ed. Hoboken: Pearson, 2021.
