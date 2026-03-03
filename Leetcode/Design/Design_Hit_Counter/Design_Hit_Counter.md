### 1. 核心題意與挑戰

設計一個系統統計過去 300 秒內的點擊次數。

* **關鍵限制**：`timestamp` 遞增，同一秒可能有多個 `hit`。
* **隱藏挑戰**：在高流量下如何節省空間？如何確保 `getHits` 的效率？

---

### 2. 解法對比與完整程式碼

#### A. 環狀陣列解法 (Circular Buffer) —— **推薦面試解法**

**思路**：利用 `timestamp % 300` 將時間映射到固定大小的陣列。當指針繞回時，若時間戳不同，代表舊數據過期，直接覆蓋。

* **優點**： 寫入、 查詢，**空間固定 **。
* **缺點**：無法查詢歷史數據，過期即丟失。

```python
class HitCounter:
    def __init__(self):
        self.size = 300
        self.times = [0] * self.size
        self.counts = [0] * self.size

    def hit(self, timestamp: int) -> None:
        idx = timestamp % self.size
        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.counts[idx] = 1
        else:
            self.counts[idx] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(self.size):
            if timestamp - self.times[i] < 300:
                total += self.counts[i]
        return total

```

#### B. 分桶雜湊解法 (Bucketing with Hashmap) —— **適合歷史查詢**

**思路**：將時間切成 300 秒一個大桶。查詢時只找「當前桶」與「上一個桶」，並清理更早之前的數據。

* **優點**：具備**時序資料庫**雛形，若取消清理邏輯，可支持歷史隨機查詢。
* **缺點**：Hashmap 有額外記憶體開銷，遍歷 Key 的效率略低於陣列。

```python
from collections import defaultdict

class HitCounter:
    def __init__(self):
        # bucket_id -> { timestamp -> count }
        self.timemap = defaultdict(lambda: defaultdict(int))

    def hit(self, timestamp: int) -> None:
        bucket = timestamp // 300
        self.timemap[bucket][timestamp] += 1

    def getHits(self, timestamp: int) -> int:
        bucket = timestamp // 300
        # 主動清理機制：保留最近兩個區間，刪除其餘
        for old_id in list(self.timemap.keys()):
            if old_id < bucket - 1:
                del self.timemap[old_id]

        total = 0
        # 遍歷當前與上一個桶子的 keys
        for b_id in [bucket, bucket - 1]:
            if b_id in self.timemap:
                for t, cnt in self.timemap[b_id].items():
                    if timestamp - t < 300:
                        total += cnt
        return total

```

---

### 3. 實務應用場景

這套演算法不只是刷題，在實際工業界有極廣的應用：

#### 1. API 限流器 (Rate Limiter)

* **應用**：防止惡意爬蟲或 DDoS。
* **實現**：使用 Circular Buffer 統計每個 User ID 在過去 1 分鐘內的 Request 數，超過閾值則回傳 `429 Too Many Requests`。

#### 2. 系統監控與報警 (Monitoring)

* **應用**：監控伺服器的錯誤率。
* **實現**：每秒記錄錯誤次數，若過去 5 分鐘內錯誤數（`getHits`）超過 10%，自動發送 Slack/郵件告警。

#### 3. 影片熱度即時統計 (YouTube/TikTok)

* **應用**：顯示影片「過去 1 小時觀看人數」。
* **實現**：你的 **Bucketing 思路** 就派上用場了。我們會將數據分桶存入 Redis，不同機器的 Hit 先在本地聚合後，再非同步更新到全域計數器。

#### 4. 電商促銷防刷 (Anti-Fraud)

* **應用**：防止秒殺活動中同一帳號瞬間下單萬次。
* **實現**：滑動窗口檢查該 IP 的下單頻率。

---

### 4. 總結筆記

| 比較維度 | Circular Buffer | Hashmap Bucketing |
| --- | --- | --- |
| **記憶體** | **優** (固定分配) | **良** (動態增減) |
| **寫入效能** | **極快** (O(1)) | **快** (O(1) average) |
| **查詢效能** | **穩定** (O(300)) | **視點擊密度而定** |
| **擴展性** | 僅限滑動窗口 | **可擴展為歷史查詢** |
| **推薦語** | 追求單機效能與記憶體極限時使用。 | 需求可能變更（如查歷史）或分散式系統分片時使用。 |