#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Problema da Feira — Visualização

Este módulo gera gráficos a partir de:

- arquivos de log individuais gerados pelo agente;
- arquivo CSV gerado pelo experimento.py.

"""

import re
import csv
import math
from pathlib import Path
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")   # backend sem janela (funciona em qualquer ambiente)
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ============================================================
# Caminhos do projeto  (relativos a src/, onde o script roda)
# ============================================================

LOG_DIR      = Path("logs")
CSV_PATH     = Path("data") / "resultados_experimento.csv"
GRAFICOS_DIR = Path("data") / "graficos"


# ============================================================
# Estilo visual compartilhado
# ============================================================

PALETA = [
    "#2196F3",  # azul
    "#E91E63",  # rosa
    "#4CAF50",  # verde
    "#FF9800",  # laranja
    "#9C27B0",  # roxo
    "#00BCD4",  # ciano
    "#F44336",  # vermelho
    "#8BC34A",  # verde-claro
]

def _aplicar_estilo():
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor":   "#F8F9FA",
        "axes.grid":        True,
        "grid.linestyle":   "--",
        "grid.alpha":       0.5,
        "font.size":        11,
        "axes.titlesize":   13,
        "axes.titleweight": "bold",
        "axes.labelsize":   11,
        "legend.fontsize":  9,
        "legend.framealpha": 0.85,
    })


# ============================================================
# Leitura de logs
# ============================================================

# Padrão: "  [72] adicionar Banana | TOTAL=30.00 | ERRO=0.00"
_RE_LINHA = re.compile(r"\[(\d+)\].*TOTAL=([\d.]+).*ERRO=([-\d.]+)")
# Padrão do nome do arquivo para extrair orçamento e seed
_RE_NOME  = re.compile(r"orc([\d_]+)__seed(\w+)__")


def _parse_orc(orc_str: str) -> float:
    return float(orc_str.replace("_", "."))


def ler_log(caminho: Path):
    m = _RE_NOME.search(caminho.name)
    orcamento = _parse_orc(m.group(1)) if m else 0.0
    seed      = m.group(2)            if m else "?"

    iteracoes, erros = [], []
    try:
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                mo = _RE_LINHA.search(linha)
                if mo:
                    iteracoes.append(int(mo.group(1)))
                    erros.append(float(mo.group(3)))
    except OSError as exc:
        print(f"  [aviso] Não foi possível ler {caminho.name}: {exc}")
        return None

    if not iteracoes:
        return None

    return {
        "iteracoes": iteracoes,
        "erros":     erros,
        "orcamento": orcamento,
        "seed":      seed,
        "nome":      caminho.stem,
    }


def carregar_logs():
    logs = []
    for caminho in sorted(LOG_DIR.glob("*.txt")):
        dados = ler_log(caminho)
        if dados:
            logs.append(dados)
    return logs


# ============================================================
# Leitura do CSV do experimento
# ============================================================

def carregar_csv():
    """
    Lê data/resultados_experimento.csv e retorna lista de dicts.
    """
    if not CSV_PATH.exists():
        return []

    campos_esperados = {
        "orcamento", "limite_iteracoes", "taxa_sucesso",
        "erro_medio", "desvio_padrao_erro", "media_iteracoes",
    }

    linhas = []
    try:
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None or not campos_esperados.issubset(reader.fieldnames):
                faltando = campos_esperados - set(reader.fieldnames or [])
                print(f"  [aviso] CSV ignorado — campos ausentes: {faltando}")
                return []

            for i, row in enumerate(reader, start=2):
                try:
                    linhas.append({
                        "orcamento":          float(row["orcamento"]),
                        "limite_iteracoes":   int(row["limite_iteracoes"]),
                        "taxa_sucesso":       float(row["taxa_sucesso"]),
                        "erro_medio":         float(row["erro_medio"]),
                        "desvio_padrao_erro": float(row["desvio_padrao_erro"]),
                        "media_iteracoes":    float(row["media_iteracoes"]),
                    })
                except (KeyError, ValueError) as exc:
                    # [CORRIGIDO] Informa a linha problemática e continua
                    print(f"  [aviso] CSV linha {i} ignorada — {exc}")

    except OSError as exc:
        print(f"  [aviso] Não foi possível ler o CSV: {exc}")

    return linhas


# ============================================================
# Gráfico 1 — Curva de convergência de h(s)  (uma execução)
# ============================================================

def grafico_convergencia(logs, saida: Path):
    candidatos = [lg for lg in logs if lg["orcamento"] == 30.0]
    dados = candidatos[-1] if candidatos else logs[-1]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(
        dados["iteracoes"],
        dados["erros"],
        color=PALETA[0],
        linewidth=2,
        marker="o",
        markersize=5,
        label=f"seed = {dados['seed']}",
        zorder=3,
    )

    # Destaca o ponto final (solução encontrada)
    ax.scatter(
        dados["iteracoes"][-1],
        dados["erros"][-1],
        color="#F44336",
        s=80,
        zorder=4,
        label=f"Solução  h(s) = {dados['erros'][-1]:.2f}",
    )

    # [CORRIGIDO] Título identifica explicitamente o orçamento e a seed da execução
    ax.set_title(
        f"Convergência de h(s) ao longo das iterações\n"
        f"(orçamento = R$ {dados['orcamento']:.2f} — seed = {dados['seed']})"
    )
    ax.set_xlabel("Número da iteração (apenas ações aceitas)")
    ax.set_ylabel("h(s) = |Orçamento − Total|  (R$)")
    ax.legend()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    fig.tight_layout()
    fig.savefig(saida, dpi=150)
    plt.close(fig)
    print(f"  [ok] {saida.name}  (seed={dados['seed']}, orç=R${dados['orcamento']:.2f})")


# ============================================================
# Gráfico 2 — Comparação de curvas entre seeds distintas
# ============================================================

def grafico_comparacao_seeds(logs, saida: Path):
    orcamento_ref = 30.0
    candidatos = [lg for lg in logs if lg["orcamento"] == orcamento_ref]

    if not candidatos:
        # Fallback: usa todos os logs disponíveis com o orçamento mais comum
        from collections import Counter
        orc_mais_comum = Counter(lg["orcamento"] for lg in logs).most_common(1)[0][0]
        candidatos = [lg for lg in logs if lg["orcamento"] == orc_mais_comum]
        orcamento_ref = orc_mais_comum
        print(
            f"  [aviso] Nenhum log com orç=R$30,00. "
            f"Usando orç=R${orcamento_ref:.2f} como referência."
        )

    # Mantém apenas o log mais recente de cada seed
    por_seed: dict = {}
    for lg in sorted(candidatos, key=lambda x: x["nome"]):
        por_seed[lg["seed"]] = lg
    selecionados = list(por_seed.values())

    # Limita a 8 curvas para não poluir o gráfico
    selecionados = selecionados[:8]

    fig, ax = plt.subplots(figsize=(9, 5))

    for i, dados in enumerate(selecionados):
        cor = PALETA[i % len(PALETA)]
        ax.plot(
            dados["iteracoes"],
            dados["erros"],
            color=cor,
            linewidth=1.5,
            marker="o",
            markersize=3,
            alpha=0.85,
            label=f"seed = {dados['seed']}",
        )

    n_seeds = len(selecionados)
    ax.set_title(
        f"Comparação de convergência — R$ {orcamento_ref:.2f} — "
        f"{n_seeds} seed{'s' if n_seeds != 1 else ''} distinta{'s' if n_seeds != 1 else ''}"
    )
    ax.set_xlabel("Número da iteração (apenas ações aceitas)")
    ax.set_ylabel("h(s) = |Orçamento − Total|  (R$)")
    ax.legend(loc="upper right", ncol=2)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    fig.tight_layout()
    fig.savefig(saida, dpi=150)
    plt.close(fig)
    print(f"  [ok] {saida.name}  ({n_seeds} seed(s) comparada(s))")


# ============================================================
# Gráfico 3 — Histograma do erro final
# ============================================================

def grafico_histograma_erro(logs, saida: Path):
    por_orc: dict = defaultdict(list)
    for lg in logs:
        por_orc[lg["orcamento"]].append(lg["erros"][-1])

    orcamentos = sorted(por_orc.keys())
    n_paineis  = len(orcamentos)

    fig, axes = plt.subplots(
        1, n_paineis,
        figsize=(6 * n_paineis, 5),
        sharey=False,
        squeeze=False,
    )

    for col, orc in enumerate(orcamentos):
        ax = axes[0][col]
        erros_finais = por_orc[orc]

        zeros     = [e for e in erros_finais if e == 0.0]
        nao_zeros = [e for e in erros_finais if e > 0.0]

        max_erro = max(erros_finais) if erros_finais else 0.0

        if max_erro == 0.0:
            ax.bar(
                0, len(zeros),
                width=0.3,
                color=PALETA[1],
                edgecolor="white",
                linewidth=0.8,
                label=f"Erro = 0 (ótima)  — {len(zeros)} exec.",
                zorder=3,
            )
            ax.set_xlim(-0.5, 0.5)
            ax.set_xticks([0])
            ax.set_xticklabels(["0.00"])
        else:
            bins = [i * max_erro / 15 for i in range(16)]

            if zeros:
                barra_w = max_erro / 15 * 0.8
                ax.bar(
                    0, len(zeros),
                    width=barra_w,
                    color=PALETA[1],
                    edgecolor="white",
                    linewidth=0.8,
                    label=f"Erro = 0 (ótima)  — {len(zeros)} exec.",
                    zorder=3,
                )
            if nao_zeros:
                ax.hist(
                    nao_zeros,
                    bins=bins[1:],
                    color=PALETA[0],
                    edgecolor="white",
                    linewidth=0.8,
                    alpha=0.85,
                    label=f"Erro > 0 (aprox.)  — {len(nao_zeros)} exec.",
                    zorder=2,
                )

        taxa = len(zeros) / len(erros_finais) * 100 if erros_finais else 0
        ax.set_title(
            f"R$ {orc:.2f}  —  {taxa:.0f}% ótimas\n"
            f"({len(erros_finais)} execuções)"
        )
        ax.set_xlabel("Erro final h(s)  (R$)")
        ax.set_ylabel("Nº de execuções")
        ax.legend(fontsize=8)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    fig.suptitle("Distribuição do erro final h(s) por orçamento", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(saida, dpi=150)
    plt.close(fig)

    resumo = ", ".join(
        f"R${orc:.2f}: {len(por_orc[orc])} exec." for orc in orcamentos
    )
    print(f"  [ok] {saida.name}  ({resumo})")


# ============================================================
# Gráfico 4 — Taxa de soluções ótimas por configuração
# ============================================================

def grafico_taxa_otimas(linhas_csv, saida: Path):
    if not linhas_csv:
        print(f"  [aviso] {saida.name} ignorado — CSV não encontrado.")
        return

    # Agrupa por orçamento para criar grupos de barras
    grupos = defaultdict(list)
    for linha in linhas_csv:
        grupos[linha["orcamento"]].append(linha)

    orcamentos     = sorted(grupos.keys())
    limites_unicos = sorted({ln["limite_iteracoes"] for ln in linhas_csv})
    n_limites      = len(limites_unicos)

    largura  = 0.7 / n_limites          # largura de cada barra
    fig, ax  = plt.subplots(figsize=(10, 5))

    for j, limite in enumerate(limites_unicos):
        posicoes = []
        taxas    = []
        for i, orc in enumerate(orcamentos):
            for ln in grupos[orc]:
                if ln["limite_iteracoes"] == limite:
                    posicoes.append(i + j * largura - (n_limites - 1) * largura / 2)
                    taxas.append(ln["taxa_sucesso"] * 100)

        barras = ax.bar(
            posicoes,
            taxas,
            width=largura * 0.9,
            color=PALETA[j % len(PALETA)],
            edgecolor="white",
            linewidth=0.8,
            label=f"max_iter = {limite:,}",
            zorder=3,
        )

        # Anotação do valor percentual no topo de cada barra
        for barra, taxa in zip(barras, taxas):
            ax.text(
                barra.get_x() + barra.get_width() / 2,
                barra.get_height() + 0.8,
                f"{taxa:.0f}%",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
            )

    ax.set_xticks(range(len(orcamentos)))
    ax.set_xticklabels([f"R$ {o:.2f}" for o in orcamentos])
    ax.set_ylim(0, 115)
    ax.set_title("Taxa de soluções ótimas por orçamento e limite de iterações")
    ax.set_xlabel("Orçamento")
    ax.set_ylabel("Taxa de soluções ótimas (%)")
    ax.legend(loc="lower right")

    fig.tight_layout()
    fig.savefig(saida, dpi=150)
    plt.close(fig)
    print(f"  [ok] {saida.name}  ({len(orcamentos)} orçamentos × {n_limites} limites)")


# ============================================================
# Main
# ============================================================

def main():
    _aplicar_estilo()
    GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("PROBLEMA DA FEIRA — GERAÇÃO DE GRÁFICOS")
    print("=" * 60)

    # ----------------------------------------------------------
    # Carrega fontes de dados
    # ----------------------------------------------------------
    logs       = carregar_logs()
    linhas_csv = carregar_csv()

    if not logs:
        print(
            "\n[ERRO] Nenhum log encontrado em logs/.\n"
            "Execute antes:\n"
            "  python3 main.py data/feira.csv 30.00 10000 42\n"
            "  (ou ./run.sh para gerar vários logs de uma vez)\n"
        )
        return

    if not linhas_csv:
        print(
            "\n[AVISO] data/resultados_experimento.csv não encontrado.\n"
            "O gráfico 04 será ignorado. Execute:\n"
            "  python3 experimento.py\n"
        )

    print(f"\nLogs carregados   : {len(logs)}")
    print(f"Linhas no CSV     : {len(linhas_csv)}\n")

    # ----------------------------------------------------------
    # Geração dos 4 gráficos
    # ----------------------------------------------------------
    grafico_convergencia(
        logs,
        GRAFICOS_DIR / "01_convergencia.png"
    )
    grafico_comparacao_seeds(
        logs,
        GRAFICOS_DIR / "02_comparacao_seeds.png"
    )
    grafico_histograma_erro(
        logs,
        GRAFICOS_DIR / "03_histograma_erro.png"
    )
    grafico_taxa_otimas(
        linhas_csv,
        GRAFICOS_DIR / "04_taxa_otimas.png"
    )

    print(f"\nGráficos salvos em: {GRAFICOS_DIR.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()