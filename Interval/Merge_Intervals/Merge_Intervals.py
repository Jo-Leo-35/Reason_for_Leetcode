### 1. 核心抽象模板：排序與貪婪掃描

這題的精髓在於透過**排序**將二維空間的重疊問題，簡化為一維數線上的**連續性判斷**。

* **抽象概念**：`結果集中的最後一個區間 (Merged[-1])` 是當前的邊界守門員。
* **決策邏輯**：
* **無重疊**：下一個區間起點 > 守門員終點。動作：`append` 新區間。
* **有重疊**：下一個區間起點  守門員終點。動作：更新守門員的終點（取 `max`）。



### 2. 精煉程式碼 (Google 面試推薦版)

這份 Code 採用你剛寫出的邏輯，並加上了必要的語意化註解。

```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # 1. 溝通前置：處理空輸入並進行排序
        if not intervals: return []
        intervals.sort(key=lambda x: x[0]) # O(N log N)
        
        # 2. 初始化結果集，將第一個區間作為起點
        merged = [intervals[0]]

        for i in range(1, len(intervals)):
            current_start, current_end = intervals[i]
            
            # 3. 判斷重疊：利用「排序後」的特性
            if merged[-1][1] < current_start:
                # 情況 A：完全斷開，直接新增
                merged.append(intervals[i])
            else:
                # 情況 B：有重疊或相連，合併邊界
                # 這裡的 max 是靈魂，能正確處理 [1, 10] 包住 [2, 5] 的情況
                merged[-1][1] = max(merged[-1][1], current_end)

        return merged 

```

---

### 3. 面試官的高階 Follow-up (Strong Hire 必備)

在 Google 面試中，寫完程式碼只是開始。面試官通常會拋出以下問題：

* **Q1: 為什麼要用 `max` 而不直接取 `intervals[i][1]`？**
* **關鍵點**：處理「包覆 (Enclosed)」。例如 `[1, 10]` 與 `[2, 3]`，若不取 `max`，終點會從 `10` 縮減為 `3`，導致錯誤。


* **Q2: 如果區間已經排好序，還需要  嗎？**
* **關鍵點**：不需要。直接  掃描即可。這引申出 **LeetCode 57. Insert Interval**，是區間問題的優化考點。


* **Q3: 如何在原地 (In-place) 修改以節省空間？**
* **關鍵點**：可以使用兩個指針，一個負責讀取 `read`，一個負責寫入 `write`，將合併後的結果直接蓋掉原數組前面的空間。



---

### 4. 產業實務案例 (Real-world Applications)

將 LeetCode 連結到現實系統，是展現你具備 Senior 工程師潛力的最好方式：

#### A. 網路封包重組 (Network Packet Reassembly)

* **場景**：TCP 協議中，封包可能亂序抵達或有重複。
* **應用**：接收端會緩存已收到的 Sequence Number 區間（例如 `[1, 100], [101, 200]`）。利用 Merge Intervals 邏輯，當發現所有區間合併後能覆蓋完整的 Data Range，系統才將資料傳給應用層。

#### B. 雲端資源配額管理 (Cloud Resource Quota)

* **場景**：Google Cloud 的用戶預約了多個時段的 GPU。
* **應用**：系統需合併所有預約區間，以判斷「實質佔用時間」，進而計算閒置時間並動態調整電費或自動關閉閒置機器。

#### C. 影音剪輯軟體 (Video Timeline)

* **場景**：在 YouTube 剪輯器中，當你把兩段重疊的背景音樂拖在一起。
* **應用**：後端會使用此演算法合併重疊的音軌區間，以優化渲染引擎的資源調度，避免在同一秒重複解碼兩個相同的音訊流。