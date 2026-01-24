from collections import defaultdict, deque
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        graph_indegee = [0] * numCourses
        
        for cou, pre in prerequisites:
            graph[pre].append(cou)
            graph_indegee[cou] += 1 

        queue = deque()
        order = []
        for i in range(numCourses):
            if graph_indegee[i] == 0:
                queue.append(i)
        
        count = 0
        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                graph_indegee[neighbor] -=1
                if graph_indegee[neighbor] == 0:
                    queue.append(neighbor)
            count += 1
            order.append(current)

        if count != numCourses:
            return []
        else:
            return order
        
        
"""
### Kahn's Algorithm
1. 建立一個 graph, {Node : [Neighibor]}
2. 建立一個 List,  用於紀錄 Node 的 indegree
3. 建立一個 Queue, 用於 bfs, 並將 indegree 讀入作為初始節點
4. 建立 count 變數, 用於計算成功的課數
5. Queue 的值都是 indegree = 0 的數, 所以 pop 出來並計算
"""
