# Infra-Hardware-Paralelismo

## Infraestrutura de Hardware – Análise Experimental do Paralelismo em Arquiteturas Híbridas

## Descrição

Este repositório contém os artefatos produzidos para o trabalho da disciplina **Infraestrutura de Hardware** da **CESAR School**, desenvolvido na modalidade **Trilha B – Relatório Técnico Expandido**.

O estudo investiga o impacto do paralelismo no desempenho computacional de uma aplicação CPU-bound executada em um processador híbrido **Intel Core 7 150U** sob ambiente **WSL2**, utilizando metodologia experimental baseada em análise estatística, intervalos de confiança e testes de hipótese.

O objetivo principal foi avaliar se o aumento do número de threads produz ganhos estatisticamente significativos de desempenho e identificar possíveis limitações de escalabilidade associadas ao compartilhamento de recursos computacionais, como cache, memória e overhead de sincronização.

---

## Artigo

**Título:**

> Impacto do Paralelismo na Eficiência Computacional em Arquiteturas Híbridas: Um Estudo Experimental com Intel Core 7 150U sob WSL2

O relatório expandido final encontra-se na pasta:

```text
relatorio/
```

Arquivo principal:

```text
relatorio/RelatorioExpandido_InfraHardware_LuizEduardo.pdf
```

---

## Ambiente Experimental

### Hardware

* Processador: Intel Core 7 150U
* Núcleos físicos: 6
* Threads lógicas: 12
* Cache L3: 12 MB
* Memória RAM: aproximadamente 8 GB
* Armazenamento: SSD NVMe

### Software

* Ubuntu 22.04.5 LTS
* Kernel Linux 6.6.87.2-microsoft-standard-WSL2
* Python 3
* NumPy
* ProcessPoolExecutor

---

## Estrutura do Repositório

```text
Infra-Hardware-Paralelismo/
│
├── README.md
│
├── relatorio/
│   ├── RelatorioExpandido_InfraHardware_LuizEduardo.pdf
│   ├── Tempo_Threads.png
│   ├── Figura2_Speedup.png
│   └── tempo_execucao_por_threads.html
│
├── dados/
│   ├── Tabela_Teste_Estatistico.xlsx
│   ├── paralelismo_dados_brutos.csv
│   ├── output_cpu.txt
│   ├── topologia-cpu.png
│   ├── paralelo.txt
│   ├── teste_localidade.txt
│   ├── leitura_sequencial.txt
│   ├── leitura_aleatoria.txt
│   ├── mbw_16.txt
│   ├── mbw_128.txt
│   ├── mbw_1024.txt
│   ├── saida_meminfo.txt
│   ├── stress_vmstat.txt
│   ├── lspci.txt
│   ├── interrupts_antes.txt
│   ├── interrupts_depois.txt
│   └── interrupts_diff.txt
│
└── scripts/
    ├── teste_paralelismo.py
    ├── teste_paralelismo_repeticoes.py
    ├── teste_localidade.py
    └── workload_completo.py
```

---

## Experimento Principal: Paralelismo

O experimento principal do trabalho utiliza um benchmark em Python baseado em multiplicação de matrizes 800 × 800, caracterizando uma carga predominantemente CPU-bound.

Foram avaliadas as seguintes configurações:

* 1 thread
* 2 threads
* 3 threads
* 4 threads
* 6 threads
* 8 threads
* 12 threads

Cada configuração foi executada:

* 33 vezes no total;
* 3 execuções descartadas como warm-up;
* 30 execuções válidas utilizadas para análise estatística.

O arquivo com os dados brutos do experimento principal está em:

```text
dados/paralelismo_dados_brutos.csv
```

---

## Metodologia Estatística

Foram calculadas as seguintes métricas:

* Média;
* Desvio-padrão;
* Intervalo de confiança de 95%;
* Speedup;
* Eficiência paralela;
* Teste t de Student bilateral.

Hipóteses avaliadas:

### H0

