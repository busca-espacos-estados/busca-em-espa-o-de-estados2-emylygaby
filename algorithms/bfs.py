from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(initial, nodes_expanded=0, nodes_generated=1, max_frontier_size=1, depth=0)

        frontier = deque([initial])
        explored = {initial.tiles}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        while frontier:
            curr = frontier.popleft()
            nodes_expanded += 1

            for neighbor in curr.neighbors():
                nodes_generated += 1
                if neighbor.tiles not in explored:
                    if neighbor.is_goal:
                        return SearchResult(
                            solution=neighbor,
                            nodes_expanded=nodes_expanded,
                            nodes_generated=nodes_generated,
                            max_frontier_size=max(max_frontier_size, len(frontier)),
                            depth=neighbor.cost
                        )
                    explored.add(neighbor.tiles)
                    frontier.append(neighbor)
                    max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0
        )
