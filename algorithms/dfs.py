from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        visited = {initial.tiles: 0}
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        solution = None

        while frontier:
            curr = frontier.pop()

            if curr.is_goal:
                solution = curr
                break

            if curr.cost < self.depth_limit:
                nodes_expanded += 1
                for neighbor in reversed(curr.neighbors()):
                    nodes_generated += 1
                    depth = neighbor.cost
                    if neighbor.tiles not in visited or depth < visited[neighbor.tiles]:
                        visited[neighbor.tiles] = depth
                        frontier.append(neighbor)
                
                max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=solution,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=solution.cost if solution else 0
        )
