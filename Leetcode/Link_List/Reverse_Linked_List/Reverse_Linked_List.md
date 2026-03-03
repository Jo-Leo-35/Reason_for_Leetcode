### 1. 核心題意與挑戰

反轉一個單向鏈結串列 (Singly Linked List)。

* **隱藏挑戰**：這是一切指標 (Pointer) 變換的基礎操作。面試官看的不只是你「能不能寫出來」，更會看你寫得「夠不夠乾淨、有沒有處理空指標異常 (Null Pointer Exception)」。

---

### 2. 解法對比與完整程式碼

#### A. 迭代法 (Iterative) —— **業界與面試的最標準解法**

**思路**：
我們需要三個指針來輔助此過程：
1. `prev`：指向已經反轉好的部分，最初為 `None`。
2. `curr`：指向當前正在處理的節點，最初為 `head`。
3. `next_node`：暫存下一個節點，以免切斷 `curr.next` 之後丟失後續的長鏈結。

每次迴圈的操作順序：先救後人 (`next_node = curr.next`) -> 掉頭 (`curr.next = prev`) -> 指針前進 (`prev = curr`, `curr = next_node`)。

* **優點**：空間複雜度 $O(1)$，無遞迴堆疊溢出風險。

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        
        while curr:
            # 1. 暫存下一個節點
            next_node = curr.next
            # 2. 當前節點掉頭
            curr.next = prev
            # 3. 推進 prev 和 curr
            prev = curr
            curr = next_node
            
        # 迴圈結束時，curr 會是 None，prev 剛好是原本鏈結的最後一個節點（反轉後的新頭節點）
        return prev
```

#### B. 遞迴法 (Recursive) —— **展現抽象邏輯思維的寫法**

**思路**：
遞迴的核心是：我們假設 `reverseList(head.next)` 已經完美地把後面的節點都反轉好了。
現在後面的部分長這樣：`head -> head.next <- Node <- Node`
我們只要做兩步：
1. 把 `head.next` 的指針指向自己 (`head.next.next = head`)
2. 把自己的指針指向 Null (`head.next = None`)

* **優點**：程式碼極具數學美感，邏輯抽象程度高。
* **缺點**：空間複雜度因為 Call Stack 的關係變成了 $O(N)$，且在超長鏈結時會 Stack Overflow。

```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 遞迴的基底條件 (Base Case)
        if not head or not head.next:
            return head
            
        # 遞迴取得反轉後的新頭節點 (永遠都是原本的最後一個節點)
        new_head = self.reverseList(head.next)
        
        # 將自己後面的那個節點，反過來指向自己
        head.next.next = head
        
        # 切斷自己往後的連結，防止形成環
        head.next = None
        
        return new_head
```

---

### 3. 實務應用場景

反轉鏈結是最基本的操作，往往作為更大型系統的某一個微型子步驟。

#### 1. Undo/Redo 系統操作
* **應用**：編輯器中的復原機制，若使用 Linked List 來儲存歷史操作步驟，在某些情況下對步驟進行反轉以快速回溯。

#### 2. K-Group Reverse (進階題前置)
* **應用**：在處理網路封包的交錯重組、或者是資料加密中 Block 的位元翻轉時，會利用到固定長度的區段反轉。這時 Iterative 反轉就成了核心積木。

---

### 4. 總結筆記

| 比較維度 | Iterative 迭代 | Recursive 遞迴 |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ |
| **空間複雜度** | $O(1)$ | $O(N)$ (遞迴堆疊) |
| **實戰心法** | 必背！「三指針法」的順序不能搞混。 | 了解原理即可，面試時建議優先寫 Iterative。 |
| **容易犯錯** | 忘記回傳 `prev` 而是回傳了 `head` | 忘記把 `head.next = None` 導致產生 Circular List |
