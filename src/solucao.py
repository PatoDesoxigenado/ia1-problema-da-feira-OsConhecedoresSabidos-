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

        # 1. Sorteia uma ação/operador aleatório
        operador = random.choice(["adicionar", "remover", "substituir"])
        item_sorteado = random.choice(lista_itens)
        
        # 2. Gera o estado candidato baseado no operador escolhido
        if operador == "adicionar":
            candidato = adicionar_item(estado, item_sorteado)
            descricao_acao = f"adicionar {item_sorteado}"
        elif operador == "remover":
            candidato = remover_item(estado, item_sorteado)
            descricao_acao = f"remover {item_sorteado}"
        else: # substituir
            item_saida = random.choice(lista_itens)
            candidato = substituir_item(estado, item_saida, item_sorteado)
            descricao_acao = f"substituir {item_saida} por {item_sorteado}"

        # 3. Avalia o candidato
        total_candidato = calcular_total(candidato, itens)
        erro_candidato = calcular_heuristica(total_candidato, orcamento)

        # 4. Política de aceitação (só aceita se melhorar ou mantiver o erro se for válido)
        if erro_candidato < erro:
            estado = candidato
            total = total_candidato
            erro = erro_candidato
            
            # Registrar a trajetória no log para auditoria de XAI exigida pelo professor
            entradas_log.append(
                f"[{i}] {descricao_acao}"
                f" | TOTAL={total:.2f}"
                f" | ERRO={erro:.2f}"
            )

    # Determinar status final
    status = "OTIMA" if erro == 0.0 else "APROXIMADA"

    return Resultado(
        estado=estado,
        total=total,
        erro=erro,
        iteracoes=iteracoes,
        status=status,
        entradas_log=entradas_log,
        log=""
    )