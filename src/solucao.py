#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira

Este módulo implementa o agente Alice.

O agente:

- percebe o ambiente;
- conhece os itens disponíveis;
- conhece os preços;
- possui um objetivo;
- executa ações;
- busca minimizar erro heurístico.

Inicialmente o agente não possui
comportamento inteligente.

A inteligência emerge conforme
os operadores heurísticos e mecanismos
de busca são implementados.
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

    O ambiente contém:

    ambiente = {
        "itens": {
            item -> preco
        },
        "orcamento": valor
    }
    """

    #
    # Inicialização do gerador pseudoaleatório
    #

    if seed is not None:
        random.seed(seed)

    #
    # Percepção do ambiente
    #

    itens = ambiente["itens"]
    orcamento = ambiente["orcamento"]

    #
    # Estado inicial do agente
    #

    estado = {
        item: 0
        for item in itens.keys()
    }

    #
    # Variáveis da busca
    #

    total = 0.0
    erro = orcamento
    iteracoes = 0
    entradas_log = []

    #
    # O agente inicia sem conhecimento útil.
    #
    # O comportamento inteligente emerge
    # conforme os operadores heurísticos
    # são implementados.
    #
    # TODO:
    #
    # implementar:
    #
    # - operadores de ação
    # - geração de candidatos
    # - heurística
    # - melhoria iterativa
    #
    # Para registrar cada ação no log, adicione
    # entradas à lista entradas_log durante a busca.
    #
    # Exemplo:
    #
    #   entradas_log.append(
    #       f"[{i}] adicionar Melancia"
    #       f" | TOTAL={total:.2f}"
    #       f" | ERRO={erro:.2f}"
    #   )
    #

    for i in range(1, max_iter + 1):

        iteracoes = i

        #
        # Critério de parada
        #

        if erro == 0.0:
            break

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
