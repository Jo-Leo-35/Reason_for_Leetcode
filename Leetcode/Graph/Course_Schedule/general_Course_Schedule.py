'''
演算法步驟（Kahn's Algorithm - BFS 拓樸排序）：
1. 找出課程的先修順序，標準的圖論 Topological Sort 問題。通用且較易追蹤進度的解法是 Kahn's 演算法 (BFS)。
2. 我們需要兩樣圖的組件：
   - 一個 `in_degree` 陣列：記錄每堂課前面還擋著幾堂先修課（擋箭牌/入度）。
   - 一個 `adj_list` 字典：記錄每堂課念完後，可以「解鎖」哪些後續課程（相鄰節點）。
3. 掃描 `prerequisites`：把 `in_degree` 和 `adj_list` 建立起來。
4. 將所有 `in_degree` 等於 0 的課（代表沒有任何先修限制，可以直接上的課），通通推進一個 Queue 裡面。
5. 設立一個計數器 `courses_taken = 0`。
6. 開始拔蘿蔔 (BFS)：從 Queue 裡拿出一堂課，`courses_taken += 1`。
   - 去 `adj_list` 看看這堂課解鎖了哪些後續課程。
   - 把那些後續課程的 `in_degree` (擋箭牌) 通通減一。
   - 如果某堂後續課的 `in_degree` 變成 0 了，代表限制解除，把它推進 Queue 裡等待上課。
7. 當 Queue 空了之後，如果 `courses_taken == numCourses` 代表所有課都上完了，無環存在；否則代表有死胡同（環）導致有些課永遠入度退不到 0，回傳 False。
'''
from collections import defaultdict, deque
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        courses_taken = 0
        while queue:
            curr_course = queue.popleft()
            courses_taken += 1
            
            for neighbor in adj_list[curr_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        return courses_taken == numCourses
