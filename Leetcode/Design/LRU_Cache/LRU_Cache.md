### 1. 核心題意與挑戰

設計一個符合 **LRU（Least Recently Used，最近最少使用）** 策略的快取資料結構。

* **關鍵限制**：`get` 與 `put` 都必須在 **O(1)** 時間內完成。
* **隱藏挑戰**：要同時做到「O(1) 查找」與「O(1) 順序調整」，單一資料結構無法辦到，必須組合兩種結構。

---

### 2. 解法對比與完整程式碼

#### A. 雙向鏈結串列 + HashMap —— **推薦面試解法**

**思路**：
* **HashMap** (`dict`): `key -> Node`，負責 O(1) 查找節點。
* **Doubly Linked List**: 維護使用順序，Head 端 = 最近使用，Tail 端 = 最久未使用。
* 兩個 **Dummy 節點**（head/tail）作為哨兵，避免操作時的邊界判斷。

每次 `get` 或 `put`，將對應節點移到 Head 端；容量超限時，驅逐 Tail 端節點。

* **優點**：`get`/`put` 均為嚴格 O(1)，完全符合題目要求。
* **缺點**：需要手動管理 4 條指針，容易出錯，需要謹慎實現。

```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = Node()  # dummy head (最近使用端)
        self.tail = Node()  # dummy tail (最久未使用端)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

#### B. Python OrderedDict —— **快速實現（不推薦作為主要答案）**

**思路**：`OrderedDict` 內建維護插入順序，`move_to_end()` 可 O(1) 移動元素，`popitem(last=False)` 可 O(1) 移除最舊元素。

* **優點**：程式碼極為簡潔，不易出錯。
* **缺點**：依賴 Python 標準庫，面試官通常會要求你解釋或手動實現底層邏輯。

```python
from collections import OrderedDict

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

---

### 3. 實務應用場景

LRU Cache 不只是刷題，在工業界幾乎無處不在：

#### 1. CPU / 記憶體分頁快取 (CPU L1/L2/L3 Cache)

* **應用**：作業系統的虛擬記憶體管理，決定哪些分頁（Page）可以被置換到磁碟。
* **實現**：LRU 是最常見的分頁置換演算法之一。當 RAM 不足時，驅逐最久未被訪問的分頁。

#### 2. 資料庫查詢快取 (Database Buffer Pool)

* **應用**：MySQL InnoDB、PostgreSQL 的 Buffer Pool，快取磁碟上的資料頁（Data Page）。
* **實現**：熱門查詢結果常駐記憶體，冷門的被驅逐回磁碟，大幅減少 I/O 次數。

#### 3. CDN / 反向代理快取 (Nginx, Varnish)

* **應用**：快取靜態資源（圖片、JS、CSS），減少回源請求。
* **實現**：LRU 策略決定哪些資源繼續留在快取，哪些被新內容取代。

#### 4. 行動 App 圖片快取 (Glide, Picasso on Android)

* **應用**：App 快取已下載的圖片，避免重複網路請求，節省流量。
* **實現**：使用 LRU 策略管理記憶體中的 Bitmap 快取，當記憶體不足時自動驅逐最舊的圖片。

---

### 4. 總結筆記

| 比較維度 | 雙向鏈結串列 + HashMap | OrderedDict |
| --- | --- | --- |
| **get 效能** | **O(1)** | **O(1)** |
| **put 效能** | **O(1)** | **O(1)** |
| **空間** | O(capacity) | O(capacity) |
| **面試適合度** | **極佳**（展現底層理解） | **普通**（需補充解釋） |
| **推薦語** | 標準答案，展示你對指針操作與資料結構設計的掌握。 | 作為 follow-up 提及，表示你熟悉語言特性。 |

**關鍵實現細節（易錯點）**：
1. **Dummy 節點**：head 和 tail 永遠不存真實資料，省去大量邊界判斷。
2. **put 的順序**：先移除舊節點再建立新節點，最後才驅逐 LRU，順序不能錯。
3. **驅逐時先取 key**：`lru = self.tail.prev` → `del self.cache[lru.key]`，必須在 `_remove` 之前取好 key，否則斷鏈後找不回來。
