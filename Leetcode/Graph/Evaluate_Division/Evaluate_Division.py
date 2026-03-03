from collections import defaultdict, deque
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # Weighted Undirected Graph with BFS
        graph = defaultdict(dict)
        
        for (u, v), val in zip(equations, values):
            graph[u][v] = val
            graph[v][u] = 1.0 / val
            
        def bfs_find_path(start, end):
            if start not in graph or end not in graph:
                return -1.0
                
            queue = deque([(start, 1.0)])
            visited = set()
            visited.add(start)
            
            while queue:
                curr_node, curr_product = queue.popleft()
                
                if curr_node == end:
                    return curr_product
                    
                for neighbor, weight in graph[curr_node].items():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, curr_product * weight))
                        
            return -1.0
            
        return [bfs_find_path(c, d) for c, d in queries]
