### 1. 核心題意與挑戰

設計一個支援以下操作的資料結構：
1. `SnapshotArray(int length)`：初始化一個與指定長度相等的、所有元素初始值為 0 的陣列。
2. `void set(index, val)`：將陣列在 `index` 位置的元素設為 `val`。
3. `int snap()`：獲取該陣列的快照，並返回快照的編號 `snap_id`（從 0 開始遞增）。
4. `int get(index, snap_id)`：返回陣列在給定快照編號 `snap_id` 時的 `index` 元素值。

* **隱藏要求**：陣列長度最高達 $5 \cdot 10^4$，總操作次數也是。如果你在每次 `snap()` 的時候都把整個陣列 `Deep Copy` 一份存起來，絕對會 Memory Limit Exceeded (MLE) 或 Time Limit Exceeded (TLE)。

---

### 2. 解法對比與完整程式碼

#### A. 暴力深層複製 (Deep Copy) —— **面試不及格的雷區**

**思路**：
準備一個巨大的 List of Lists。每次 `snap` 就把整個長度 N 的 Array `copy()` 加進去。
* **缺點**：
  * **空間**：如果 Snap 了 S 次，需要 $O(S \times N)$ 空間。極度浪費，因為每次 Snap 可能只有 1 個元素改變。
  * **時間**：每次 Snap 要複製 N 個元素，$O(N)$。

#### B. 紀錄單點歷史變革 (History per Index + Binary Search) —— **標準時空最佳解**

**思路**：
與其備份「全世界那一刻長怎樣」，我們不如備份「**每個格子各自經歷了怎樣的人生**」。
我們讓每一個 `index` 自己維護一份歷史紀錄表 (A List of History Records)。
結構為：`history[index] = [(snap_id_A, val_A), (snap_id_B, val_B), ...]`。

* **`set` 實作**：
  就在該 `index` 的陣列中，加上一筆 `(目前的全局 snap_id, val)`。如果這個 Snap 世代我們修改了這個格子很多次，我們只要覆寫掉最後一筆就好（因為 Snap 還沒發生）。
* **`snap` 實作**：
  超簡單，只要把全局計數器 `snap_id` 加 1 就好了。時間複雜度 $O(1)$。我們根本不需要去掃描任何陣列！這就是延遲綁定 (Lazy behavior) 的精髓。
* **`get` 實作**：
  拿到指定格子的歷史紀錄陣列。因為這格子被修改的時候，`snap_id` 一定是遞增的，所以**這個歷史紀錄陣列一定是按照 `snap_id` 排序好**的！熟悉的 Binary Search 又來了。找出「小於等於目標 `snap_id` 的最晚一筆歷史紀錄」即為答案。

```python
import bisect

class SnapshotArray:

    def __init__(self, length: int):
        # 每個 index 維護自己的變更歷史
        # 初始狀態：在第 0 世代 (未拍照前) 每格都是 0
        self.history = [[(0, 0)] for _ in range(length)]
        self.curr_snap_id = 0

    def set(self, index: int, val: int) -> None:
        records = self.history[index]
        # 如果最後一筆紀錄就是這個世代打的，代表我們在一次快照前改了這個格子兩次，直接覆蓋
        if records[-1][0] == self.curr_snap_id:
            records[-1] = (self.curr_snap_id, val)
        else:
            # 第一筆這個世代的修改，追加進去
            records.append((self.curr_snap_id, val))

    def snap(self) -> int:
        # 直接進入下一個世代
        self.curr_snap_id += 1
        # 返回的是剛才拍下的那個世代 ID
        return self.curr_snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        records = self.history[index]
        
        # 使用二元搜尋找尋 insertion point
        # 在 Python 中，bisect 是基於 Tuple 的第一個元素 (snap_id) 來比較的
        idx = bisect.bisect_right(records, (snap_id, float('inf')))
        
        # 既然 idx 是剛好大於的，那 idx - 1 就是這期間最新的這筆
        return records[idx - 1][1]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_3 = obj.snap()
# param_4 = obj.get(index,snap_id)
```

---

### 3. 實務應用場景

#### 1. 虛擬機快照與寫入時複製 (Copy-On-Write, COW)
* **應用**：VMware / VirtualBox 照快照時，並不是真的複製 50GB 的硬碟。而是把當下的狀態設為 Read-Only，之後只有「被修改」的區塊才會產生 Fork 紀錄。Snapshot Array 的思想就是 COW 在軟體架構層級的一維實現。

#### 2. 資料庫的多版本並發控制 (MVCC in PostgreSQL/MySQL)
* **應用**：高併發的關聯式資料庫中，為了讓讀取操作不會被寫入操作卡死 (Lock)，通常每一筆 Row 都會存有多個歷史版本 (TxID)。使用者查詢時，會透過自己的 Transaction ID 拿 Binary Search 去找出這筆 Row 對它而言最新、合法可見的那一筆歷史紀錄。

---

### 4. 總結筆記

| | 說明 |
| --- | --- |
| **Why Per-Index History?** | 在資源稀缺的情況下，我們只記錄「隨機微小的增量改變 (Delta)」。如果沒有改變，就省下所有空間。是最佳化軟體必修的思想。 |
| **覆寫同一世代的寫入** | 面試中必須要想到：如果在同一個 Snap 世代內 `set(0, 5)` 又 `set(0, 8)`，這個串列只應該留下一筆 `(id, 8)`。不能放任 Array 無限長大浪費空間。 |