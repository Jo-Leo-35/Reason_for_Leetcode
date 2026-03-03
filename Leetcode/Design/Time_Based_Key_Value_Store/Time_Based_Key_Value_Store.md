### 1. 核心題意與挑戰

設計一個基於時間的鍵值存儲系統 (Time-Based Key-Value Store)，該系統支援為同一鍵在不同時間戳記下存儲多個值。
這代表除了 `key` 和 `value`，還有第三個維度：`timestamp`。
實作兩個方法：
1. `set(key, value, timestamp)`：儲存鍵 `key`、值 `value`，以及給定時間戳 `timestamp`。
2. `get(key, timestamp)`：返回鍵 `key` 在之前時間（即 `prev_timestamp <= timestamp`）的最新值。如果在 `timestamp` 之前沒有對應的值，返回空字串 `""`。

* **隱藏前提**：題目保證所有的 `set` 操作，其 `timestamp` 都是**嚴格遞增的**。也就是說寫入永遠都是往未來的時間寫，不會有「回溯寫入歷史」的情況發生。這點極其重要！

---

### 2. 解法對比與完整程式碼

#### 唯一正解：雜湊表 + 二元搜尋 (HashMap + Binary Search)

**思路**：
因為寫入的時間戳一定是**遞增的**，所以如果我們把同一個 `key` 的所有 `(timestamp, value)` 存成一個 Python `List`，這個 List 自然而然就已經是**按照時間排序好**的陣列了！
這太棒了，看到「已經排序好的陣列」加上「尋找小於等於目標的最大值」，這明顯就是為 **Binary Search (二元搜尋)** 量身打造的場景。

* **資料結構設計**：
  使用 `collections.defaultdict(list)`。
  結構長這樣：`store["foo"] = [(1, "bar"), (4, "bar2"), (5, "bar3")]`

* **`set` 實作**：
  直接 `store[key].append((timestamp, value))`。時間複雜度 $O(1)$。

* **`get` 實作**：
  拿到該 `key` 的陣列。用二元搜尋尋找 `timestamp`。
  如果找到完全匹配的，太好了直接回傳。
  如果沒找到，我們必須回傳**最後一個比 `timestamp` 小**的那個記錄。

* **空間複雜度**：$O(N)$，儲存所有的 Set 請求。

```python
from collections import defaultdict
import bisect

class TimeMap:

    def __init__(self):
        # 初始化字典，裡面存 tuple(timestamp, value) 的陣列
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
            
        values = self.store[key]
        
        # 邊界處理：如果要求尋找的時間比我們歷史上最早的一筆還要小，代表那時候根本沒這東西
        if timestamp < values[0][0]:
            return ""
            
        # 使用二元搜尋找尋 insertion point
        # 在 Python 中，bisect 是基於 Tuple 的第一個元素來比較的
        # 為了要比大小，我們故意偽造一個 tuple
        # bisect_right 會找到「第一個嚴格大於目標值」的位置
        idx = bisect.bisect_right(values, (timestamp, chr(127)))
        
        # 既然 idx 是第一個大於目標的，那 idx - 1 就是這期間最新的這筆！
        return values[idx - 1][1]
        
        ''' 
        如果不熟悉 bisect，手刻 Binary Search 的版本：
        left, right = 0, len(values) - 1
        res = ""
        while left <= right:
            mid = left + (right - left) // 2
            if values[mid][0] == timestamp:
                return values[mid][1]
            elif values[mid][0] < timestamp:
                res = values[mid][1]
                left = mid + 1
            else:
                right = mid - 1
        return res
        '''

# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
```

---

### 3. 實務應用場景

本題就是**時序型資料庫 (Time-Series Database, TSDB)** 的超級微縮版原型。

#### 1. 監控系統與度量引擎 (Metrics Engine - Prometheus / Grafana)
* **應用**：蒐集伺服器 CPU 使用率。當用戶在前端畫圖表時拉了一條 X 軸，你必須回傳每一秒的狀態，即便那一秒系統沒有主動回報數字，你也必須透過 Binary Search 往前回推拿到上一筆最近的採樣資料。

#### 2. 遊戲伺服器的狀態回滾防作弊 (Lag Compensation in FPS Games)
* **應用**：在《CS:GO》或《Apex》這種射擊遊戲中，伺服器必須保存所有玩家過去 1 秒鐘內每 0.01 秒的物理坐標。當玩家 A 送出「我在 t=150 毫秒時開槍打中玩家 B」的封包時，伺服器必須調閱歷史記錄 `get(PlayerB, 150)` 來重現 150 毫秒那瞬間 B 的位置，這就是嚴格的時間軸調閱機制。

---

### 4. 總結筆記

| | 解說 |
| --- | --- |
| **Why not Dict of Dicts?** | 如果寫 `store["foo"][150] = "bar"`，雖然 $O(1)$。但當有人查 `151` 甚至 `200` 時，你無法輕鬆找到離他最近的前面那筆，因為 HashMap 的 Key 是無序的。只能用排序 Array 幫忙。 |
| **`bisect_right` 與 Fake Tuple** | 為了相容 tuple comparison，必須構造一個 `(timestamp, 非常大的字元)` 以確保二分搜順利推進到最右邊。如果是面試，建議寫下方註解裡**手刻的 Binary Search** 會顯得更能掌握細節。 |
