### LeetCode 1146. Snapshot Array 學習筆記

---

#### 1. 題目敘述與抽象概念

* **題目簡述**：設計一個支援「多版本管理」的陣列。除了基礎的 `set(index, val)` 與 `get(index)`，核心功能是 `snap()`。每次呼叫 `snap()` 都會產生一個目前狀態的存檔點，並回傳一個遞增的 `snap_id`。隨後呼叫 `get(index, snap_id)` 必須能精準回傳該版本時該索引的值。
* **抽象概念**：
* **版本控制 (Version Control)**：這是一種類似 Git 的設計。
* **寫入時複製 (Copy-on-Write, COW)**：只有在資料發生變動時才記錄，避免冗餘的空間浪費。
* **時空權衡 (Space-Time Trade-off)**：放棄儲存完整快照，改為儲存「變更日誌」，並透過二分搜尋在查詢時找回狀態。


* **題型標籤 (Tags)**：`Array`, `Hash Table`, `Binary Search`, `Design`

---

#### 2. 算法比較與複雜度分析

| 算法 | `set` 複雜度 | `snap` 複雜度 | `get` 複雜度 | 空間複雜度 | 評價 |
| --- | --- | --- | --- | --- | --- |
| **暴力複製 (Naive Copy)** |  |  |  |  | **Fail**：快照次數多時會造成記憶體崩潰 (MLE)。 |
| **全量記錄 (History Log)** |  |  |  |  | **Lean Hire**：線性查找歷史記錄，查詢效率低。 |
| **二分搜尋歷史 (Optimized)** |  |  |  |  | **Strong Hire**：兼顧寫入與查詢效率。 |

*(註： 為陣列長度， 為快照次數， 為 `set` 操作的總次數)*

---

#### 3. 微系統設計與產業應用

在微系統設計或實際後端架構中，此算法的邏輯可應用於：

* **資料庫 MVCC (Multi-Version Concurrency Control)**：如 PostgreSQL 或 MySQL InnoDB。當一筆資料被修改時，系統不會直接覆蓋，而是保留舊版本，讓其他正在執行的 Transaction 能讀取到一致的「快照」內容，實現非阻塞讀取。
* **分散式儲存系統的 Snapshot**：在雲端儲存（如 AWS EBS 或 Google Cloud Storage）中，快照是透過記錄 **Block 級別的增量更新** 來實現的，這與本題「只在對應 index 的 list 增加記錄」的行為完全一致。
* **撤銷/重做系統 (Undo/Redo)**：軟體編輯器中的歷史記錄管理。

---

#### 4. Following up 延伸題型

* **延伸題目 1：LeetCode 981. Time Based Key-Value Store**
* **關聯**：與本題邏輯幾乎相同，只是將 `index` 換成 `key`，將 `snap_id` 換成 `timestamp`。


* **延伸題目 2：Persistent Segment Tree (可持久化線段樹)**
* **關聯**：如果題目要求在 `set` 之後還要能基於某個快照進行「修改」並派生出新的分支，二分搜尋就不夠用了，需要使用函數式資料結構（Functional Data Structure）。


* **微系統設計 Follow-up**：
* 如果快照數量多到單機記憶體放不下，該如何設計分散式快照系統？（關鍵點：Consistency Hashing, Sharding by Index, LSM-tree 結構化儲存）。
* 如何實作「刪除過舊快照」的機制來回收空間？（TTL 與背景 Compaction 流程）。