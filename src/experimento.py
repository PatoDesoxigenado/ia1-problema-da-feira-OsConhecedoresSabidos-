#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira — Experimento

Este módulo executa o agente Alice repetidamente com diferentes
combinações de parâmetros e coleta métricas quantitativas.
"""

import csv
import math
from pathlib import Path

# Importando a função do agente e a leitura do ambiente criadas pelos meninos
from solucao import agente_alice
from main import carregar_itens

def calcular_desvio_padrao(valores, media):
    if len(valores) <= 1:
        return 0.0
    variancia = sum((x - media) ** 2 for x in valores) / (len(valores) - 1)
    return math.sqrt(variancia)

def executar_experimentos():
    # Definição dos cenários de teste exigidos
    orcamentos = [20.00, 50.00, 100.00]
    limites_iteracoes = [1000, 5000, 10000]
    seeds = [42, 100, 2026, 7, 13]  # Variadas sementes para análise estatística
    
    # Caminhos baseados na estrutura do projeto (executando de dentro da pasta src/)
    csv_path = "data/feira.csv"
    output_path = "data/resultados_experimento.csv"
    
    # Cabeçalho do arquivo CSV conforme especificado
    cabecalho = [
        "orcamento", "limite_iteracoes", "taxa_sucesso", 
        "erro_medio", "desvio_padrao_erro", "media_iteracoes"
    ]
    
    linhas_resultados = []
    
    # Carrega o ambiente uma única vez para otimizar
    itens_ambiente = carregar_itens(csv_path)
    
    print("=" * 60)
    print("INICIANDO EXECUÇÃO EM MASSA DOS EXPERIMENTOS")
    print("=" * 60)
    print(f"{'Orçamento':<10} | {'Limite':<8} | {'Sucesso':<8} | {'Erro Méd.':<10} | {'Média Iter.'}")
    print("-" * 60)

    # Loops aninhados para gerar todas as combinações
    for orcamento in orcamentos:
        for limite in limites_iteracoes:
            
            erros_rodada = []
            iteracoes_rodada = []
            sucessos = 0
            
            # Executa o agente para cada seed neste cenário
            for seed in seeds:
                ambiente = {
                    "itens": itens_ambiente,
                    "orcamento": orcamento
                }
                
                # Chamando o motor implementado pelo Alerrandro e Luiz
                resultado = agente_alice(
                    ambiente=ambiente,
                    max_iter=limite,
                    seed=seed
                )
                
                # Coletando os atributos do objeto nomeado retornado (namedtuple)
                erro_absoluto = abs(resultado.erro)
                erros_rodada.append(erro_absoluto)
                iteracoes_rodada.append(resultado.iteracoes)
                
                if resultado.status == "OTIMA" or erro_absoluto == 0.0:
                    sucessos += 1
            
            # Cálculo das métricas agregadas da configuração atual
            total_seeds = len(seeds)
            taxa_sucesso = sucessos / total_seeds
            erro_medio = sum(erros_rodada) / total_seeds
            desvio_padrao_erro = calcular_desvio_padrao(erros_rodada, erro_medio)
            media_iteracoes = sum(iteracoes_rodada) / total_seeds
            
            # Print de acompanhamento no terminal
            print(f"R$ {orcamento:<7.2f} | {limite:<8} | {taxa_sucesso*100:<6.1f}% | {erro_medio:<9.2f} | {media_iteracoes:.1f}")
            
            # Guarda os dados formatados para a linha do CSV
            linhas_resultados.append([
                orcamento, 
                limite, 
                f"{taxa_sucesso:.4f}", 
                f"{erro_medio:.4f}", 
                f"{desvio_padrao_erro:.4f}", 
                f"{media_iteracoes:.2f}"
            ])
            
    # Cria o diretório data se não existir e salva o CSV
    Path("data").mkdir(parents=True, exist_ok=True)
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas_resultados)
        
    print("-" * 60)
    print(f"Resultados exportados para: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    executar_experimentos()