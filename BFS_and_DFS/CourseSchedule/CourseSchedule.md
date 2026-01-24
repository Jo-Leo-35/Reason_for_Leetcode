### 1. 核心觀念 (Core Concept)

* **題目本質：** 這不是排課表，而是 **「有向圖的環檢測 (Cycle Detection in Directed Graph)」**。
* **關鍵問題：** 給定一堆依賴關係 (A 依賴 B)，判斷是否出現「死鎖」(A 等 B，B 等 A)。
* **圖論術語：** 我們要找的是這個圖是否為 **DAG (Directed Acyclic Graph, 有向無環圖)**。

---

### 2. 工程實際應用 (Real-World Engineering)

面試官問：「這題演算法在 Google 裡哪裡會用到？」，請回答以下場景：

#### **A. 建置系統 (Build Systems)**

* **場景：** 像是 Bazel (Google 內部用)、Webpack、Make、Maven。
* **問題：** 檔案 A `import` B，檔案 B `import` C。編譯器需要知道編譯順序 (C -> B -> A)。
* **應用：** 如果開發者寫出 A `import` B，且 B `import` A，Build System 必須報錯 "Circular Dependency Detected"。這就是 LeetCode 207。

#### **B. 任務排程與資料管線 (Task Orchestration / ETL)**

* **場景：** Airflow, Kubernetes Jobs。
* **問題：** 每天早上的報表任務 (Task A) 依賴於 資料清理任務 (Task B)。如果設定錯誤造成循環依賴，整個 Pipeline 會卡死。
* **應用：** 在任務執行前，系統會先跑一次拓撲排序檢查，確保流程是單向流動的。

#### **C. 資源死鎖檢測 (Deadlock Detection)**

* **場景：** 資料庫 (Database) 或作業系統 (OS)。
* **問題：** Process 1 鎖住資源 X 等待 Y，Process 2 鎖住資源 Y 等待 X。
* **應用：** OS 會維護一張 "Wait-for Graph"，利用此算法定期掃描，發現環就強制殺掉其中一個 Process 來解開死鎖。

---

### 3. 解題模板 (Templates)

#### **方法一：BFS (Kahn's Algorithm) - 推薦首選 🏆**

* **口訣：** 剝洋蔥法。先找軟柿子 (入度 0) 吃掉，吐出骨頭 (減少鄰居入度)，直到吃完。
* **特點：** 直觀、迭代式 (無 Stack Overflow 風險)、容易改寫成輸出順序 (LC 210)。

```python
from typing import List
from collections import deque, defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 1. 建圖 & 計算入度
        graph = defaultdict(list)
        indegree = [0] * numCourses
        
        for course, prereq in prerequisites:
            graph[prereq].append(course) # prereq -> course
            indegree[course] += 1
            
        # 2. 初始 Queue：將所有 "無門檻" (入度 0) 的課放入
        queue = deque([i for i in range(numCourses) if indegree[i] == 0])
        
        processed_count = 0
        
        # 3. BFS 剝洋蔥
        while queue:
            current = queue.popleft()
            processed_count += 1
            
            for neighbor in graph[current]:
                indegree[neighbor] -= 1 # 拔掉依賴邊
                if indegree[neighbor] == 0:
                    queue.append(neighbor) # 解鎖新課程
                    
        # 4. 驗證是否修完所有課
        return processed_count == numCourses

```

#### **方法二：DFS (三色標記法) - 找環路徑專用**

* **口訣：** 走迷宮插旗子。
* ⚪ **0 (Unvisited):** 沒去過。
* 🔘 **1 (Visiting):** 正在辦案中 (在 Stack 裡)。**遇到這個代表有環！**
* ⚫ **2 (Visited):** 已結案 (安全)。


* **特點：** 程式碼簡潔、適合需要「遞迴回溯」的場景。

```python
from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            
        # 0: Unvisited, 1: Visiting, 2: Visited
        state = [0] * numCourses
        
        def has_cycle(node):
            if state[node] == 1: return True  # 撞到自己 -> 有環
            if state[node] == 2: return False # 已確認安全 -> Pass
            
            state[node] = 1 # 標記為 "辦案中"
            
            for neighbor in graph[node]:
                if has_cycle(neighbor):
                    return True
            
            state[node] = 2 # 標記為 "結案"
            return False

        # 必須遍歷所有點，防範 "不連通圖"
        for i in range(numCourses):
            if has_cycle(i):
                return False
                
        return True

```

---

### 4. 複雜度分析 (Complexity Analysis)

面試時請自信地寫下：

* **時間複雜度 (Time):** 
*  (Vertices): 課程數 `numCourses`。
*  (Edges): 先修條件數 `prerequisites.length`。
* **理由：** 建圖遍歷一次 ，BFS/DFS 每個點進出一次 ，每條邊檢查一次 。


* **空間複雜度 (Space):** 
* **理由：** 鄰接表 `graph` 存了  條邊，輔助陣列 (`indegree`/`state`) 存了  個狀態。



---

### 5. 常見錯誤與除錯 (Debug Checklist)

在 Dry Run 時，請特別檢查這些點：

1. **方向搞反：** 題目是 `[1, 0]` 代表 `0 -> 1`。建圖時別寫反，不然邏輯會全錯。
2. **忘記不連通圖 (Disconnected Graph)：** 如果圖是分開的兩坨，BFS 只要把所有入度 0 的都加進 Queue 就沒問題；DFS 則必須外層包一個 `for` 迴圈跑遍所有點。
3. **List vs Deque：** BFS 的 Queue 絕對不能用 `list.pop(0)`，一定要用 `collections.deque` 的 `popleft()`，否則複雜度退化成 。
4. **DFS 忘記回溯：** DFS 在離開函式前，一定要把狀態改成 `2` (Visited)，否則會重複計算導致 TLE。
