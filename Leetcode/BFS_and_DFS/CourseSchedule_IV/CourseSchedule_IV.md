## 1. 題目核心 (The Core Idea)

* **關鍵字**：Graph Reachability（圖的可達性）、Transitive Closure（傳遞閉包）。
* **一句話描述**：給定先修依賴關係，判斷任意兩堂課 `(u, v)` 是否存在「直接或間接」的先修關係（即 `u` 能否走到 `v`）。
* **類比**：族譜查詢。如果 A 是 B 的父親，B 是 C 的父親，則 A 也是 C 的祖先。

---

## 2. 面試前置三要素 (The Three Elements)

在動手寫 Code 前，必須先與面試官對齊的規格：

1. **Constraints (限制條件)**
* ：極小。強烈暗示  算法 (Floyd-Warshall) 是可行的。
* Queries ：查詢非常多。強烈暗示必須做 **預處理 (Pre-computation)**，將查詢降至 。


2. **Edge Cases (邊界情況)**
* **Disconnected Graph**：圖是不連通的（A區塊跟B區塊沒關係）。
* **No Prerequisites**：沒有任何依賴，所有查詢應為 False。
* **Linear vs. Dense**：單鏈結構 () vs 複雜網狀結構（影響 Set Merge 的效能）。


3. **Complexity Goal (預期複雜度)**
* **Time**: 預處理  或 ，查詢 。
* **Space**:  用於儲存可達性表。



---

## 3. 演算法決策矩陣 (Decision Matrix)

這題有兩個 Strong Hire 等級的解法，取決於  的大小與圖的特性：

| 特性 | Floyd-Warshall (FW) | Kahn's Algo (BFS + Set Propagation) |
| --- | --- | --- |
| **適用場景** | ** 很小 ()**，且圖稠密。 | ** 稍大**，圖稀疏，或需要 Topo Sort 順序。 |
| **複雜度** |  (穩定) |  (受 Set Merge 影響) |
| **思路** | DP：枚舉中繼站 ，填表 `dp[i][j]`。 | BFS：依賴傳遞，子節點繼承父節點的 Set。 |
| **優勢** | 程式碼最短 (3 loops)，不易錯。 | 符合系統設計 (Build System) 直覺，模組化強。 |

---

## 4. 模組化程式碼實作 (Modular Implementation)

採用 **Kahn's Algorithm + Set Propagation**，強調語意化命名與邏輯拆分。

```python
from collections import defaultdict, deque
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        """
        解題思路：使用 Khan's Algorithm 進行依賴傳遞 (Dependency Propagation)。
        對於每條邊 u -> v，我們將 u 的所有先修課集合 (Ancestors) 合併給 v。
        """
        
        # 1. 初始化資料結構
        adj_list = defaultdict(list)
        indegree = [0] * numCourses
        # prereq_set[i] 儲存課程 i 的所有 "祖先" (直接與間接先修)
        # 使用 List Comprehension 確保每個 Set 都是獨立物件
        prereq_set = [set() for _ in range(numCourses)]

        # 2. 建圖 (Build Graph)
        self._build_graph(prerequisites, adj_list, indegree)

        # 3. 執行依賴傳遞 (Execute Propagation)
        self._propagate_dependencies(numCourses, adj_list, indegree, prereq_set)
        
        # 4. 處理查詢 (Process Queries)
        return self._process_queries(queries, prereq_set)

    def _build_graph(self, prerequisites: List[List[int]], adj: dict, indegree: List[int]) -> None:
        """ 建立鄰接表與計算入度 """
        for pre, course in prerequisites:
            adj[pre].append(course)
            indegree[course] += 1

    def _propagate_dependencies(self, n: int, adj: dict, indegree: List[int], prereq_set: List[set]) -> None:
        """ 
        核心邏輯：BFS 拓撲排序 + 集合合併 
        Time: O(N * E) - 因為每次處理邊時，可能涉及 O(N) 的 Set Update
        """
        queue = deque()
        for i in range(n):
            if indegree[i] == 0:
                queue.append(i)
        
        while queue:
            current = queue.popleft()
            
            for neighbor in adj[current]:
                # 邏輯 1: current 是 neighbor 的直接先修
                prereq_set[neighbor].add(current)
                
                # 邏輯 2: current 的所有祖先也是 neighbor 的先修 (滾雪球效應)
                # update 操作是 O(Size of Set)，最壞情況為 O(N)
                prereq_set[neighbor].update(prereq_set[current]) 
                
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

    def _process_queries(self, queries: List[List[int]], prereq_set: List[set]) -> List[bool]:
        """ 
        回答查詢
        Time: O(Q) - Set Lookup 為 O(1)
        """
        result = []
        for u, v in queries:
            # 檢查 u 是否在 v 的先修集合中 (Hash Lookup)
            result.append(u in prereq_set[v])
        return result

```

---

## 5. 複雜度深度解析 (Complexity Deep Dive)

這是區分 Junior 與 Senior 的戰場。

### A. 時間複雜度：

為什麼不是 ？

* **BFS 基本盤**：訪問每個節點和邊是 。
* **隱藏成本 (The Hidden Cost)**：`pre_set[neighbor].update(pre_set[current])`。
* 這行程式碼本質是一個 **迴圈**。
* 隨著 BFS 推進，`pre_set[current]` 會像**滾雪球**一樣越來越大（最多  個元素）。
* 總共有  條邊，每條邊最壞要搬運  個元素 。



### B. 空間複雜度：

* 我們為每個課程維護一個 Set。
* 最壞情況下（單鏈或稠密圖），每個 Set 都要存接近  個先修課。
* 總空間 = 。

### C. 查詢複雜度： vs 

* **List Lookup (`if x in list`)**：。需要遍歷整個列表比對。
* **Set Lookup (`if x in set`)**：。
* **原理**：Hash Function 算出記憶體地址  直接跳轉檢查。
* **面試話術**：雖然 Worst Case (Hash Collision) 是 ，但在一般工程實務與演算法分析中，視為 **Amortized **。



---

## 6. Python 實作陷阱 (Pitfalls)

* **List Comprehension**:
* ✅ `[set() for _ in range(N)]`：創建  個獨立的 Set 物件。
* ❌ `[set()] * N`：創建  個指向**同一個** Set 的指標（淺拷貝），改一個全部都會變，這是 Bug。