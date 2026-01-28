### 1. 題目敘述與抽象概念

* **題目簡述**：給定一系列會議時間區間 `intervals[i] = [start, end]`，求最少需要多少間會議室才能容納所有會議（即解決重疊問題）。
* **抽象概念**：找出時間軸上的**「最大併發重疊數」**。這是一個典型的「區間覆蓋」問題，我們要求的是在任何一個時刻，同時存在的區間數量的最大值。
* **標籤 (Tag)**：`Sweep Line (掃描線)`、`Heap (堆積)`、`Greedy`、`Sorting`。

---

### 2. 算法比較（Google 面試評級）

| 比較維度 | 最小堆積 (Min-Heap) | 掃描線 (Sweep Line) |
| --- | --- | --- |
| **核心邏輯** | 維護一個動態清單，紀錄「目前所有房間中最快結束的時間」。 | 將所有「開始」與「結束」拆解成獨立事件，按時間排序。 |
| **時間複雜度** |  |  |
| **空間複雜度** | （ 為最大併發數） | （需儲存所有端點） |
| **物理意義** | **資源重用**：新會議進來時，看有無舊房可進。 | **流量監控**：計算瞬間水位的淨變化量。 |
| **Google 評價** | **Strong Hire** (適合處理 Streaming 數據) | **Strong Hire** (邏輯最優雅且通用) |

---

### 3. 掃描線算法 (Sweep Line) 的物理意義

此算法將「區間」抽象化為兩個**「觸發事件」**：

1. **`(start, 1)`**：**資源請求事件**。有人進場，計數器 `+1`。
2. **`(end, -1)`**：**資源釋放事件**。有人離場，計數器 `-1`。

* **排序的物理意義**：模擬時間線的流逝。
* **`-1` 優先於 `1` 的意義**：當 A 會議結束時間與 B 會議開始時間相同時（如 10:00），我們先讓 A 走（`-1`），再讓 B 進（`+1`），這確保了在 10:00 這一瞬間，房間數不會虛高。
* **`max_rooms` 的意義**：記錄歷史上的**「最高水位（Peak Capacity）」**，即為所需的最少房間數。

---

### 4. 精通級 Python 模板 (掃描線版)

```python
class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
        
        # 1. 溝通前置：將區間拆解為具語意的事件點
        # 使用 1 代表進場，-1 代表離場
        events = []
        for start, end in intervals:
            events.append((start, 1))
            events.append((end, -1))
        
        # 2. 排序：優先排時間；時間相同時，-1 (結束) 會排在 1 (開始) 前面
        events.sort()
        
        max_rooms = 0
        current_rooms = 0
        
        # 3. 掃描時間軸 (Dry Run 核心)
        for time, change in events:
            current_rooms += change
            # 主動驗證：隨時紀錄最高水位
            max_rooms = max(max_rooms, current_rooms)
            
        return max_rooms

```

---

### 5. 微系統設計與產業應用

* **雲端運算 (Serverless Scaling)**：
在 Google Cloud Functions 中，系統需要根據請求的「開始時間」與「執行時長」來決定要啟動多少個實體容器（Instances）。這就是 Meeting Rooms II 的變體。
* **網路頻寬調度**：
計算在特定時段內，所有併發下載任務所需的總頻寬，以確保骨幹網路不會因瞬時流量過載（Peak Traffic Management）。

---

### 6. Follow-up 延伸題目

1. **如果數據量太大 (TB 等級)**：討論使用 **Bucket Sort** 或 **差分陣列 (Difference Array)** 來優化排序開銷。
2. **分配房間 ID**：不僅要數量，還要輸出會議 A 在 Room 1、會議 B 在 Room 2。
* *提示*：此時必須回到 **Min-Heap** 解法，並搭配一個 `available_room_ids` 的 Heap 來分配 ID。


3. **LeetCode 1094. Car Pooling**：這題是本題的直接變體，將 `1` 換成 `num_passengers` 即可。

---
「這題的精髓在於將**時間段**轉化為**事件流**。透過 `(time, change)` 的排序，我們能優雅地處理邊界重疊問題，並利用一次線性掃描找到系統的峰值需求。這種掃描線思想是處理所有區間重疊問題的核心模板。」