### 1. 核心題意與挑戰

和 Course Schedule I 一模一樣，只是這題不只問「能不能修滿所有課」，這題還要求你印出一個合法的**修課順序 (Order)**。如果修不完，印出空陣列 `[]`。

* **隱藏題意**：如果你上一題是用 Kahn's Algorithm (BFS)，這題只要多加一行程式碼就完美解決了！這就是 Topological Sort 強大的地方。

---

### 2. Kahn's Algorithm 程式碼實作

**思路**：
同上一題。我們在每次把一門課從 Queue 裡 `popleft()` 出來當作「修過」時，順手把它 `append()` 到一個叫 `order_result` 的陣列裡面。
走到最後，如果修完的課程數等於總課數，直接回傳 `order_result`。如果不等於，代表發生死鎖，回傳 `[]`。

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # 1. 建圖
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        # 2. 找起點
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        # 3. BFS 與記錄順序! (新增的地方)
        order_result = []
        
        while queue:
            curr_course = queue.popleft()
            # 走到哪紀錄到哪
            order_result.append(curr_course)
            
            for neighbor in adj_list[curr_course]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # 4. 判斷是否有死結
        if len(order_result) == numCourses:
            return order_result
        else:
            return []
```

---

### 3. 解題心法

* 上一題的 `courses_taken` 計數器變成了 `order_result` 陣列，長度等於計數器。
* 當面試官把題目的結尾從「是不是」變成「把路徑印出來」時，BFS 的寫法比 DFS 優勢太多了。如果是 DFS，還得在遞迴時把結果逆向塞進 Array 再整個 Reverse 過來，非常折騰頭腦。Kahn's 演算法就是拓樸排序的親兒子無誤。
