from collections import defaultdict, deque
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # Topological Sort with ancestor propagation: O(V + EV + Q) time
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        # Store all ancestors of a node in a Set for O(1) query time
        ancestors = [set() for _ in range(numCourses)]
        
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        while queue:
            curr = queue.popleft()
            
            for neighbor in adj_list[curr]:
                # Propagate all ancestors of the current node to the neighbor
                ancestors[neighbor].add(curr)
                ancestors[neighbor].update(ancestors[curr])
                
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        return [u in ancestors[v] for u, v in queries]
