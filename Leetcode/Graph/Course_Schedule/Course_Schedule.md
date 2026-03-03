### 1. 核心題意與挑戰

這題是整個計算機科學必學的起點 —— 圖論 (Graph Theory)。
你有 `numCourses` 門課要修，課程從 `0` 到 `numCourses - 1` 。
你拿到了一個陣列 `prerequisites` ，其中 `prerequisites[i] = [A, B]` ，表示如果你要修 A，就必須先修完 B。（這是一條從 $B \rightarrow A$ 的有向邊）。
請判斷你是否可能完成所有課程？

* **隱藏題意**：如果要把所有課修完，這整張課程依賴圖裡面**絕對不可以出現環 (Cycle)**。如果 $A$ 依賴 $B$，$B$ 依賴 $C$，$C$ 又依賴 $A$，這就是一個死結，誰都沒辦法開始修課。這題本質上就是「有向圖的環狀檢測」。

---

### 2. 解法對比與完整程式碼

#### A. 拓撲排序法 (Topological Sort / Kahn's Algorithm) —— **Graph 必背神級框架**

**思路**：
這是一套可以用來解決所有「依賴順序問題」的公式化解法 (Kahn's Algorithm)。
1. **建立資料結構**：我們需要兩樣東西：
   * `adj_list`：一個字典，紀錄這門課修完後，可以解鎖哪些**下一門課**。（也就是有向邊的箭頭指向誰）。
   * `in_degree`：一個陣列，紀錄每門課它目前的「入度 (In-Degree)」也就是**它還有幾門前置課程沒還清**。這是在這套演算法中至關重要的變數，決定生死的狀態機。
2. **尋找突破口**：先把所有 `in_degree == 0` 的課丟進一個 Queue 裡面。這些就是「不用任何前置，現在馬上就能修的這學期先修課」。
3. **擴散 (BFS)**：
   * 從 Queue 中拿出一門課當作修完。因為它修完了，我們就把它在 `adj_list` 裡面所有指向的「下一門課」的 `in_degree` 全部減一（代表前置條件少了一個）。
   * 一旦有哪門課的 `in_degree` 變成 0 了，太棒了！代表它的前置都修完了，我們把它也推進 Queue 裡面。
4. **驗收**：只要把 Queue 從頭到尾走完，我們就算算出總共修了幾門課。如果修完的課數目等於 `numCourses`，代表全部修完（沒有死結）。否則就是有課程因為有環，`in_degree` 永遠無法變成 0！

* **時間複雜度**：$O(V + E)$ (頂點數加邊數，因為圖走訪一次)
* **空間複雜度**：$O(V + E)$ (儲存整個圖的 adj list)

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # 1. 建立圖的鄰接表與入度表
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        # [A, B] 代表 B -> A
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            in_degree[dest] += 1
            
        # 2. 找出所有可以直接修的課 (入度為 0)
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        # 3. BFS 開始修課
        courses_taken = 0
        while queue:
            curr_course = queue.popleft()
            courses_taken += 1
            
            # 巡視修完這門課後能解鎖哪些人
            for neighbor in adj_list[curr_course]:
                in_degree[neighbor] -= 1
                # 如果解鎖完後前置債務清除了，就可以放進 Queue
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # 4. 判斷是否修完所有課
        return courses_taken == numCourses
```

#### B. 深度優先搜尋 (DFS Cycle Detection) —— **純粹利用遞迴堆疊的解法**

**思路**：
這解法不用 `in_degree`，而是每一門課我們都去 DFS 一路深挖它的依賴。如果我們在深挖的過程中，竟然遇到了一門**「我們這次探險路徑上早就遇過的課」**，這就是一個環！
為了標記狀態，我們設一個 `visited` 陣列有三種值：
* `0`: 沒去過
* `1`: 目前這趟路徑正在訪問中
* `2`: 安全（這門課跟它後面的依賴我們都驗證過了，沒死結，以後如果有別的路徑連過來，遇到 `2` 就可以直接 Return True 收工）。

```python
from collections import defaultdict
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj_list = defaultdict(list)
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            
        # 0=未訪問, 1=路徑訪問中, 2=已驗證安全
        visited = [0] * numCourses
        
        def has_cycle(course):
            # 撞到這次路徑上正在訪問的結點 -> 發現環！
            if visited[course] == 1:
                return True
            # 撞到以前驗證過已經安全的結點 -> 沒事
            if visited[course] == 2:
                return False
                
            # 將自己標記為「正在訪問」
            visited[course] = 1
            
            # 繼續深挖下一層
            for neighbor in adj_list[course]:
                if has_cycle(neighbor):
                    return True
                    
            # 全部挖完沒發現環，把自己標記為「安全」
            visited[course] = 2
            return False
            
        # 每一個節點都可能是一個孤島，所以每個節點都要 DFS 一次
        for i in range(numCourses):
            if has_cycle(i):
                return False
                
        return True
```

---

### 3. 實務應用場景

#### 1. 套件管理器 (Package Manager - NPM / Maven)
* **應用**：你在下 `npm install` 或是 `pip install` 時，套件 A 依賴套件 B，套件 B 依賴 C 與 D。NPM 底層就是跑 Topological Sort 決定要用什麼順序抓取並編譯這些套件，若發現循環依賴就會噴出大紅色的 Error 拒絕安裝。

#### 2. CI/CD Pipeline 構建 (Jenkins / GitHub Actions)
* **應用**：設定中寫的 `needs: [build, test]` 就是依賴圖。排程系統用 Kahn's Algorithm 把那些 `needs` 都滿足的 Job 平行部署到雲端 Runner 上，再逐步觸發下一個階段。

---

### 4. 總結筆記

| | Kahn's Algorithm (BFS) | DFS (三色標記法) |
| --- | --- | --- |
| **時間/空間複雜度** | $O(V+E)$ | $O(V+E)$ |
| **面試表現** | **強烈推薦**，邏輯順暢不會繞錯圈，是工程界主流應用。 | 非常看臨場發揮，遞迴容易寫亂。 |
| **死穴/重點** | 建立圖的時候 `[A, B]` 是 `B -> A`，別寫反了導致 In-degree 算錯。 | `visited` 陣列必須設計三種狀態 `-1, 0, 1`。 |
