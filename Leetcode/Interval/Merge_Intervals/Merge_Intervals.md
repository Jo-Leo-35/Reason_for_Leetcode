### 1. 核心題意與挑戰

給定一個區間陣列 `intervals`，其中 `intervals[i] = [start_i, end_i]`。
請你合併所有重疊的區間，並返回一個不重疊的區間陣列，該陣列需恰好涵蓋輸入中的所有區間。

* **隱藏挑戰**：
  * 輸入的區間不一定是有序的。`[[1,4], [0,2]]` 也是可能的輸入。如果硬要遍歷檢查重疊，時間複雜度會是 $O(N^2)$。

---

### 2. 解法對比與完整程式碼

#### 唯一標準正解：排序後遍歷 (Sorting & Linear Scan)

**思路**：
處理所有的區間問題，90% 都要**先根據區間的 `start` 進行排序**。
一旦根據起點排序好了，我們就可以保證：
如果區間 B 要跟區間 A 重疊，那 B 的起點絕對在 A 的終點之前（或是剛好重疊）。
因為 B 的起點一定在 A 的起點之後（因為排過序了），所以我們只需要關注**目前的終點**推進到哪裡。

具體作法：
1. 先將 `intervals` 按照 `start` 升序排列。
2. 建立一個 `merged` 陣列，先把第一個區間放進去。
3. 開始遍歷後面的區間，設當前最後放入 `merged` 的區間叫 `last`，正在看的區間叫 `curr`。
4. 如果 `curr.start <= last.end`，代表兩者重疊了！我們將它們合併：更新 `last.end = max(last.end, curr.end)`。注意要取 Max，因為可能是 `[1,4]` 把 `[2,3]` 整個包住的情況。
5. 如果沒有重疊，代表 `curr` 是一個全新的獨立區間，直接放入 `merged` 的尾端。

* **時間複雜度**：$O(N \log N)$ (瓶頸在於排序，掃描只需 $O(N)$)。
* **空間複雜度**：$O(N)$ (回傳的新陣列，或 Python 排序算法的內部開銷)。

```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
            
        # 1. 以每個區間的 start (即 x[0]) 為基準進行從小到大排序
        intervals.sort(key=lambda x: x[0])
        
        # 2. 初始化結果陣列，先放入第一個區間
        merged = [intervals[0]]
        
        for curr in intervals[1:]:
            last = merged[-1] # merged 裡面最後一個處理好的區間
            
            # 3. 如果最新這個區間的起點，小於等於陣列尾端區間的終點，代表重疊了
            if curr[0] <= last[1]:
                # 合併：維持起點不變，終點取兩者最大的
                last[1] = max(last[1], curr[1])
            else:
                # 4. 沒有重疊，獨立成新區間
                merged.append(curr)
                
        return merged
```

---

### 3. 實務應用場景

#### 1. IP 位址黑名單/路由表壓縮 (CIDR Block Merging)
* **應用**：防火牆常常會載入數以萬計的黑名單 IP 區段。為了加速後續的 IP 封包比對，系統啟動時一定會把所有重疊網段進行 Merge，減少比對次數。

#### 2. 行事曆的空閒時間尋找 (Free/Busy Time Slotting)
* **應用**：Google Calendar 中，要尋找部門所有人都有空的時間，會先將每個人的忙碌區間 (Busy Intervals) 收集起來全部做一次 Merge Intervals。合併後的區間之外，就是完全連續的空閒時段。

---

### 4. 總結筆記

| 記憶點 | 說明 |
| --- | --- |
| **`intervals.sort(key=lambda x: x[0])`** | 解決 9 成區間題的起手式。 |
| **`curr[0] <= last[1]`** | 判斷是否有交集的鐵則。 |
| **`max(last[1], curr[1])`** | 合併不是無腦把右邊塞過去，要防範「大包小」的極端案例。 |
