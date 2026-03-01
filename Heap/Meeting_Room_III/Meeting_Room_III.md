### 1. 題目敘述與抽象概念

* **題目簡述**：給定 `n` 個會議室與一連串會議 `meetings[i] = [start, end]`。規則是：(1) 優先分配編號最小的空閒會議室；(2) 若無空閒會議室，會議被**延遲**至最早有空的房間，且持續時長不變；(3) 回傳舉辦過**最多**會議的會議室編號。
* **抽象概念**：帶有**等待佇列**與**優先級分配**的時間軸模擬問題。在資源有限的情況下，如何最優地排程與等待。
* **標籤 (Tag)**：`Array`、`Sorting`、`Heap (Priority Queue)`、`Simulation`。

---

### 2. 演算法比較（面試評級）

| 比較維度 | 暴力陣列掃描 (Brute Force) | 雙優先佇列 (Two Heaps) |
| --- | --- | --- |
| **核心思路** | 維護長度 $N$ 的 `roomEndTimes` 陣列，每次用 $O(N)$ 迴圈尋找可用或最早結束的房間 | 維護兩個 Heap：一個管空閒房間，一個管進行中的會議 |
| **時間複雜度** | $O(M \log M + M \cdot N)$ | $O(M \log M + M \log N)$ |
| **空間複雜度** | $O(N)$ | $O(N)$ |
| **瓶頸所在** | 尋找可用房間的 $O(N)$ 線性掃描 | 無，Heap 操作為 $O(\log N)$ |
| **面試評級** | **Lean Hire**：邏輯正確，但效率不足 | **Strong Hire**：完美利用 Heap 特性 |

---

### 3. 核心 Edge Case 剖析

**當沒有空房間時，延遲計算不能用 `end`，要用 `oldEndTime + duration`。**

```
會議室 A：正在進行，將在 t=10 結束
新會議：[start=5, end=8]，duration = 3
```

* **錯誤思路**：新的結束時間 = `end = 8` ❌（8 比 10 還早，邏輯矛盾）
* **正確思路**：新的結束時間 = `oldEndTime + duration = 10 + 3 = 13` ✅

---

### 4. 雙優先佇列解法：逐行解析

```python
import heapq

class Solution:
    def mostBooked(self, n: int, meetings: list[list[int]]) -> int:

        meetings.sort()

        availableRooms = list(range(n))  # Min-Heap：空閒房間（by 編號）
        heapq.heapify(availableRooms)

        ongoingMeetings = []             # Min-Heap：[endTime, roomNumber]
        count = [0] * n

        for start, end in meetings:
            duration = end - start

            # 將所有在 start 之前已結束的會議室釋放回 availableRooms
            while ongoingMeetings and ongoingMeetings[0][0] <= start:
                endTime, room = heapq.heappop(ongoingMeetings)
                heapq.heappush(availableRooms, room)

            if availableRooms:
                # 有空房間：分配編號最小的房間
                room = heapq.heappop(availableRooms)
                heapq.heappush(ongoingMeetings, [end, room])
            else:
                # 無空房間：延遲會議，等最早結束的房間
                endTime, room = heapq.heappop(ongoingMeetings)
                newEnd = endTime + duration
                heapq.heappush(ongoingMeetings, [newEnd, room])

            count[room] += 1

        return count.index(max(count))
```

**兩個 Heap 的語意：**

| Heap | 儲存內容 | 排序依據 | 語意 |
| --- | --- | --- | --- |
| `availableRooms` | 房間編號 | 編號最小優先 | 「我現在有空，請分配我」 |
| `ongoingMeetings` | `[endTime, roomNumber]` | 結束時間最早優先 | 「我何時最快能空出來？」 |

---

### 5. 微系統設計應用 (Micro-System Design)

這正是**雲端運算資源調度（Cloud Computing Instance Allocation）**的縮影：

* **$N$ 台 Worker Node** ↔ $N$ 個會議室
* **運算任務湧入** ↔ 會議按 start 時間抵達
* **優先分配低編號節點** ↔ 減少開機碎片化、節省跨節點通訊成本
* **任務等待佇列** ↔ 無空房時的延遲機制，確保任務**不遺失**

這與 GCP / AWS 的 **Spot Instance 排程器**設計原理完全一致。

---

### 6. Follow-up 延伸追問

**追問 1：如果會議可以中途動態取消（Cancel），如何設計？**

> 考驗 **Lazy Deletion（延遲刪除）**。Heap 不支援隨機刪除，因此：
> 1. 用 `HashMap` 記錄每個會議的取消狀態。
> 2. 當 Heap 彈出該會議時，若發現已被取消，直接丟棄（不放回 `availableRooms`）。
> 3. 這犧牲了 $O(1)$ 的確認成本，但避免了 $O(N)$ 的堆重建。

**追問 2：如果會議有優先權（Priority），高優先權可以插隊怎麼辦？**

> 需要引入第三個資料結構：`waitingQueue`（Max-Heap by Priority）。
> 當有房間空出時，優先從 `waitingQueue` 取出優先權最高的等待會議，而非按照 FIFO 順序。

**追問 3：與 Meeting Rooms II (LC 253) 的核心差異？**

| | LC 253 Meeting Rooms II | LC 2402 Meeting Rooms III |
| --- | --- | --- |
| **問題目標** | 最少需要幾間房？ | 最多會議的房間是哪間？ |
| **關注點** | 峰值並發數 | 分配策略 + 延遲模擬 |
| **核心工具** | 單 Heap（結束時間） | 雙 Heap（空閒編號 + 結束時間）|
| **有無延遲** | 無 | 有（資源滿載時） |

---

「這題的精髓在於用**兩個 Heap 分別管理兩種狀態**：空閒的房間與進行中的會議。透過即時從 `ongoingMeetings` 釋放到 `availableRooms`，我們用 $O(\log N)$ 取代了 $O(N)$ 的線性掃描。最關鍵的 Edge Case 是：延遲會議的新結束時間必須是 `舊結束時間 + 持續時長`，而非原本的 `end`。」
