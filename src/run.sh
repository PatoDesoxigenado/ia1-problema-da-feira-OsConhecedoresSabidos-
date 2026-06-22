#!/bin/sh

#
# Problema da Feira
#
# Script de execução experimental e automação de métricas.
#

CSV="data/feira.csv"

echo "=================================================="
echo "Problema da Feira - Execuções Demonstrativas"
echo "=================================================="

echo
echo "[Exemplo 1]"
python3 main.py "$CSV" 20.00 500 2

echo
echo "[Exemplo 2]"
python3 main.py "$CSV" 25.00 10000 4

echo
echo "[Gerando logs para o Gráfico de Comparação de Seeds]"
echo "Mesmo orçamento (30.00), mesmas iterações, seeds distintas..."
python3 main.py "$CSV" 30.00 2000 42
python3 main.py "$CSV" 30.00 2000 100
python3 main.py "$CSV" 30.00 2000 2026

echo
echo "=================================================="
echo "Iniciando Automação de Experimentos em Massa"
echo "=================================================="
echo "Executando o script de métricas quantitativas..."

# Chama o script Python que faz os loops de todas as combinações
python3 experimento.py

echo
echo "=================================================="
echo "Gerando Gráficos Estatísticos"
echo "=================================================="

# Deixa engatado para rodar a parte da Thafine logo em seguida
python3 visualizacao.py

echo
echo "=================================================="
echo "Fim do pipeline de execução. Dados e gráficos salvos!"
echo "=================================================="