Não existe diferença estatisticamente significativa entre o desempenho obtido com uma thread e múltiplas threads.

### H1

Existe diferença estatisticamente significativa entre o desempenho obtido com uma thread e múltiplas threads.

Nível de significância adotado:

```text
α = 0,05
```

A tabela estatística consolidada está disponível em:

```text
dados/Tabela_Teste_Estatistico.xlsx
```

---

## Principais Resultados

| Threads | Tempo Médio (s) | Speedup |
| ------: | --------------: | ------: |
|       1 |           0,595 |   1,00× |
|       2 |           0,397 |   1,50× |
|       3 |           0,373 |   1,60× |
|       4 |           0,352 |   1,69× |
|       6 |           0,362 |   1,64× |
|       8 |           0,365 |   1,63× |
|      12 |           0,411 |   1,45× |

### Principais Achados

* O melhor desempenho foi observado com 4 threads.
* O speedup máximo obtido foi de 1,69×.
* Houve redução aproximada de 40,8% no tempo médio de execução em relação à execução sequencial.
* Todas as comparações apresentaram diferenças estatisticamente significativas, com p < 0,001.
* O aumento do paralelismo acima de 4 threads resultou em retornos decrescentes.
* Os resultados sugerem influência da contenção de cache, do subsistema de memória e do overhead de sincronização sobre a escalabilidade observada.

---

## Figuras

As figuras utilizadas no relatório estão disponíveis na pasta `relatorio/`.

### Figura 1 – Tempo médio de execução por número de threads

```text
relatorio/Tempo_Threads.png
```

### Figura 2 – Speedup observado versus speedup ideal

```text
relatorio/Figura2_Speedup.png
```

---

## Outros Dados Experimentais

Além do experimento principal de paralelismo, este repositório também contém medições realizadas nas atividades práticas da disciplina, incluindo:

* Identificação da CPU;
* Topologia da CPU;
* Testes de largura de banda de memória com `mbw`;
* Testes de localidade espacial;
* Informações de memória;
* Testes com `stress-ng`;
* Inspeção de barramentos com `lspci`;
* Medições de interrupções antes e depois de carga de I/O.

Esses dados estão armazenados na pasta:

```text
dados/
```

---

## Scripts Disponíveis

| Script                            | Descrição                                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------------------- |
| `teste_paralelismo.py`            | Executa o teste inicial de paralelismo variando o número de threads/processos.            |
| `teste_paralelismo_repeticoes.py` | Executa o experimento principal com repetições, warm-up e geração de dados brutos em CSV. |
| `teste_localidade.py`             | Avalia o impacto da localidade espacial no acesso à memória.                              |
| `workload_completo.py`            | Executa uma carga sintética com fases CPU-bound, memory-bound e I/O-bound.                |

---

## Como Executar os Experimentos

### Instalação das Dependências

```bash
pip install numpy psutil
```

### Executar o experimento principal de paralelismo

```bash
python3 scripts/teste_paralelismo_repeticoes.py
```

### Executar o teste simples de paralelismo

```bash
python3 scripts/teste_paralelismo.py
```

### Executar o teste de localidade de memória

```bash
python3 scripts/teste_localidade.py
```

### Executar o workload completo

```bash
python3 scripts/workload_completo.py
```

---

## Reprodutibilidade

Este repositório disponibiliza os principais artefatos necessários para reprodução e auditoria dos experimentos:

* Código-fonte dos benchmarks;
* Dados brutos coletados;
* Tabela estatística consolidada;
* Gráficos utilizados no relatório;
* Relatório expandido final;
* Informações do ambiente experimental.

A presença dos dados brutos permite verificar os resultados estatísticos apresentados no relatório, incluindo médias, desvios-padrão, intervalos de confiança e comparações entre configurações de paralelismo.

---

## Disciplina

**Infraestrutura de Hardware**

CESAR School

2026

---

## Autor

Luiz Eduardo Mariz

Curso de Ciência da Computação

CESAR School
