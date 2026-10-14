"""
Trabalho Acadêmico: Resolução do Problema dos Jarros d'Água por Busca Cega
Disciplina: Inteligência Artificial
Curso: Análise e Desenvolvimento de Sistemas (ADS)
"""

from collections import deque
import time

class WaterJugProblem:
    def __init__(self, capacity_4=4, capacity_3=3, target=2):
        self.cap_4 = capacity_4
        self.cap_3 = capacity_3
        self.target = target

    def is_goal(self, state):
        x, y = state
        return x == self.target or y == self.target

    def get_successors(self, state):
        """Retorna uma lista de tuplas (novo_estado, descricao_da_acao)"""
        x, y = state
        successors = []

        if x < self.cap_4:
            successors.append(((self.cap_4, y), "Encher o jarro de 4L"))
        if y < self.cap_3:
            successors.append(((x, self.cap_3), "Encher o jarro de 3L"))
        if x > 0:
            successors.append(((0, y), "Esvaziar o jarro de 4L"))
        if y > 0:
            successors.append(((x, 0), "Esvaziar o jarro de 3L"))
        if x > 0 and y < self.cap_3:
            transfer = min(x, self.cap_3 - y)
            successors.append(((x - transfer, y + transfer), "Transferir de 4L para 3L"))
        if y > 0 and x < self.cap_4:
            transfer = min(y, self.cap_4 - x)
            successors.append(((x + transfer, y - transfer), "Transferir de 3L para 4L"))

        return successors

    def reconstruct_path(self, parent_map, start_state, goal_state):
        current = goal_state
        path = [current]
        actions = []

        while current in parent_map and parent_map[current] is not None:
            prev_state, action = parent_map[current]
            actions.append(action)
            path.append(prev_state)
            current = prev_state

        path.reverse()
        actions.reverse()
        return path, actions

    def bfs(self, initial_state):
        start_time = time.perf_counter()
        if self.is_goal(initial_state):
            return [initial_state], [], 0, 1, 0.0

        queue = deque([initial_state])
        parent_map = {initial_state: None}
        visited = {initial_state}
        states_expanded = 0

        while queue:
            current_state = queue.popleft()
            states_expanded += 1

            if self.is_goal(current_state):
                elapsed = time.perf_counter() - start_time
                path, actions = self.reconstruct_path(parent_map, initial_state, current_state)
                return path, actions, len(actions), states_expanded, elapsed

            for next_state, action in self.get_successors(current_state):
                if next_state not in visited:
                    visited.add(next_state)
                    parent_map[next_state] = (current_state, action)
                    queue.append(next_state)

        elapsed = time.perf_counter() - start_time
        return None, None, 0, states_expanded, elapsed

    def dfs(self, initial_state):
        start_time = time.perf_counter()
        stack = [initial_state]
        parent_map = {initial_state: None}
        visited = set()
        states_expanded = 0

        while stack:
            current_state = stack.pop()
            if current_state in visited:
                continue

            visited.add(current_state)
            states_expanded += 1

            if self.is_goal(current_state):
                elapsed = time.perf_counter() - start_time
                path, actions = self.reconstruct_path(parent_map, initial_state, current_state)
                return path, actions, len(actions), states_expanded, elapsed

            for next_state, action in reversed(self.get_successors(current_state)):
                if next_state not in visited:
                    if next_state not in parent_map:
                        parent_map[next_state] = (current_state, action)
                    stack.append(next_state)

        elapsed = time.perf_counter() - start_time
        return None, None, 0, states_expanded, elapsed

    def dls(self, current_state, limit, parent_map, visited_path, stats):
        stats['expanded'] += 1
        if self.is_goal(current_state):
            return current_state
        if limit <= 0:
            return None

        visited_path.add(current_state)
        for next_state, action in self.get_successors(current_state):
            if next_state not in visited_path:
                parent_map[next_state] = (current_state, action)
                result = self.dls(next_state, limit - 1, parent_map, visited_path, stats)
                if result is not None:
                    return result
        visited_path.remove(current_state)
        return None

    def iddfs(self, initial_state):
        start_time = time.perf_counter()
        stats = {'expanded': 0}
        depth = 0

        while True:
            parent_map = {initial_state: None}
            visited_path = set()
            result_state = self.dls(initial_state, depth, parent_map, visited_path, stats)
            
            if result_state is not None:
                elapsed = time.perf_counter() - start_time
                path, actions = self.reconstruct_path(parent_map, initial_state, result_state)
                return path, actions, len(actions), stats['expanded'], elapsed

            depth += 1
            if depth > 25:
                break

        elapsed = time.perf_counter() - start_time
        return None, None, 0, stats['expanded'], elapsed


def print_search_tree_with_highlight(problem, state, solution_path_set, current_depth=0, max_depth=4, visited=None):
    """
    Exibe a árvore de busca textual e destaca os nós pertencentes ao caminho da solução.
    """
    if visited is None:
        visited = set()

    indent = "    " * current_depth
    
    # Destaca se o estado faz parte da solução ótima/encontrada
    is_on_solution = state in solution_path_set
    marker = " ⭐ [PARTE DO CAMINHO DA SOLUÇÃO]" if is_on_solution else ""
    
    print(f"{indent}Estado: {state}{marker}")

    if current_depth >= max_depth or problem.is_goal(state):
        return

    visited.add(state)
    for next_state, action in problem.get_successors(state):
        if next_state not in visited:
            print(f"{indent} |-- Ação: {action}")
            print_search_tree_with_highlight(problem, next_state, solution_path_set, current_depth + 1, max_depth, visited.copy())


def main():
    print("=" * 60)
    print(" RESOLUÇÃO DO PROBLEMA DOS JARROS D'ÁGUA - BUSCA CEGA ")
    print("=" * 60)

    problem = WaterJugProblem(capacity_4=4, capacity_3=3, target=2)

    while True:
        try:
            print("\nInforme o estado inicial dos jarros:")
            x_init = int(input("Quantidade inicial no jarro de 4L (0 a 4): "))
            y_init = int(input("Quantidade inicial no jarro de 3L (0 a 3): "))

            if 0 <= x_init <= 4 and 0 <= y_init <= 3:
                initial_state = (x_init, y_init)
                break
            else:
                print("[ERRO] Valores fora dos limites permitidos! Tente novamente.")
        except ValueError:
            print("[ERRO] Entrada inválida. Digite números inteiros.")

    print(f"\nEstado Inicial Definido: {initial_state}")
    print("Executando os algoritmos...\n" + "-" * 60)

    # Executando a BFS como referência para destacar a árvore
    path, actions, cost, expanded, elapsed_time = problem.bfs(initial_state)

    print(f">>> Algoritmo: Busca em Largura (BFS)")
    if path:
        print(f"Status: Solução encontrada com {cost} ações em {elapsed_time:.7f}s.")
        print("Caminho da Solução:")
        for i, state in enumerate(path):
            if i == 0:
                print(f"  [Início] {state}")
            else:
                print(f"  [Ação: {actions[i-1]}] -> {state}")
        
        # Convertendo o caminho em um Set para verificação rápida na árvore
        solution_path_set = set(path)

        print("\n" + "=" * 60)
        print(" ÁRVORE DE BUSCA EXPLORADA COM DESTAQUE PARA O CAMINHO DA SOLUÇÃO ")
        print("=" * 60)
        print_search_tree_with_highlight(problem, initial_state, solution_path_set, max_depth=3)
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
