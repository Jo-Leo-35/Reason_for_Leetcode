### 1. 核心題意與挑戰

給定一個單向鏈結串列：`L0 → L1 → … → Ln-1 → Ln`
將其重新排列後變為：`L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → …`
**不能只是改變節點內部的值**，而是需要實際進行節點指標的重整。

* **隱藏挑戰**：
  * 單向鏈結串列無法「從尾巴走回來」，所以不可能直觀地一前一後交替取用。
  * 這題其實是前面三個 Linked List 基礎題型的**大魔王綜合體**！必須將這道題拆解。

---

### 2. 解法對比與完整程式碼

#### A. O(N) 空間解法 (Array 中繼法)

**思路**：把所有節點裝進一個 Python 的 `List` (陣列) 中。既然變成陣列了，我們就可以輕鬆透過雙指針 (`left=0, right=len-1`) 一頭一尾地交替修改 `next` 連結。
* **缺點**：使用了 $O(N)$ 的額外空間，面試官一定會要求你做到 In-place 修改 ($O(1)$ 空間)。

#### B. 三步拆解法 (Find Mid -> Reverse -> Merge) —— **展現基本功的唯一正解**

**思路**：
如果把題目畫出來，其實就是要拿「前半段」加上「反轉過後的後半段」進行交錯編織。
1. **快慢指針找中點** (龜兔賽跑找中位數)
2. **反轉後半段** (Reverse Linked List)
3. **交錯合併兩個串列** (Merge Two Sorted Lists 變形)

這三個步驟各佔一部份常數級別的時間 $O(N)$，總體仍為 $O(N)$，且空間複雜度 $O(1)$！

```python
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return
            
        # 步驟一：快慢指針找鏈結中點
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
        # 步驟二：反轉後半段 (slow 之後的節點)
        # 這裡的邏輯等同於 Reverse Linked List 基礎題
        prev = None
        curr = slow.next
        # 將前半段與後半段切斷連結，否則會形成環！
        slow.next = None
        
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
            
        # 此時 prev 是反轉後那段的頭節點
        
        # 步驟三：交錯合併前半段與後半段
        first = head
        second = prev # 反轉過後的下半部
        
        while second: # 因為 second 的長度會等於或少1於 first，所以用 second 判斷即可
            # 暫存兩者的下一個節點
            tmp1, tmp2 = first.next, second.next
            
            # 將 first 指向 second，再將 second 指向原本 first 的下一個
            first.next = second
            second.next = tmp1
            
            # 指針推進
            first = tmp1
            second = tmp2
```

---

### 3. 實務應用場景

#### 1. 儲存設備的反向尋軌優化 (Elevator Algorithm in Disks)
* **應用**：這種類似一前一後的來回掃瞄（頭-尾-頭-尾）邏輯，與傳統磁帶或磁碟 IO 讀寫時優化磁頭移動路徑的（例如 C-SCAN 的變形）概念有異曲同工之妙。

#### 2. UI/元件渲染的交錯排列 (Interleaving Views)
* **應用**：前端開發常常遇到要把兩個清單來源（例如「廣告推薦清單」與「自然搜尋結果」）一對一交錯渲染到畫面上，若來源是只能向前遍歷的串流 (Stream)，這類演算法提供很好的基礎抽象。

---

### 4. 總結筆記

| 比較解說 | 陣列暫存法 | 三步拆解法 (In-place) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ (走訪共三次 $\sim3N$) |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **測驗主旨** | N/A | **中點**、**反轉**、**合併**的完美結合 |
| **易錯細節** | 必須記得把陣列最後一個結點的 `next` 設為 Null。 | 忘記 `slow.next = None` 切斷中點，程式會陷入無窮迴圈。 |
