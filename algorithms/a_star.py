import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        dist = 0
        for idx, val in enumerate(state.tiles):
            if val != 0:
                goal_idx = val - 1
                curr_row, curr_col = idx // 3, idx % 3
                goal_row, goal_col = goal_idx // 3, goal_idx % 3
                dist += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return dist

    def search(self, initial: State) -> SearchResult:
        # frontier elements: (f_value, counter, state)
        counter = 0
        frontier = []
        heapq.heappush(frontier, (self.heuristic(initial), counter, initial))

        explored = {initial.tiles: 0}

        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        solution = None

        while frontier:
            f, _, curr = heapq.heappop(frontier)

            if curr.tiles in explored and explored[curr.tiles] < curr.cost:
                continue

            if curr.is_goal:
                solution = curr
                break

            nodes_expanded += 1
            for neighbor in curr.neighbors():
                nodes_generated += 1
                g_cost = neighbor.cost
                if neighbor.tiles not in explored or g_cost < explored[neighbor.tiles]:
                    explored[neighbor.tiles] = g_cost
                    counter += 1
                    f_val = g_cost + self.heuristic(neighbor)
                    heapq.heappush(frontier, (f_val, counter, neighbor))

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=solution,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=solution.cost if solution else 0
        )
