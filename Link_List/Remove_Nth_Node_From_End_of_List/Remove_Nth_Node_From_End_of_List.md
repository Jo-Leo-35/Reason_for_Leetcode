### 1. 核心題意與挑戰

給定一個鏈結串列，刪除鏈結串列的倒數第 `n` 個節點，並且返回鏈結串列的頭節點。

* **隱藏挑戰**：
  * 面試官一定會問：你能用**一次走訪 (One Pass)** 完成嗎？（也就是不能先遍歷一次求長度，再遍歷一次去刪除）。
  * 如果要刪除的是第一個節點（即 `head`），如何優雅地處理，而不寫一堆 `if/else` 邊界防護？

---

### 2. 解法對比與完整程式碼

#### A. 基礎解法 —— 兩次走訪 (Two Passes)

**思路**：
最直白的思路：先花 $O(N)$ 走訪一次找出鏈結總長度 `L`，然後再從頭走 `L - n - 1` 步找到要刪除節點的**前一個**節點，將它的 `next` 指向 `next.next`。

* **優點**：思路無壓力。
* **缺點**：面試官覺得你還沒有掌握雙指針的精髓。

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # 建立 dummy_node 處理刪除頭節點的例外狀況
        dummy = ListNode(0, head)
        
        # 1. 計算總長度
        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next
            
        # 2. 找到倒數 n 的前一個節點，也就是走 length - n 步
        curr = dummy
        for _ in range(length - n):
            curr = curr.next
            
        # 刪除
        curr.next = curr.next.next
        
        return dummy.next
```

#### B. 雙指針法 (Two Pointers / Fast & Slow) —— **高頻面試最佳解 (One Pass)**

**思路**：
利用距離差：
如果我們有一個 `fast` 指針先走 `n` 步。那麼 `fast` 跟 `slow` 指針之間就差了 `n` 個節點。
接著讓 `fast` 和 `slow` **同時**往前走。當 `fast` 走到鏈結串列的盡頭 (Null) 時，`slow` 剛好就會位在距離終點 `n` 步的地方，也就是我們要刪除的目標！

為了方便刪除，我們要讓 `slow` 停在被刪除目標的**前一個**節點，所以 `fast` 可以多走一步，或者初始時把兩者放在 `dummy` 節點。

* **優點**：只需要遍歷一次，時間複雜度 $O(N)$，空間 $O(1)$，程式碼洗鍊。

```python
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Dummy Node 是處理刪除類問題的萬靈丹
        dummy = ListNode(0, head)
        left = dummy
        right = dummy
        
        # 1. right 先走 n 步
        for _ in range(n):
            right = right.next
            
        # 2. right 和 left 一起走，直到 right 到達鏈的最後一個實體節點
        while right and right.next:
            right = right.next
            left = left.next
            
        # 3. 此時 left 的下一個節點就是要被刪除的節點
        left.next = left.next.next
        
        return dummy.next
```

---

### 3. 實務應用場景

#### 1. 固定大小的緩衝區 (Fixed Size Sliding Window)
* **應用**：用於監聽日誌串流時，需要隨時過濾掉「過去 N 分鐘前」或是「倒數 N 筆」的舊資料。用固定距離的雙指針可以在 $O(1)$ 時間複雜度下維護這段窗口。

#### 2. 快取丟棄策略 (Cache Eviction)
* **應用**：在手刻 LRU (Least Recently Used) 快取時，有時需要從 Double Linked List 的尾端將過期的節點抹除。

---

### 4. 總結筆記

| 比較維度 | Two Passes (兩次走訪) | Two Pointers (雙指針一次走訪) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ (只走一趟) |
| **空間複雜度** | $O(1)$ | $O(1)$ |
| **Dummy Node** | 必須使用才能省心 | 必須使用才能省心 |
| **雙指針精神** | N/A | 「先行者」創造距離差，隨後「同步推進」 |