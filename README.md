# Resolução do Problema dos Jarros d’Água por Busca Cega em Python

> **Curso:** Análise e Desenvolvimento de Sistemas (ADS) — 3º Módulo  
> **Disciplina:** Inteligência Artificial  
> **Linguagem:** Python 3 (Bibliotecas Padrão)

---

##  Sobre o Projeto

Este repositório contém a implementação prática e o relatório técnico referentes ao trabalho acadêmico de **Inteligência Artificial**, focado no **Problema dos Jarros d’Água** (Water Jug Problem) resolvido por meio de **Algoritmos de Busca sem Informação (Busca Cega)**.

### Intuito da Atividade
O objetivo principal é aplicar conceitos fundamentais de IA simbólica e algoritmos de busca em grafos/árvores para resolver um problema clássico de tomada de decisão sequencial e restrições. A aplicação simula o comportamento de um agente autônomo capaz de encontrar a sequência exata de operações físicas para obter **2 litros de água** a partir de um estado inicial parametrizado pelo usuário.

---

## 🧩 Formalização do Problema

* **Jarros Disponíveis:**
  * Jarro $A$: capacidade de **4 Litros**.
  * Jarro $B$: capacidade de **3 Litros**.
* **Estado Inicial:** $(0, 0)$ por padrão (ou informado interativamente pelo usuário).
* **Teste de Objetivo:** $x = 2$ ou $y = 2$ (obter 2 litros em qualquer um dos jarros).
* **Espaço de Estados:** Conjunto finito de 20 tuplas $(x, y)$ onde $x \in \{0, 1, 2, 3, 4\}$ e $y \in \{0, 1, 2, 3\}$.
* **Ações Permitidas:**
  1. Encher o jarro de 4L.
  2. Encher o jarro de 3L.
  3. Esvaziar o jarro de 4L.
  4. Esvaziar o jarro de 3L.
  5. Transferir água do jarro de 4L para o de 3L.
  6. Transferir água do jarro de 3L para o de 4L.

---

## 🛠️ Algoritmos Implementados

O programa executa de forma independente três estratégias de busca cega a partir do mesmo estado inicial:

1. **Busca em Largura (BFS):** Explora o espaço de estados nível por nível utilizando uma fila FIFO (`deque`). Garante encontrar a **solução ótima** (menor número de ações).
2. **Busca em Profundidade (DFS):** Explora os ramos o mais fundo possível utilizando uma pilha LIFO/recursão. Controla estados visitados para evitar ciclos infinitos.
3. **Busca com Aprofundamento Iterativo (IDDFS):** Realiza buscas em profundidade limitadas crescentes ($limite = 0, 1, 2, \dots$). Une a eficiência de memória da DFS com a **otimalidade e completude** da BFS.

---

## 🌲 Visualização da Árvore de Busca

O programa gera no terminal a **árvore de busca explorada** a partir do estado inicial informado, destacando visualmente os estados e transições que compõem o caminho da solução encontrada:

```text
============================================================
 ÁRVORE DE BUSCA EXPLORADA COM DESTAQUE PARA O CAMINHO DA SOLUÇÃO 
============================================================
Estado: (0, 0) ⭐ [PARTE DO CAMINHO DA SOLUÇÃO]
 |-- Ação: Encher o jarro de 4L
    |-- Estado: (4, 0)
 |-- Ação: Encher o jarro de 3L
    |-- Estado: (0, 3) ⭐ [PARTE DO CAMINHO DA SOLUÇÃO]
        |-- Ação: Transferir de 3L para 4L
            |-- Estado: (3, 0) ⭐ [PARTE DO CAMINHO DA SOLUÇÃO]
...
