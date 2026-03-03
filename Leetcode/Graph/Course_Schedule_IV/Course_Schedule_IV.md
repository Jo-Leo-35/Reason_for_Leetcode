### 1. 核心題意與挑戰

這題是 Course Schedule 宇宙的第三部曲。
給定課程總數 `numCourses` 和一個陣列 `prerequisites`。
接下來給你一個陣列 `queries`，其中 `queries[j] = [u, v]`。對於每個查詢，請判斷課程 `u` 是否是課程 `v` 的先修課。

* **隱藏題意**：
  * 在圖論中，這叫做「圖的遞移閉包 (Transitive Closure)」或者是「多源點可達性問題 (All-Pairs Reachability)」。
  * 查詢的次數可能高達 $10^4$，如果每次 Query 都去跑一次 DFS 會得到 TLE 超時。必須**預先計算 (Pre-compute)** 好所有的可達性關係。

---

### 2. 解法對比與完整程式碼

#### A. Floyd-Warshall 演算法 —— **最無腦的 $O(N^3)$ 暴力解**

**思路**：
如果 $A \rightarrow B$ 且 $B \rightarrow C$，那麼 $A \rightarrow C$。
用一個二維的布林陣列 `reachable[i][j]` 記錄 $i$ 能不能抵達 $j$。三重迴圈 $V$ (中介點) $\times$ $I$ (起點) $\times$ $J$ (終點) 掃描一次，所有關係一網打盡。

* **缺點**：如果課程數目超過幾百，這會是 $N^3$ 的夢靨。

#### B. 基於 Kahn's Algorithm 的路徑繼承法 —— **最高效的面試正解**

**思路**：
結合原本 BFS 拓樸排序的做法。
我們維護一個陣列的集合 `prerequisites_sets`，其中 `prerequisites_sets[i]` 是一個 `Set`，裡面儲存了「所有祖宗十八代」必須要先修的課。
當我們利用 BFS 從一門課 `A` 走到 `B` 時（代表修完 `A` 才能修 `B`）：
* `B` 會繼承 **A 自己**。
* `B` 還會繼承 **A 的所有祖先們**。
因為是 DAG (有向無環圖)，BFS 走到 `B` 並將它加入 Queue 的瞬間（入度等於 0），保證 `B` 前面的所有前置課程都已經把自己的祖宗查明清楚了！

* **時間複雜度**：$O(V + E \times V + Q)$ (每個點最多被塞進 $V$ 個祖宗)。
* **空間複雜度**：$O(V^2)$ (每個點存一個最差長度為 V 的 Set)。

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        # 1. 建立圖與入度
        adj_list = defaultdict(list)
        in_degree = [0] * numCourses
        
        for u, v in prerequisites:
            adj_list[u].append(v)
            in_degree[v] += 1
            
        # 2. 為每個點準備一個 Set，存入所有的祖先
        ancestors = [set() for _ in range(numCourses)]
        
        # 3. BFS 拓樸排序
        queue = deque()
        for i in range(numCourses):
            if in_degree[i] == 0:
                queue.append(i)
                
        while queue:
            curr = queue.popleft()
            
            for neighbor in adj_list[curr]:
                # 繼承 curr，以及 curr 所有的祖宗
                ancestors[neighbor].add(curr)
                ancestors[neighbor].update(ancestors[curr])
                
                # 入度減去
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        # 4. 回答所有查詢
        return [u in ancestors[v] for u, v in queries]
```

---

### 3. 實務應用場景

#### 1. 身分權限系統的繼承關係 (RBAC Role Inheritance)
* **應用**：在 IAM 系統設計中，如果角色 C 繼承自角色 B，角色 B 繼承自角色 A。當系統需要頻繁檢查使用者 (擁有角色 C) 是否具備 A 的權限時，通常會在建立角色 DAG 圖時就 Cache 好完整的繼承 Set 去做 $O(1)$ Answer。

#### 2. Make 檔案與編譯系統 (Build Dependency Checking)
* **應用**：在 Bazel 或是 C++ Makefile 中，我們常常需要 query "某個底層的 `common.o` 被修改了，究竟會影響上層多大範圍的模組需要重編譯？" 這種「被依賴」的廣度與深度探尋。

---

### 4. 總結筆記

| 解題心法 | 說明 |
| --- | --- |
| **不要傻傻地針對每個 Query 都去跑 BFS** | 查詢量大時必須作 Pre-computation (預運算)。 |
| **`ancestors[neighbor].update(ancestors[curr])`** | Set 的 `update` 可以快速吸收別人的所有元素，這是 Python 處理 Graph 繼承時最優美的寫法。 |
| **拓樸排序的彈性** | 只要保證是 DAG，你可以順便在 BFS 中挾帶很多需要動態規劃或是逐步疊加的運算。 |
