### **1. 溝通前置：對齊三要素 (The Alignment)**

在開始寫 Code 之前，我們先像在面試白板前一樣，確認邊界與限制：

* **Constraints (限制):**
* 課程編號是 `0` 到 `numCourses - 1`。
* 如果發現 **Cycle (環)**（例如 A 擋 B，B 擋 A），則不可能修完，必須回傳 **空陣列 `[]**`。
* 如果有多種合法的修課順序，回傳 **任意一種** 即可。


* **Edge Cases (邊界情況):**
* 沒有任何先修課限制 (`prerequisites` 為空)  任意順序回傳 `0` 到 `n-1`。
* 只有一門課  回傳 `[0]`。


* **Complexity (複雜度):**
* 時間複雜度：，其中  是課程數， 是先修限制數。我們必須處理每個節點和每條邊。
* 空間複雜度：，用於儲存 Graph (Adjacency List) 和 Indegree 陣列。



---

### **2. 核心觀念：剝洋蔥法 (Kahn's Algorithm)**

我們使用 **BFS** 的思路，想像這是一顆洋蔥，你要一層一層剝開：

1. **入度 (Indegree) 概念**：
* 一門課的「入度」代表「還有幾門先修課沒修完」。
* **入度 = 0** 的課：代表沒有門檻，**現在就可以修**。


2. **演算法流程**：
* **Step 1**: 把所有「入度 = 0」的課丟進 Queue（這些是起點）。
* **Step 2**: 從 Queue 拿出一門課（修完它），把它加入結果名單。
* **Step 3**: 通知這門課的後續課程（鄰居），將它們的入度減 1（因為解決了一個擋路石）。
* **Step 4**: 如果某個鄰居的入度變成了 0，代表它解鎖了，丟進 Queue。
* **Loop**: 重複直到 Queue 空。


3. **偵測環 (Cycle Detection)**：
* 如果最後「修完的課程總數」等於 `numCourses`，代表成功。
* 如果不相等（還有課沒修完但 Queue 空了），代表有 Cycle（互相卡死），回傳空陣列。



---

### **3. Strong Hire 程式碼實作 (Python)**

這裡我們嚴格遵守你的要求：**強制模組化**、**語意化命名**。

```python
from collections import deque
from typing import List, Dict

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        使用 Kahn's Algorithm (BFS) 進行拓撲排序。
        Time: O(V + E)
        Space: O(V + E)
        """
        # 1. 構建圖與計算入度
        graph, indegree = self._build_graph(numCourses, prerequisites)
        
        # 2. 執行拓撲排序
        return self._topological_sort(numCourses, graph, indegree)

    def _build_graph(self, numCourses: int, prerequisites: List[List[int]]) -> (Dict[int, List[int]], List[int]):
        """
        Helper Function: 建立 Adjacency List 並計算每個節點的入度 (In-degree)
        """
        graph = {i: [] for i in range(numCourses)}
        indegree = [0] * numCourses
        
        for course, pre_course in prerequisites:
            # 題目給的是 [course, pre_course]，代表 pre_course -> course
            graph[pre_course].append(course)
            indegree[course] += 1
            
        return graph, indegree

    def _topological_sort(self, numCourses: int, graph: Dict[int, List[int]], indegree: List[int]) -> List[int]:
        """
        Helper Function: 使用 Queue 進行 BFS 剝洋蔥
        """
        # 初始化 Queue，將所有沒有擋路石(入度為0)的課程加入
        queue = deque([course for course in range(numCourses) if indegree[course] == 0])
        topological_order = []
        
        while queue:
            current_course = queue.popleft()
            topological_order.append(current_course)
            
            # 遍歷當前課程的後續課程
            for next_course in graph[current_course]:
                indegree[next_course] -= 1
                # 如果入度歸零，代表該課程解鎖
                if indegree[next_course] == 0:
                    queue.append(next_course)
        
        # 驗證是否修完所有課程 (Cycle Check)
        if len(topological_order) == numCourses:
            return topological_order
        else:
            return [] # 存在 Cycle，無法修完

```

---

### **4. 主動驗證：Dry Run**

面試時，寫完 Code 後**不要急著說完成了**，主動拿一個 Test Case 跑一遍。

