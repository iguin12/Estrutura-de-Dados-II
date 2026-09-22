"""
Atividade Prática - Análise de Algoritmos de Ordenação
Central de Distribuição de Pedidos

Compara Bubble Sort, Insertion Sort, Selection Sort e Quick Sort
contando o número de comparações e de trocas/movimentações realizadas
por cada algoritmo, para vetores de tamanhos 10, 20 e 1.000 elementos.

Critério de contagem adotado (deixado explícito para o relatório):
- Comparação: toda vez que dois elementos do vetor são comparados entre si
  (ex.: arr[j] > arr[j+1]) para decidir a ordenação.
- Troca/movimentação: toda vez que um valor é efetivamente escrito em uma
  posição do vetor por causa da ordenação.
    * Bubble Sort  -> cada swap (troca de posição de dois elementos) conta
      como 1 troca.
    * Selection Sort -> mesmo critério: 1 troca por swap realizado ao final
      de cada passagem (mesmo quando min_idx == i, o swap é "trivial" e não
      é contado, pois nenhuma movimentação de fato ocorre).
    * Insertion Sort -> cada deslocamento de um elemento uma posição à
      direita (arr[j+1] = arr[j]) conta como 1 movimentação, mais a
      inserção final do elemento-chave na posição correta.
    * Quick Sort -> cada troca feita dentro do particionamento (Lomuto)
      conta como 1 movimentação (inclui a troca do pivô para sua posição
      final).
"""

import random
import copy
import csv
import sys


# ---------------------------------------------------------------------
# Algoritmos instrumentados: cada função retorna (comparacoes, trocas)
# e ordena o vetor "in place".
# ---------------------------------------------------------------------

def bubble_sort(arr):
    comparacoes = 0
    trocas = 0
    n = len(arr)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            comparacoes += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                trocas += 1
                trocou = True
        if not trocou:
            break
    return comparacoes, trocas


