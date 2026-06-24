"""Script de demonstração interativo para o 8-puzzle."""

import sys
from puzzle.state import State
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def is_solvable(tiles) -> bool:
    seq = [t for t in tiles if t != 0]
    inversions = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inversions += 1
    return inversions % 2 == 0


def print_result(name: str, result):
    print(f"\n{'='*40}")
    print(f"Algoritmo : {name}")
    if result.found:
        print(f"Solução   : {' → '.join(result.actions)}")
        print(f"Custo     : {result.path_cost}")
        print(f"Profund.  : {result.depth}")
    else:
        print("Solução   : NÃO ENCONTRADA")
    print(f"Expandidos: {result.nodes_expanded}")
    print(f"Gerados   : {result.nodes_generated}")
    print(f"Fronteira : {result.max_frontier_size} (máx)")


def get_predefined_states():
    return {
        "1": ("Muito Fácil (2 movimentos)", (1, 2, 3, 4, 5, 6, 0, 7, 8)),
        "2": ("Fácil (3 movimentos)", (1, 2, 3, 0, 4, 6, 7, 5, 8)),
        "3": ("Médio (original - ~20 movimentos)", (2, 8, 3, 1, 6, 4, 7, 0, 5)),
        "4": ("Objetivo", (1, 2, 3, 4, 5, 6, 7, 8, 0))
    }


def main():
    print("====================================================")
    print("      8-PUZZLE - BUSCA EM ESPAÇO DE ESTADOS         ")
    print("====================================================")
    
    # 1. Escolha do estado inicial
    print("\nEscolha o Estado Inicial:")
    print("1 - Escolher um estado pré-definido")
    print("2 - Digitar um estado personalizado")
    op = input("Opção: ").strip()

    tiles = None
    if op == "1":
        states = get_predefined_states()
        for k, v in states.items():
            print(f"{k} - {v[0]}: {v[1]}")
        sub_op = input("Escolha o estado (padrão 3): ").strip() or "3"
        if sub_op in states:
            tiles = states[sub_op][1]
        else:
            print("Opção inválida, usando o estado Médio.")
            tiles = states["3"][1]
    else:
        print("\nDigite os 9 números (0 a 8) separados por espaços (ex: 2 8 3 1 6 4 7 0 5):")
        try:
            inp = input("Entrada: ").strip()
            if not inp:
                print("Entrada vazia, utilizando estado padrão Médio (original).")
                tiles = (2, 8, 3, 1, 6, 4, 7, 0, 5)
            else:
                tiles = tuple(map(int, inp.split()))
        except Exception:
            print("Formato inválido! Utilizando estado padrão Médio (original).")
            tiles = (2, 8, 3, 1, 6, 4, 7, 0, 5)

    if not tiles or len(tiles) != 9 or set(tiles) != set(range(9)):
        print("\n[ERRO] O estado fornecido é inválido (deve conter os valores de 0 a 8 sem repetição).")
        print("Usando estado padrão Médio (original): (2, 8, 3, 1, 6, 4, 7, 0, 5)")
        tiles = (2, 8, 3, 1, 6, 4, 7, 0, 5)

    solv = is_solvable(tiles)
    print("\nEstado selecionado:")
    initial = State(tiles)
    print(initial)
    if not solv:
        print("\n[AVISO] ATENÇÃO: Este estado NÃO é solúvel!")
        print("O número de inversões é ímpar. Nenhum algoritmo encontrará uma solução.")
        confirm = input("Deseja continuar mesmo assim? (s/n, padrão n): ").strip().lower()
        if confirm != "s":
            print("Saindo...")
            sys.exit(0)

    print("\nEscolha o algoritmo de busca:")
    print("1 - BFS (Busca em Largura)")
    print("2 - DFS (Busca em Profundidade com Limite)")
    print("3 - A* (Busca Estrela com Manhattan)")
    print("4 - Executar todos e comparar")
    
    algo_op = input("Opção (padrão 4): ").strip() or "4"
    
    if algo_op == "1":
        print("\nExecutando BFS...")
        print_result("BFS", BFS().search(initial))
    elif algo_op == "2":
        lim_inp = input("Digite o limite de profundidade (padrão 50): ").strip()
        lim = 50
        if lim_inp.isdigit():
            lim = int(lim_inp)
        print(f"\nExecutando DFS (Limite={lim})...")
        print_result("DFS", DFS(depth_limit=lim).search(initial))
    elif algo_op == "3":
        print("\nExecutando A*...")
        print_result("A*", AStar().search(initial))
    else:
        print("\nExecutando todos os algoritmos...")
        print_result("BFS", BFS().search(initial))
        print_result("DFS", DFS().search(initial))
        print_result("A*", AStar().search(initial))


if __name__ == "__main__":
    main()
