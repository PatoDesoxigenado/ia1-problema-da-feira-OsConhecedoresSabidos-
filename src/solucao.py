#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira

Este módulo implementa o agente Alice.
"""

from collections import namedtuple
import random


# ============================================================
# Estrutura de retorno
# ============================================================

Resultado = namedtuple(
    "Resultado",
    [
        "estado",
        "total",
        "erro",
        "iteracoes",
        "status",
        "entradas_log",
        "log"
    ]
)

# ============================================================
# Funções Auxiliares (Operadores e Cálculos)
# ============================================================

def calcular_total(estado, itens):
    """
    Calcula o valor total da cesta somando a (quantidade * preço) 
    de cada item presente no estado.
    """
    total = 0.0
    for item, quantidade in estado.items():
        total += quantidade * itens[item]
    return total

def calcular_heuristica(total, orcamento):
    """
    Calcula o erro absoluto h(s) da cesta atual.
    Quanto mais próximo de 0, melhor é o estado.
    """
    return abs(orcamento - total)

def adicionar_item(estado, item):
    """
    Retorna um novo estado (candidato) com +1 unidade do item escolhido.
    """
    novo_estado = estado.copy()
    novo_estado[item] += 1
    return novo_estado

def remover_item(estado, item):
    """
    Retorna um novo estado (candidato) com -1 unidade do item escolhido.
    Garante que a quantidade não fique negativa.
    """
    novo_estado = estado.copy()
    if novo_estado[item] > 0:
        novo_estado[item] -= 1
    return novo_estado

def substituir_item(estado, item_sai, item_entra):
    """
    Retorna um novo estado (candidato) removendo 1 unidade do 'item_sai' 
    (se possível) e adicionando 1 unidade do 'item_entra'.
    """
    novo_estado = estado.copy()
    if novo_estado[item_sai] > 0:
        novo_estado[item_sai] -= 1
        novo_estado[item_entra] += 1
    return novo_estado

# ============================================================
# Agente Alice
# ============================================================

def agente_alice(
    ambiente,
    max_iter=10000,
    seed=None
):
    """
    Agente heurístico estocástico.
    """

    if seed is not None:
        random.seed(seed)

    # Percepção do ambiente
    itens = ambiente["itens"]
    orcamento = ambiente["orcamento"]
    lista_itens = list(itens.keys())

    # Estado inicial do agente (cesta vazia)
    estado = {item: 0 for item in lista_itens}

    # Variáveis da busca
    total = calcular_total(estado, itens)
    erro = calcular_heuristica(total, orcamento)
    iteracoes = 0
    entradas_log = []

    for i in range(1, max_iter + 1):
        iteracoes = i

        if erro == 0.0:
            break

        #
        # Geração de candidatos
        #

        lista_itens = list(itens.keys())
        operador = random.choice(["adicionar", "remover", "substituir"])

        if operador == "adicionar":
            item = random.choice(lista_itens)
            candidato = adicionar_item(estado, item)
            acao = f"adicionar {item}"

        elif operador == "remover":
            itens_possiveis = [i for i in lista_itens if estado[i] > 0]
            if not itens_possiveis:
                entradas_log.append(
                    f"[{i}] remover (impossivel)"
                    f" | TOTAL={total:.2f}"
                    f" | ERRO={erro:.2f}"
                )
                continue
            item = random.choice(itens_possiveis)
            candidato = remover_item(estado, item)
            acao = f"remover {item}"

        elif operador == "substituir":
            itens_possiveis = [i for i in lista_itens if estado[i] > 0]
            if not itens_possiveis:
                entradas_log.append(
                    f"[{i}] substituir (impossivel)"
                    f" | TOTAL={total:.2f}"
                    f" | ERRO={erro:.2f}"
                )
                continue
            item_sai = random.choice(itens_possiveis)
            item_entra = random.choice([i for i in lista_itens if i != item_sai])
            candidato = substituir_item(estado, item_sai, item_entra)
            acao = f"substituir {item_sai} por {item_entra}"

        #
        # Avaliação do candidato
        #

        total_candidato = calcular_total(candidato, itens)
        erro_candidato = calcular_heuristica(total_candidato, orcamento)

        #
        # Política de aceitação (melhoria estrita)
        #

        if erro_candidato < erro:
            estado = candidato
            total = total_candidato
            erro = erro_candidato

        #
        # Registro de trajetória (XAI) — a cada iteração
        #

        entradas_log.append(
            f"[{i}] {acao}"
            f" | TOTAL={total:.2f}"
            f" | ERRO={erro:.2f}"
        )

    #
    # Determinar status
    #

    status = (
        "OTIMA"
        if erro == 0.0
        else "APROXIMADA"
    )

    #
    # Resultado final do agente
    #

    return Resultado(
        estado=estado,
        total=total,
        erro=erro,
        iteracoes=iteracoes,
        status=status,
        entradas_log=entradas_log,
        log=""
    )