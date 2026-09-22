# Análise de Algoritmos de Ordenação — Central de Distribuição de Pedidos

## Critério de contagem adotado

- **Comparação**: toda vez que dois elementos do vetor são comparados entre si para decidir a ordenação.
- **Troca/movimentação**: toda vez que um valor é efetivamente escrito em uma posição do vetor por causa da ordenação.
  - **Bubble Sort**: cada troca (swap) de dois elementos adjacentes conta como 1.
  - **Selection Sort**: 1 troca por passagem, apenas quando o mínimo encontrado é diferente da posição atual (swap "trivial" não é contado).
  - **Insertion Sort**: cada deslocamento de um elemento uma posição à direita conta como 1 movimentação, mais a inserção final do elemento-chave.
  - **Quick Sort** (particionamento de Lomuto, pivô = último elemento): cada troca dentro do particionamento conta como 1 movimentação, incluindo a troca final do pivô para sua posição correta.

Código-fonte completo: `ordenacao.py`. Os vetores são gerados aleatoriamente (inteiros entre 1 e 100.000) e as **quatro cópias idênticas** são ordenadas pelos quatro algoritmos, conforme exigido no enunciado.

---

## Etapa 3 — Resultados (vetores aleatórios)

| Tamanho | Bubble Comp. | Bubble Trocas | Insertion Comp. | Insertion Mov. | Selection Comp. | Selection Trocas | Quick Comp. | Quick Mov. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 45 | 26 | 33 | 35 | 45 | 6 | 29 | 15 |
| 20 | 180 | 89 | 107 | 108 | 190 | 17 | 68 | 42 |
| 1.000 | 499.497 | 244.664 | 245.656 | 245.663 | 499.500 | 992 | 11.553 | 6.723 |

*(valores obtidos executando `python3 ordenacao.py`; como os vetores são gerados aleatoriamente, pequenas variações de execução para execução são esperadas, mas a tendência geral se mantém.)*

---

## Etapa 4 — Análise dos resultados

**a) Qual algoritmo realizou o menor número de comparações para 10 elementos?**
O Quick Sort, com 29 comparações — bem abaixo de Bubble e Selection (45 cada) e de Insertion (33).

**b) Qual algoritmo realizou menos trocas ou movimentações?**
O Selection Sort, com apenas 6 trocas. Isso é esperado: o Selection Sort faz no máximo n-1 trocas (uma por passagem), independentemente dos valores do vetor.

**c) O comportamento observado para 10 elementos permaneceu semelhante quando o tamanho aumentou para 20?**
Sim. A ordem relativa se manteve: Quick Sort continuou com o menor número de comparações (68) e Selection Sort com o menor número de trocas (17). As proporções cresceram de forma coerente com o que se esperava teoricamente para cada algoritmo.

**d) O que aconteceu com a quantidade de operações quando o vetor passou para 1.000 elementos?**
Bubble, Insertion e Selection Sort tiveram um crescimento muito acentuado nas comparações (todas próximas de 500.000, ou seja, próximas de n²/2), caracterizando o comportamento quadrático. Já o Quick Sort cresceu de forma muito mais discreta (11.553 comparações), evidenciando um comportamento próximo de n·log(n).

**e) Bubble, Insertion e Selection Sort apresentam complexidade O(n²) em situações típicas. Eles apresentaram exatamente a mesma quantidade de operações? Explique.**
Não. Embora os três sejam O(n²) assintoticamente, as constantes e o comportamento no caso médio diferem:
- O **Selection Sort** sempre faz exatamente n(n-1)/2 comparações (499.500 para n=1.000), pois sempre varre todo o restante do vetor em busca do mínimo, independentemente de como os dados estão organizados.
- O **Bubble Sort** com otimização de parada antecipada (flag "trocou") também fez praticamente todas as comparações possíveis (499.497) com dados aleatórios, porque é muito improvável que o vetor fique ordenado antes da última passagem.
- Já o **Insertion Sort** fez bem menos comparações (245.656, quase metade) — isso ocorre porque o laço interno do Insertion Sort para assim que encontra a posição correta do elemento, sem precisar varrer o restante do vetor, o que na prática (caso médio) reduz o número de comparações para próximo de n²/4.

Ou seja: mesma classe assintótica (O(n²)), mas constantes multiplicativas diferentes.

