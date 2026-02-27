'''
演算法步驟（Floyd-Warshall 多源最短路徑 O(V^3) 經典寫法）：
1. 這一題的本質是要問「圖中任意兩點之間，是否存在一條相連的路徑」。這恰好是 Floyd-Warshall (佛洛伊德演算法) 中「尋找傳遞閉包 (Transitive Closure)」的絕佳應用！
2. 我們建立一個 `V x V` 的布林值二維矩陣 `connected`，初始化全為 `False`。
3. 歷遍所有的給定先修課，把直接有相連的點設為 `True`：`connected[pre][course] = True`。
4. 【核心的三層迴圈】：
   - 外層迴圈 `k` 代表「中繼站」。
   - 中層迴圈 `i` 代表「起點」。
   - 內層迴圈 `j` 代表「終點」。
5. 如果 `i` 到 `k` 是通的，而且 `k` 到 `j` 也是通的，代表我們可以搭特快車！那麼 `i` 到 `j` 就是通的，我們就把 `connected[i][j]` 設為 `True`。這就是著名的狀態轉移方程：`connected[i][j] = connected[i][j] or (connected[i][k] and connected[k][j])`。
6. 這三層迴圈無情攪拌過後，圖中哪裡能走到哪裡，所有秘密都被攤在陽光下。
7. 回答 Query 時，依然是 O(1) 的超暴力直接查表！
'''
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # 建立 V x V 的 Boolean 矩陣
        connected = [[False] * numCourses for _ in range(numCourses)]
        
        for pre, course in prerequisites:
            connected[pre][course] = True
            
        # Floyd-Warshall 極致的三層靈魂迴圈
        for k in range(numCourses):
            for i in range(numCourses):
                for j in range(numCourses):
                    connected[i][j] = connected[i][j] or (connected[i][k] and connected[k][j])
                    
        # O(1) 暴力回答
        return [connected[u][v] for u, v in queries]
