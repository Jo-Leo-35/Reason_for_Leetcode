'''
演算法步驟（拓樸排序 + 祖先傳播 Set O(V + EV + Q)）：
1. Course Schedule IV 是一個需要快速回應多筆查詢（某堂課是否為另一堂課的先修課）的問題。
2. 我們依然使用 Kahn's Algorithm (BFS) 進行拓樸排序。這就像是課程時間軸的洪流。
3. 我們建立一個長度為 `numCourses` 的陣列 `ancestors`。陣列裡的每一格都存放一個獨立的 Python `set`！這個 `set` 的使命是把這堂課所有的「老祖宗（歷代先修課）」通通都記下來。
4. 在 BFS 拔蘿蔔的階段：
   - 每當我們從 Queue 裡面拿出一堂 `curr` 課，準備解鎖它的相鄰後代課 `neighbor` 時。
   - 我們鄭重地向 `neighbor` 宣告：「我不只是你的先修課，我背後的所有老祖宗也都自動成為你的先修課了！」。
   - 代碼實作：`ancestors[neighbor].add(curr)`，然後再把所有的老祖宗疊加上去 `ancestors[neighbor].update(ancestors[curr])`。
5. 經過這番傳播，BFS 拔完蘿蔔後，所有的 `ancestors` 陣列已經吸飽了日月精華。
6. 我們能以 O(1) 的完美時間，無情地回答題目的任何查詢：`u in ancestors[v]`！
'''
from collections import defaultdict, deque
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        ancestors = [set() for _ in range(numCourses)]
        
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        while queue:
            curr = queue.popleft()
            
            for neighbor in adj_list[curr]:
                ancestors[neighbor].add(curr)
                ancestors[neighbor].update(ancestors[curr])
                
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        return [u in ancestors[v] for u, v in queries]