**f) Qual algoritmo apresentou maior crescimento no número de operações?**
Bubble Sort e Selection Sort apresentaram o maior crescimento relativo nas comparações (de dezenas para ~500 mil, um fator de ~10.000x ao multiplicar o tamanho por 100 — coerente com o crescimento quadrático teórico, (100)² = 10.000). O Quick Sort cresceu muito menos (fator de ~400x), compatível com o crescimento n·log(n).

**g) Como o comportamento experimental do Quick Sort se diferenciou dos demais algoritmos?**
Com dados aleatórios, o Quick Sort precisou de ordens de grandeza a menos de operações do que os demais para 1.000 elementos, confirmando na prática sua complexidade média O(n·log n). Ele "divide para conquistar", reduzindo drasticamente o número de comparações necessárias em vetores grandes, ao contrário dos algoritmos O(n²) que continuam comparando pares de elementos de forma repetitiva.

**h) Os resultados encontrados são coerentes com as complexidades teóricas estudadas?**
Sim. Para dados aleatórios (caso médio), Bubble, Insertion e Selection Sort se comportaram como O(n²) e o Quick Sort como O(n·log n), exatamente como previsto pela teoria. (O desafio adicional, abaixo, mostra também que o caso médio não é o único caso relevante — o Quick Sort implementado com pivô fixo pode degradar para O(n²) em situações específicas.)

**i) Qual algoritmo você escolheria para o sistema da central de distribuição, com milhares de pedidos?**
O **Quick Sort**, pois foi disparadamente o mais eficiente para o vetor de 1.000 elementos (11.553 comparações contra ~500.000 dos demais), e essa vantagem tende a aumentar ainda mais para vetores maiores. A única ressalva é que, como mostra o desafio adicional a seguir, a escolha ingênua do pivô (último elemento) faz o Quick Sort degradar para O(n²) justamente quando os pedidos já chegam ordenados ou em ordem inversa — cenário que pode ocorrer na prática. Por isso, na implementação real eu usaria uma estratégia de pivô mais robusta (por exemplo, mediana de três ou pivô aleatório) para manter o bom desempenho médio em qualquer ordem de entrada.

---

## Desafio adicional — Vetor aleatório × já ordenado × ordem inversa (n = 1.000)

| Caso | Bubble Comp. | Bubble Trocas | Insertion Comp. | Insertion Mov. | Selection Comp. | Selection Trocas | Quick Comp. | Quick Mov. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Aleatório | 499.499 | 248.830 | 249.821 | 249.829 | 499.500 | 990 | 10.495 | 5.727 |
| Já ordenado | 999 | 0 | 999 | 999 | 499.500 | 0 | 499.500 | 500.499 |
| Ordem inversa | 499.500 | 499.492 | 499.500 | 500.491 | 499.500 | 507 | 493.462 | 247.466 |

**A organização inicial dos dados interfere na quantidade de operações realizadas por todos os algoritmos da mesma maneira? Não.** Cada algoritmo reage de um jeito diferente à ordem inicial dos dados:

- **Selection Sort** é o único totalmente indiferente à ordem inicial em termos de comparações: sempre faz 499.500 comparações, porque sempre varre todo o restante do vetor procurando o mínimo. Só o número de trocas varia (0 no vetor já ordenado, até 990 no aleatório).
- **Bubble Sort** e **Insertion Sort** se comportam de forma muito parecida entre si: no vetor **já ordenado** o desempenho é ótimo (apenas 999 comparações, O(n), graças à parada antecipada do Bubble e ao laço interno do Insertion que nem entra), enquanto na **ordem inversa** é o pior caso possível, com praticamente n²/2 comparações e o número máximo de trocas/movimentações.
- **Quick Sort** (nesta implementação, com pivô = último elemento) se comporta de forma **oposta** a Bubble/Insertion: o pior caso é justamente o vetor **já ordenado** (499.500 comparações e 500.499 movimentações — o pivô sempre é o maior valor da partição, gerando divisões extremamente desbalanceadas), e a ordem inversa também é ruim (493.462 comparações) pelo mesmo motivo. É no vetor **aleatório** que o Quick Sort brilha, com apenas 10.495 comparações.

Ou seja, a ordem inicial dos dados afeta os quatro algoritmos, mas **não da mesma forma**: para Bubble e Insertion, "já ordenado" é o melhor caso; para o Quick Sort com essa escolha de pivô, "já ordenado" é justamente o pior caso. Isso reforça, na prática, por que implementações reais de Quick Sort evitam pivôs fixos (usam pivô aleatório ou mediana de três) — para não sofrer justamente nos cenários mais comuns do dia a dia, como listas parcial ou totalmente ordenadas.
