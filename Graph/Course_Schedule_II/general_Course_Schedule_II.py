'''
演算法步驟：
1. 本題是 Course Schedule I 的孿生兄弟，只是我們不只問能不能畢業，還要問最終修課的一份有效名單。
2. 原汁原味套用 Kahn's Algorithm (BFS 拓樸排序)。
3. 在 BFS 的拔蘿蔔階段，每次從 Queue 裡彈出一堂 `curr_course`，我們就把它放進我們的 `order_result` 陣列清單內！
4. 當 Queue 空了之後，我們只要簡單判斷：`order_result` 裡面存的課程總數，有沒有等於 `numCourses`？
5. 如果有，代表世間太平，我們順利把所有課都拔乾淨了，直接回傳 `order_result`。
6. 如果沒有（例如有環死機了），因為條件要求失敗回傳空陣列，於是我們就回傳 `[]`。
'''
from collections import defaultdict, deque
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        order_result = []
        
        while queue:
            curr_course = queue.popleft()
            order_result.append(curr_course)
            
            for neighbor in adj_list[curr_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(order_result) == numCourses:
            return order_result
        return []
