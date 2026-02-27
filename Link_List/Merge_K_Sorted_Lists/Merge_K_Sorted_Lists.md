### 1. 核心題意與挑戰

給定一個包含 `k` 個鏈結串列的陣列 `lists`，其中每個鏈結串列都已經是**升序**排列的。
將所有鏈結串列合併到一個升序鏈結串列中，並返回合併後的鏈結串列。

* **隱藏挑戰**：
  * 面試常見超級魔王題 (Hard)。結合了資料結構（指標操作）與進階演算法（分治或優先佇列）。
  * 如果只有兩個鏈，這就是 `Merge Two Sorted Lists`。但有 `K` 個時，如何避免低效的 $O(K \times N)$ 寫法？

---

### 2. 解法對比與完整程式碼

#### A. 暴力兩兩擊破 (Sequential Merge) —— **可運作但不夠好**

**思路**：
把 `lists[0]` 先跟 `lists[1]` 合併，得到的結果再去跟 `lists[2]` 合併...直到最後一個。
* **缺點**：假設每次合併結果長度逐漸增加，前面的節點會被重複走訪非常多次，時間複雜度高達 $O(K^2 \times N)$。面試中這只能算是不及格的妥協。

#### B. 優先佇列 (Min-Heap) —— **思維最直觀的最佳解**

**思路**：
每個串列都已排序，所以**全域的最小值一定出現在某一個串列的第一個節點**。
我們維護一個容量為 `k` 的最小堆疊 (Min-Heap)。
首先，將每個串列的**頭節點**丟入 Heap 裡。
然後，每次從 Heap 彈出最小的節點加入新串列的尾端，如果這個彈出的節點後面還有節點，就把它的**下一個節點**放入 Heap，填補剛才的空缺。
如此循環直到 Heap 為空。

* **優點**：非常容易理解，擴展性強（適合大規模串流合併）。Python 的 `heapq` 模組可以完美實現。

```python
from typing import List, Optional
import heapq

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        # 需要包裝一層 wrapper，因為 ListNode 類沒實作 __lt__ 比較大小
        # 第二個元素放的是 idx 用來區分同 value 的 tie-breaker
        min_heap = []
        
        # 1. 每個串列的第一個節點進 Heap
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(min_heap, (l.val, i, l))
                
        dummy = ListNode()
        tail = dummy
        
        # 2. 只要 Heap 非空，彈出最小的，再把接續的節點推進去
        while min_heap:
            val, i, node = heapq.heappop(min_heap)
            tail.next = node
            tail = tail.next
            
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))
                
        return dummy.next
```

#### C. 分治法大躍進 (Divide and Conquer) —— **不需額外記憶體的終極解法**

**思路**：
模仿 Merge Sort 的精神，將 `k` 個串列兩兩配對合併。
第一輪：`0與1`合併，`2與3`合併... 剩下 `k/2` 個。
第二輪：再繼續兩兩合併，剩下 `k/4` 個。
反覆這個過程直到只剩下 `1` 個。
由於每一次大合併都是平衡的，這種方式也保證了效能。

* **時間複雜度**：$O(N \log K)$ ($N$ 是所有節點總數)
* **空間複雜度**：$O(1)$。不需 Heap 的額外空間。

```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
            
        # 重用 `Merge Two Sorted Lists` 作為輔助函數
        def mergeTwo(l1, l2):
            dummy = tail = ListNode()
            while l1 and l2:
                if l1.val < l2.val:
                    tail.next, l1 = l1, l1.next
                else:
                    tail.next, l2 = l2, l2.next
                tail = tail.next
            tail.next = l1 or l2
            return dummy.next
            
        # 兩兩合併的迴圈
        while len(lists) > 1:
            merged_lists = []
            
            # 一次跳兩步，配對相鄰的串列
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                # 奇數長度時最後一個會落單
                l2 = lists[i+1] if (i+1) < len(lists) else None
                merged_lists.append(mergeTwo(l1, l2))
                
            lists = merged_lists # 將配對合併好的結果覆蓋原清單
            
        return lists[0]
```

---

### 3. 實務應用場景

本題完美呼應大數據領域中的核心演算法精神：

#### 1. 分散式資料庫的 K-way Merge (MapReduce)
* **應用**：當系統要把查詢任務發派給 100 台獨立的資料庫節點，每台節點回傳的都是自己排好序的百萬條查詢結果，發號施令的主節點 (Manager) 就要使用 Min-Heap 的 K-way merge 將這 100 股資料流交織輸出給前端，完全不需要把所有資料一次扛進記憶體。

#### 2. K-way 合併排序 (External Sorting on Files)
* **應用**：有 50GB 的資料要被排序，但記憶體只有 8GB。系統會先把資料切成數個 8GB 的 Chunk 單獨在記憶體裡排好並寫回硬碟（這變成 K 個 Sorted lists）。最後的合併階段就是在外存 (Disk) 反覆讀取每個 Chunk 的「下一個元素」出來進行比較的過程。

---

### 4. 總結筆記

| 比較維度 | Sequential Merge | Min-Heap | Divide & Conquer |
| --- | --- | --- | --- |
| **時間複雜度** | $O(K \times N)$ | $O(N \log K)$ ($N$ 為總節點數) | $O(N \log K)$ |
| **空間複雜度** | $O(1)$ | $O(K)$ (給 Heap 存指標) | $O(1)$ 若不計遞迴/陣列替補 |
| **最佳使用時機** | 千萬別寫這個 | **流式處理 (Streaming) 的最優解** | **純記憶體指標操作的最優解** |
| **容易犯錯** | TLE 超時 | 忘記 Python 實作 class 比較的 Tuple 衝突 `(val, i, node)` | 外層迴圈界線問題 (Index Out of Bounds) |
