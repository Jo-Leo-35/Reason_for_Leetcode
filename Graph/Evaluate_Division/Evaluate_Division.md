### 1. 核心題意與挑戰

給你一個方程式陣列 `equations` 和一個實數陣列 `values`。
`equations[i] = [A_i, B_i]` 表示 $A_i / B_i = values[i]$。
給你一個問題陣列 `queries`，請根據已知條件求出 `queries[j] = [C_j, D_j]` 的答案。如果無法從已知條件推導出來，則回傳 `-1.0`。

* **隱藏挑戰**：
  * 這題把數字除法偽裝成字串。其實 `A / B = 2.0` 等於說從點 `A` 到點 `B` 有一條有向邊，長度（倍率）是 `2.0`。
  * 而且反過來，`B / A = 1/2.0 = 0.5`！代表這是一張**有權重的雙向圖 (Weighted Undirected Graph)**。
  * 「從 C 走到 D」的結果，其實就是一路上經過的所有權重**全部相乘**的結果！

---

### 2. 解法對比與完整程式碼

#### DFS / BFS 走訪圖尋找路徑 —— **最強烈建議的解法**

**思路**：
1. **建圖**：因為是字串，我們用字典的字典來當作 `adj_list`。例如 `graph['a']['b'] = 2.0`。同時也要建反向邊 `graph['b']['a'] = 0.5`。
2. **回答每個問題**：
   * 如果起點或終點根本不在我們的地圖上，直接判死刑回傳 `-1.0`。
   * 如果起點和終點一樣（例如問 `a/a`），那答案就是 `1.0`。
   * 如果不是，那就是一張標準的迷宮尋路題！我們用 BFS 從起點出發，開始廣度優先搜尋。
   * 要注意有些時候圖中會有環，所以必須用一個 `visited` Set 來避免無窮迴圈。

* **時間複雜度**：$O(Q \times (V+E))$ (每個 query 可能遍歷全圖)
* **空間複雜度**：$O(V+E)$

```python
from collections import defaultdict, deque
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        # 1. 建立雙向權重圖
        graph = defaultdict(dict)
        
        for (u, v), val in zip(equations, values):
            graph[u][v] = val
            graph[v][u] = 1.0 / val  # 重點：反向路徑是倒數
            
        def bfs_find_path(start, end):
            # 如果連點都沒出現過，直接宣告失敗
            if start not in graph or end not in graph:
                return -1.0
                
            # Queue 裡放 (當前節點, 累積出來的超級乘積倍率)
            queue = deque([(start, 1.0)])
            visited = set()
            visited.add(start)
            
            while queue:
                curr_node, curr_product = queue.popleft()
                
                # 找到終點了，也就是這條路徑所有 multiplier 乘出來的值就是答案
                if curr_node == end:
                    return curr_product
                    
                # 繼續往下找遍所有鄰居
                for neighbor, weight in graph[curr_node].items():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        # 將當前的乘積再乘上這條邊的 weight，然後傳遞下去
                        queue.append((neighbor, curr_product * weight))
                        
            return -1.0
            
        # 2. 對每個 query 去跑一次 BFS 探險
        return [bfs_find_path(c, d) for c, d in queries]
```

*(註：另外有一種並查集 (Union Find with Weights) 的解法，但這會讓原本就很複雜的並查集變得更加晦澀，對於面試而言投報率極低，強烈建議用 BFS 解決即可)*

---

### 3. 實務應用場景

#### 1. 跨國貨幣的三角套利 (Triangular Arbitrage in Forex)
* **應用**：在外匯市場上，你有一堆已知的匯率牌價關係 (EUR/USD, USD/JPY, JPY/GBP)。若你想知道 EUR 到 GBP 目前的交叉匯率，你就是在做全網連線與邊長乘積運算。若換了多個國家一圈回到歐元發現倍率大於 1，這就是在找獲利空間。

#### 2. 公制單位的自動換算系統 (Unit Conversion Engine)
* **應用**：如果系統知道 `1 m = 100 cm` 和 `1 cm = 10 mm`，當你要系統回答出一個沒背過的東西如 `miles to mm` 時，系統就是建構出這個知識圖譜再用 BFS 算出兩點之間的倍率。

---

### 4. 總結筆記

| 面試提示 | 說明 |
| --- | --- |
| **不要被方程式嚇到了** | 這題骨子裡就是求「Graph Shortest/Any Path 的邊權重連乘值」。 |
| **建雙向邊** | `a/b = 2.0` 自動隱含了 `b/a = 0.5`。 |
| **`start not in graph`** | 非常賤的陷阱。他可以問一個根本沒提供過定義的變數量詞 `x / x`，答案不是 `1.0` 而是 `-1.0` （因為沒被定義過）。 |