def insertion_sort(arr):
    comparacoes = 0
    movimentacoes = 0
    n = len(arr)
    for i in range(1, n):
        chave = arr[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if arr[j] > chave:
                arr[j + 1] = arr[j]
                movimentacoes += 1
                j -= 1
            else:
                break
        arr[j + 1] = chave
        movimentacoes += 1
    return comparacoes, movimentacoes


def selection_sort(arr):
    comparacoes = 0
    trocas = 0
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparacoes += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            trocas += 1
    return comparacoes, trocas


def quick_sort(arr):
    comparacoes = [0]
    movimentacoes = [0]

    def particionar(baixo, alto):
        pivo = arr[alto]
        i = baixo - 1
        for j in range(baixo, alto):
            comparacoes[0] += 1
            if arr[j] <= pivo:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                movimentacoes[0] += 1
        arr[i + 1], arr[alto] = arr[alto], arr[i + 1]
        movimentacoes[0] += 1
        return i + 1

    def ordenar(baixo, alto):
        if baixo < alto:
            p = particionar(baixo, alto)
            ordenar(baixo, p - 1)
            ordenar(p + 1, alto)

    sys.setrecursionlimit(10000)
    ordenar(0, len(arr) - 1)
    return comparacoes[0], movimentacoes[0]


# ---------------------------------------------------------------------
# Etapa 1, 2 e 3: experimento principal com vetores aleatórios
# ---------------------------------------------------------------------

def gerar_vetor(n, semente=None):
    if semente is not None:
        random.seed(semente)
    return [random.randint(1, 100000) for _ in range(n)]


def rodar_experimento(tamanhos, semente_base=42):
    resultados = []
    for idx, n in enumerate(tamanhos):
        original = gerar_vetor(n, semente=semente_base + idx)

        vetor_bubble = original.copy()
        vetor_insertion = original.copy()
        vetor_selection = original.copy()
        vetor_quick = original.copy()

        comp_b, tr_b = bubble_sort(vetor_bubble)
        comp_i, mov_i = insertion_sort(vetor_insertion)
        comp_s, tr_s = selection_sort(vetor_selection)
        comp_q, mov_q = quick_sort(vetor_quick)

        # garante que todos ordenaram corretamente
        gabarito = sorted(original)
        assert vetor_bubble == gabarito
        assert vetor_insertion == gabarito
        assert vetor_selection == gabarito
        assert vetor_quick == gabarito

        resultados.append({
            "tamanho": n,
            "bubble_comp": comp_b, "bubble_trocas": tr_b,
            "insertion_comp": comp_i, "insertion_mov": mov_i,
            "selection_comp": comp_s, "selection_trocas": tr_s,
            "quick_comp": comp_q, "quick_mov": mov_q,
        })
    return resultados


def imprimir_tabela(resultados):
    cabecalho = ["Tamanho", "Bubble Comp.", "Bubble Trocas",
                 "Insertion Comp.", "Insertion Mov.",
                 "Selection Comp.", "Selection Trocas",
                 "Quick Comp.", "Quick Mov."]
    linhas = [cabecalho]
    for r in resultados:
        linhas.append([
            r["tamanho"], r["bubble_comp"], r["bubble_trocas"],
            r["insertion_comp"], r["insertion_mov"],
            r["selection_comp"], r["selection_trocas"],
            r["quick_comp"], r["quick_mov"],
        ])
    larguras = [max(len(str(linha[c])) for linha in linhas) for c in range(len(cabecalho))]
    for linha in linhas:
        print(" | ".join(str(v).rjust(larguras[c]) for c, v in enumerate(linha)))


def salvar_csv(resultados, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        campos = ["tamanho", "bubble_comp", "bubble_trocas",
                  "insertion_comp", "insertion_mov",
                  "selection_comp", "selection_trocas",
                  "quick_comp", "quick_mov"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)


# ---------------------------------------------------------------------
# Desafio adicional: aleatório x já ordenado x ordem inversa
# ---------------------------------------------------------------------

def rodar_desafio(n=1000, semente=7):
    aleatorio = gerar_vetor(n, semente=semente)
    ja_ordenado = sorted(aleatorio)
    ordem_inversa = sorted(aleatorio, reverse=True)

    casos = {
        "Aleatório": aleatorio,
        "Já ordenado": ja_ordenado,
        "Ordem inversa": ordem_inversa,
    }

    resultados = []
    for nome_caso, base in casos.items():
        vetor_bubble = base.copy()
        vetor_insertion = base.copy()
        vetor_selection = base.copy()
        vetor_quick = base.copy()

        comp_b, tr_b = bubble_sort(vetor_bubble)
        comp_i, mov_i = insertion_sort(vetor_insertion)
        comp_s, tr_s = selection_sort(vetor_selection)
        comp_q, mov_q = quick_sort(vetor_quick)

        resultados.append({
            "caso": nome_caso, "tamanho": n,
            "bubble_comp": comp_b, "bubble_trocas": tr_b,
            "insertion_comp": comp_i, "insertion_mov": mov_i,
            "selection_comp": comp_s, "selection_trocas": tr_s,
            "quick_comp": comp_q, "quick_mov": mov_q,
        })
    return resultados


def imprimir_tabela_desafio(resultados):
    cabecalho = ["Caso", "Tamanho", "Bubble Comp.", "Bubble Trocas",
                 "Insertion Comp.", "Insertion Mov.",
                 "Selection Comp.", "Selection Trocas",
                 "Quick Comp.", "Quick Mov."]
    linhas = [cabecalho]
    for r in resultados:
        linhas.append([
            r["caso"], r["tamanho"], r["bubble_comp"], r["bubble_trocas"],
            r["insertion_comp"], r["insertion_mov"],
            r["selection_comp"], r["selection_trocas"],
            r["quick_comp"], r["quick_mov"],
        ])
    larguras = [max(len(str(linha[c])) for linha in linhas) for c in range(len(cabecalho))]
    for linha in linhas:
        print(" | ".join(str(v).rjust(larguras[c]) for c, v in enumerate(linha)))


if __name__ == "__main__":
    print("=== Etapa 3: Experimento principal (vetores aleatórios) ===\n")
    tamanhos = [10, 20, 1000]
    resultados = rodar_experimento(tamanhos)
    imprimir_tabela(resultados)
    salvar_csv(resultados, "resultados_experimento.csv")

    print("\n=== Desafio adicional: aleatório x ordenado x ordem inversa (n=1000) ===\n")
    resultados_desafio = rodar_desafio(n=1000)
    imprimir_tabela_desafio(resultados_desafio)
    with open("resultados_desafio.csv", "w", newline="", encoding="utf-8") as f:
        campos = ["caso", "tamanho", "bubble_comp", "bubble_trocas",
                  "insertion_comp", "insertion_mov",
                  "selection_comp", "selection_trocas",
                  "quick_comp", "quick_mov"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados_desafio)
