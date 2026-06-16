#!/usr/bin/env python3
"""
Teste de Paralelismo com Repetições — versão para coleta de dados do artigo
Baseado em teste_paralelismo.py (Aula 1, Infraestrutura de Hardware)

Diferenças em relação ao script original:
  - Roda N_REPETICOES vezes por configuração de threads (não apenas 1).
  - Descarta as primeiras N_WARMUP execuções de cada configuração (warm-up).
  - Randomiza a ORDEM das configurações em cada rodada, para reduzir o efeito
    de fatores externos que variam com o tempo (ex.: throttling térmico,
    outros processos do sistema).
  - Salva cada medição individual em um CSV, uma linha por execução.
    Isso permite calcular depois: média, desvio-padrão, IC 95% e teste de
    hipótese (t de Student / Wilcoxon) sem precisar coletar de novo.

Uso:
    python3 teste_paralelismo_repeticoes.py

Saída:
    paralelismo_dados_brutos.csv  (uma linha por execução individual)

Dependências: numpy, psutil
"""

import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("BLIS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")

import csv
import multiprocessing as mp
import random
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

import numpy as np
import psutil

# ----------------------------------------------------------------------
# PARÂMETROS DO EXPERIMENTO — ajuste aqui se precisar
# ----------------------------------------------------------------------
TAMANHO_MATRIZ = 800       # mesmo valor do script original, para comparabilidade
N_TAREFAS = 16              # tarefas a distribuir entre as threads
N_REPETICOES = 30           # repetições válidas por configuração (mínimo exigido: 30)
N_WARMUP = 3                # execuções de aquecimento descartadas por configuração
ARQUIVO_SAIDA = "paralelismo_dados_brutos.csv"
SEED = 42                   # semente fixa para reprodutibilidade da ordem dos testes


def carga_computacional(_):
    a = np.random.rand(TAMANHO_MATRIZ, TAMANHO_MATRIZ)
    b = np.random.rand(TAMANHO_MATRIZ, TAMANHO_MATRIZ)
    c = a @ b
    return c.sum()


def medir(n_threads: int) -> float:
    inicio = time.perf_counter()
    with ProcessPoolExecutor(max_workers=n_threads) as executor:
        list(executor.map(carga_computacional, range(N_TAREFAS)))
    return time.perf_counter() - inicio


def main():
    nucleos_fisicos = psutil.cpu_count(logical=False)
    threads_logicas = psutil.cpu_count(logical=True)

    # Configurações de threads a testar. Inclui mais pontos intermediários
    # que o script original (1,2,4,12) para conseguir ver a forma da curva
    # de speedup/eficiência, não só os extremos.
    configuracoes = sorted(set(
        c for c in [1, 2, 3, 4, 6, 8, nucleos_fisicos, threads_logicas]
        if 1 <= c <= threads_logicas
    ))

    print("=" * 70)
    print("TESTE DE PARALELISMO COM REPETIÇÕES")
    print("=" * 70)
    print(f"Núcleos físicos:     {nucleos_fisicos}")
    print(f"Threads lógicas:     {threads_logicas}")
    print(f"Configurações:       {configuracoes}")
    print(f"Repetições válidas:  {N_REPETICOES} por configuração")
    print(f"Warm-up descartado:  {N_WARMUP} por configuração")
    total_execucoes = len(configuracoes) * (N_REPETICOES + N_WARMUP)
    print(f"Total de execuções:  {total_execucoes} "
          f"(estimativa de tempo depende da carga da máquina)")
    print("=" * 70)

    # Monta a lista de execuções (config, repeticao, é_warmup) e embaralha
    # a ORDEM GERAL para que efeitos de tempo (aquecimento da CPU, outros
    # processos) não fiquem concentrados em uma única configuração.
    rng = random.Random(SEED)
    plano = []
    for config in configuracoes:
        for i in range(N_WARMUP):
            plano.append((config, -1 - i, True))   # warm-up marcado com índice negativo
        for i in range(N_REPETICOES):
            plano.append((config, i, False))
    rng.shuffle(plano)

    linhas = []
    timestamp_inicio = datetime.now().isoformat(timespec="seconds")

    for idx, (n_threads, rep_idx, eh_warmup) in enumerate(plano, start=1):
        tempo = medir(n_threads)
        status = "warmup" if eh_warmup else "valida"
        print(f"[{idx:4d}/{len(plano)}] threads={n_threads:<3d} "
              f"rep={rep_idx:<3d} ({status:7s}) tempo={tempo:.4f}s")
        linhas.append({
            "timestamp_inicio_execucao": datetime.now().isoformat(timespec="seconds"),
            "n_threads": n_threads,
            "repeticao": rep_idx,
            "tipo": status,
            "tempo_s": f"{tempo:.6f}",
            "tamanho_matriz": TAMANHO_MATRIZ,
            "n_tarefas": N_TAREFAS,
            "nucleos_fisicos": nucleos_fisicos,
            "threads_logicas": threads_logicas,
        })

    with open(ARQUIVO_SAIDA, "w", newline="", encoding="utf-8") as f:
        campos = list(linhas[0].keys())
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(linhas)

    print("\n" + "=" * 70)
    print(f"Coleta iniciada em:  {timestamp_inicio}")
    print(f"Coleta finalizada em: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Dados salvos em:     {ARQUIVO_SAIDA}")
    print(f"Linhas no CSV:       {len(linhas)} "
          f"({N_WARMUP} warm-up + {N_REPETICOES} válidas por config)")
    print("Próximo passo: análise estatística (média, desvio-padrão, IC 95%,")
    print("teste de hipótese) usando apenas as linhas tipo='valida'.")
    print("=" * 70)


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
