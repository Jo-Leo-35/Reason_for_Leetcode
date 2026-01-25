### 1. 題目敘述與抽象概念

* **題目簡述**：給定  個已排序的鏈表，將其合併成一個新的排序鏈表。
* **抽象概念**：**多路歸併 (Multi-way Merge)**。
* **核心思維**：想像有  條輸送帶，每條帶子最前面的元素就是該隊伍的「代表」。我們利用 **Min Heap (最小堆積)** 當作擂台，每次選出最弱的（最小的）進入結果，並請該隊伍派下一位代表補位。
* **Tag (題型)**：`Linked List` (鏈表), `Heap / Priority Queue` (堆積), `Merge Sort` (歸併思想).

---

### 2. 算法比較與複雜度分析

| 算法 | 時間複雜度 | 空間複雜度 | 適合場景 |
| --- | --- | --- | --- |
| **暴力排序 (Collect all & Sort)** |  |  | 數據量小，不需考慮鏈表特性時。 |
| **Min Heap (本次實作)** |  |  | **Google 最愛考**，適合處理 Data Stream。 |
| **分治法 (Divide & Conquer)** |  |  | 空間優化極致，適合大數據分散式合併。 |

>  為總節點數， 為鏈表個數。

---

### 3. 微系統設計：外部排序 (External Sort)

在現實系統中，這個算法不只是刷題，它是 **資料庫引擎** 的基礎：

* **應用場景**：當你有 1TB 的日誌檔案需要排序，但記憶體（RAM）只有 8GB。
* **實作流程**：
1. 將 1TB 切成 125 個 8GB 的檔案，分別排序後存回硬碟（Sorted Runs）。
2. 開啟這 125 個檔案的輸入流，並建立一個 Size 為 125 的 **Min Heap**。
3. 利用你的 `mergeKLists` 邏輯，不斷彈出最小值寫入結果檔案，並從對應檔案讀取下一個數補入 Heap。
4. 這就是 **Google BigTable** 或 **RocksDB** 在做背景合併 (Compaction) 的核心邏輯。



---

### 4. 關鍵程式碼與 Dry Run (Python)

```python
# 核心精華：(數值, 索引, 節點)
# 索引 idx 是為了避免兩個節點 val 相同時，Python 嘗試去比較 Node 物件
heapq.heappush(minheap, (node.val, idx, node))

```

#### **變數追蹤 (Dry Run)**

假設 `lists = [[1, 4], [1, 3]]`

1. **Init Heap**: `[(1, 0, Node1), (1, 1, Node1)]`
2. **Pop (1, 0)**: `current` 接上 `L1[0]`，Heap 補入 `(4, 0, Node4)`。
3. **Pop (1, 1)**: `current` 接上 `L2[0]`，Heap 補入 `(3, 1, Node3)`。
* *注意：此時 Heap 裡是 `[(3, 1, Node3), (4, 0, Node4)]*`


4. **Pop (3, 1)**: `current` 接上 `L2[1]`，L2 結束，不補入。
5. **Pop (4, 0)**: `current` 接上 `L1[1]`，結束。

---

### 5. Follow-up 延伸題型

* **Q1: 如果不能用額外資料結構 (Heap) 怎麼辦？**
* 使用 **Divide and Conquer**：兩兩合併鏈表，類似 Merge Sort 的合併階段。


* **Q2: 如果  非常大，但每個 List 只有 1 個元素？**
* 這時 ，複雜度變成 ，這就退化成一般排序。


* **Q3: 如果要找第 K 小的元素？**
* 參考 **LeetCode 378. Kth Smallest Element in a Sorted Matrix**，概念完全一樣，只是不需要接成鏈表。
