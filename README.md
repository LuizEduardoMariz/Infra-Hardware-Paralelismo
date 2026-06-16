# Infra-Hardware-Paralelismo
# Infraestrutura de Hardware – Análise Experimental do Paralelismo em Arquiteturas Híbridas

## Descrição

Este repositório contém os artefatos produzidos para o trabalho da disciplina **Infraestrutura de Hardware** da **CESAR School**, desenvolvido na modalidade **Trilha B – Relatório Técnico Expandido**.

O estudo investiga o impacto do paralelismo no desempenho computacional de uma aplicação CPU-bound executada em um processador híbrido **Intel Core 7 150U** sob ambiente **WSL2**, utilizando metodologia experimental baseada em análise estatística, intervalos de confiança e testes de hipótese.

O objetivo principal foi avaliar se o aumento do número de threads produz ganhos estatisticamente significativos de desempenho e identificar possíveis limitações de escalabilidade associadas ao compartilhamento de recursos computacionais.

---

## Artigo

**Título:**

> Impacto do Paralelismo na Eficiência Computacional em Arquiteturas Híbridas: Um Estudo Experimental com Intel Core 7 150U sob WSL2

O artigo completo encontra-se na pasta:

```text
relatorio/
```

---

## Ambiente Experimental

### Hardware

* Processador: Intel Core 7 150U
* Núcleos físicos: 6
* Threads lógicas: 12
* Cache L3: 12 MB
* Memória RAM: 8 GB
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
infra-hardware-paralelismo/
│
├── README.md
│
├── relatorio/
│   ├── Artigo_Infraestrutura_Hardware.pdf
│   ├── Artigo_Infraestrutura_Hardware.docx
│   ├── figura1_tempo_threads.png
│   └── figura2_speedup.png
│
├── dados/
│   ├── info_cpu.txt
│   ├── paralelismo_dados_brutos.csv
│   ├── resultados_paralelismo.txt
│   └── estatisticas_paralelismo.csv
│
├── scripts/
│   ├── teste_paralelismo_repeticoes.py
│   ├── analise_estatistica.py
│   └── gerar_graficos.py
│
└── .gitignore
```

---

## Experimento de Paralelismo

O benchmark foi desenvolvido em Python utilizando multiplicação de matrizes 800 × 800 como carga computacional CPU-bound.

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

---

## Metodologia Estatística

Foram calculadas as seguintes métricas:

* Média
* Desvio-padrão
* Intervalo de Confiança de 95%
* Speedup
* Eficiência Paralela
* Teste t de Student bilateral

Hipóteses avaliadas:

### H0

Não existe diferença estatisticamente significativa entre o desempenho obtido com uma thread e múltiplas threads.

### H1

Existe diferença estatisticamente significativa entre o desempenho obtido com uma thread e múltiplas threads.

Nível de significância adotado:

```text
α = 0,05
```

---

## Principais Resultados

| Threads | Tempo Médio (s) | Speedup |
| ------- | --------------- | ------- |
| 1       | 0,595           | 1,00×   |
| 2       | 0,397           | 1,50×   |
| 3       | 0,373           | 1,60×   |
| 4       | 0,352           | 1,69×   |
| 6       | 0,362           | 1,64×   |
| 8       | 0,365           | 1,63×   |
| 12      | 0,411           | 1,45×   |

### Principais Achados

* Melhor desempenho observado com 4 threads.
* Speedup máximo de 1,69×.
* Redução aproximada de 40,8% no tempo médio de execução em relação à execução sequencial.
* Todas as comparações apresentaram diferenças estatisticamente significativas (p < 0,001).
* O aumento do paralelismo acima de quatro threads resultou em retornos decrescentes.
* Os resultados indicam influência da contenção de cache, do subsistema de memória e do overhead de sincronização sobre a escalabilidade observada.

---

## Como Executar os Experimentos

### Instalação das Dependências

```bash
pip install numpy
```

### Execução do Benchmark

```bash
python3 scripts/teste_paralelismo_repeticoes.py
```

### Análise Estatística

```bash
python3 scripts/analise_estatistica.py
```

### Geração dos Gráficos

```bash
python3 scripts/gerar_graficos.py
```

---

## Reprodutibilidade

Este repositório disponibiliza:

* Código-fonte completo dos experimentos;
* Dados brutos coletados durante os testes;
* Scripts de análise estatística;
* Gráficos utilizados no artigo;
* Documento final submetido para avaliação;
* Informações detalhadas do ambiente experimental.

Todos os experimentos podem ser reproduzidos utilizando os scripts disponibilizados neste repositório.

---

## Disciplina

Infraestrutura de Hardware

CESAR School

2026

---

## Autor

Luiz Eduardo Mariz

Curso de Ciência da Computação

CESAR School
