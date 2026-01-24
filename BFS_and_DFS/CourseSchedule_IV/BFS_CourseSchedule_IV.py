from collections import defaultdict, deque
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        graph_table = defaultdict(list)
        indegreelist = [0] * numCourses
        pre_set = [set() for _ in range(numCourses)]

        for pre, cou in prerequisites:
            graph_table[pre].append(cou)
            indegreelist[cou] +=1

        queue = deque()

        for i in range(numCourses):
            if indegreelist[i] == 0:
                queue.append(i)
        
        while queue:
            current = queue.popleft()
            
            for neighbor in graph_table[current]:
                indegreelist[neighbor] -= 1
                pre_set[neighbor].add(current) 
                pre_set[neighbor].update(pre_set[current]) # 修這堂課需要先修完 "先修的先修"

                if indegreelist[neighbor] == 0:
                    queue.append(neighbor)
        
        res = []

        for pre, cou in queries:
            if pre in pre_set[cou]:
                res.append(True)
            else:
                res.append(False)

        return res

"""
### Kahn's Algorithm
1. 建立一個 graph_table, defaultdict, {Node : []}, 用於 graph 的紀錄 
2. 建立一個 indegreelist, 用於紀錄 indegree 的數量
3. 初始化 pre_set, 用於紀錄每一個 Node 所需的先修課程, [{}, {} ,{}]
4. 初始化 graph, 用於紀錄 node 的 neighbor(先修), { 先修 A : 才能修 B }
5. 初始化 queue, 用於後續的 khan's algo 與需要算的 node
6. 處理 {某課程：先修} 於 pre_set, pre_set 還要 update 先修的先修
7. 初始化 res, 用於回傳 answer
8. 如果 pre_set[某課程] = {某先修} 成立於 pre, cou in queries, 則 return True
"""
