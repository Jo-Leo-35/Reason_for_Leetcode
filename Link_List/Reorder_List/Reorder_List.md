### 1. 題目敘述與抽象概念

**題目描述**：將單向鏈結串列  重新排列為 。
**抽象概念**：

* **「拉鍊式重組」**：將一條長鏈從中間剪斷，將後半段反轉，最後像拉鍊齒一樣交錯扣合。
* **核心三要素**：
1. **中點定位**：區分前半段與後半段。
2. **方向重構**：將後半段「車頭調轉」。
3. **交錯縫合**：將兩條鏈合併。



**Tag**: `Linked List`, `Two Pointers`, `Reverse List`, `In-place`.

---

### 2. 算法比較（Lean Hire vs. Strong Hire）

| 維度 | 暴力解 (Array/Stack) | **最優解 (In-place Manipulation)** |
| --- | --- | --- |
| **策略** | 存入陣列後用雙指針重組。 | **快慢指針找中點 + 反轉後半部 + 交錯合併。** |
| **時間複雜度** |  |  |
| **空間複雜度** |  | **** |
| **評價** | 簡單但消耗記憶體。 | **Strong Hire：展現對指標與記憶體的高效掌控。** |

---

### 3. 微系統設計與產業應用

* **數據交織 (Data Interleaving)**：
在數位通訊或音訊/影像編碼中，為了對抗**突發性錯誤 (Burst Errors)**，會使用類似的交錯算法。如果傳輸中發生連續丟包，交錯後的數據在解碼還原時，錯誤會被分散（分散到不同的時間點或影像幀），進而讓修復算法（如 ECC）更容易找回遺失資訊。
* **緩衝區優化 (Buffer Reordering)**：
在底層驅動開發中，為了符合特定硬體的讀取順序，常需要在不額外申請記憶體（In-place）的情況下重新排列資料塊。

---

### 4. 程式碼模板與 Dry Run (以 `1->3->5->7->9` 為例)

```python
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next: return

        # 1. 找中點 (Fast pointer 從 head.next 開始，確保 slow 停在前半段結尾)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2. 切斷與反轉 (物理意義：拔掉掛鉤，調轉車頭)
        curr = slow.next
        slow.next = None  # 重要！切斷前半段，防止環產生
        prev = None
        while curr:
            next_tmp = curr.next
            curr.next = prev
            prev = curr
            curr = next_tmp
        
        # 3. 交錯合併 (while second 決定邊界)
        first, second = head, prev
        while second:
            first_tmp_next = first.next
            second_tmp_next = second.next
            
            first.next = second
            second.next = first_tmp_next
            
            first, second = first_tmp_next, second_tmp_next

```

**Dry Run 變數追蹤：**

* **Input**: `1 -> 3 -> 5 -> 7 -> 9`
* **中點後**: `first: 1->3->5->None`, `second: 9->7->None` (已反轉)
* **合併 R1**: `1.next=9, 9.next=3`  `first=3, second=7`
* **合併 R2**: `3.next=7, 7.next=5`  `first=5, second=None`
* **結束**: `second` 結束，最後的 `5` 自動連在結尾。結果：`1->9->3->7->5`。

---

### 5. Following up 延伸思考

* **[234. Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)**: 同樣使用「找中點+反轉」的抽象模組。
* **[25. Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/)**: 更複雜的局部反轉，需處理多組銜接。
* **面試題變體**：如果串列長度極大（無法單機存儲），如何進行分佈式重排？
* *答案*：先統計總長度，利用偏移量 (Offset) 將節點編號，再進行資料的分片重排。