**測資:** `numCourses = 4`, `prerequisites = [[1,0], [2,0], [3,1], [3,2]]`

* 邏輯：`0->1`, `0->2`, `1->3`, `2->3`。

**Trace:**

1. **_build_graph**:
* `graph`: `{0: [1, 2], 1: [3], 2: [3], 3: []}`
* `indegree`: `[0, 1, 1, 2]` (Course 0 入度為 0，Course 3 入度為 2)


2. **_topological_sort**:
* **Init**: `queue = [0]`, `order = []`
* **Loop 1**:
* Pop `0`. `order = [0]`.
* Neighbors of 0 are `1, 2`.
* `indegree[1]` 變 0 -> Push `1`.
* `indegree[2]` 變 0 -> Push `2`.
* `queue` is now `[1, 2]`.


* **Loop 2**:
* Pop `1`. `order = [0, 1]`.
* Neighbor of 1 is `3`.
* `indegree[3]` 從 2 變 1 (不 Push).
* `queue` is now `[2]`.


* **Loop 3**:
* Pop `2`. `order = [0, 1, 2]`.
* Neighbor of 2 is `3`.
* `indegree[3]` 從 1 變 0 -> Push `3`.
* `queue` is now `[3]`.


* **Loop 4**:
* Pop `3`. `order = [0, 1, 2, 3]`.
* No neighbors.


* **Result**: `len(order)` (4) == `numCourses` (4). Return `[0, 1, 2, 3]`.



---

### **5. 學習筆記與必背模板**

要精通這類題目，請記住以下抽象概念：

#### **抽象概念：任務依賴解析 (Dependency Resolution)**

只要題目提到「**順序 (Order)**」、「**依賴 (Dependency)**」、「**先做 A 才能做 B**」，就是 **Topological Sort**。

#### **必背模板 (BFS - Kahn's Algorithm)**

腦中要有這張表：

| 步驟 | 關鍵資料結構 | 動作 |
| --- | --- | --- |
| **1. 建圖** | `Map<Node, List<Node>>` | 記錄 `A -> B` (A 指向 B) |
| **2. 記帳** | `int[] indegree` | 記錄每個點被多少人指著 (依賴數) |
| **3. 啟動** | `Queue` | 把所有 `indegree == 0` 的點丟進去 |
| **4. 擴散** | `while queue` | Pop 當前點 -> 鄰居 `indegree--` -> 若鄰居歸零則 Push |

---

### **6. Interview Follow-up & System Design**

從面試官的角度，這題寫出來只是 Basic Hire。我們要往 Strong Hire 推進：

#### **Follow-up Questions:**

1. **Q: 如果題目不需要你回傳順序，只需要回傳 True/False (能不能修完)？**
* **A:** 這就是 LeetCode 207 (Course Schedule I)。程式碼完全一樣，只是最後 return `len(order) == numCourses`。


2. **Q: 我們可以用 DFS 做嗎？**
* **A:** 可以。DFS 的邏輯是「後序遍歷 (Post-order Traversal)」的**反轉**。我們需要三個狀態來偵測 Cycle：`Unvisited (0)`, `Visiting (1)`, `Visited (2)`。如果 DFS 走到 `Visiting` 的點，就是有環。
* *點評：但在面試中，BFS (Kahn's) 對於「入度」的思維更直觀，且更容易修改成並行處理。*



#### **Micro System Design (微系統設計):**

這題的演算法在實際產業中非常重要，可以延伸到 **"Build System" (如 Webpack, Maven, Bazel)** 或 **"Task Scheduler" (如 Airflow)** 的設計。

* **情境**: 設計一個分散式的任務排程系統，任務之間有依賴關係。
* **應用這題的算法**:
1. **解析依賴**: 使用 Topological Sort 決定執行順序。
2. **並行執行 (Parallel Execution)**:
* 在 BFS 的每一層 (Level)，Queue 裡面的所有任務都是**彼此獨立**的（入度都剛好歸零）。
* **關鍵優化**: 我們可以把 Queue 裡的所有任務同時丟給 Worker Pool 去並行跑，而不是一個一個跑。這能最大化產能。
* 例如：在編譯程式碼時，檔案 A 和檔案 B 都只依賴檔案 C。當 C 編譯完，A 和 B 可以同時在不同 CPU 核心上編譯。
