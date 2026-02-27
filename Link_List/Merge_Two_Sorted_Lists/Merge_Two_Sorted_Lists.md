### 1. 核心題意與挑戰

將兩個**升序**鏈結串列合併為一個新的升序鏈結串列並返回。
新鏈結串列是透過拼接給定的兩個鏈結串列的所有節點組成的。

* **隱藏挑戰**：
  * 如何優雅地處理當其中一個鏈結已經為空，另一個鏈結還有剩餘節點的情況？
  * 節點不需要自己 `new` 出來，只需要調整現有節點的指標 (in-place modification)。

---

### 2. 解法對比與完整程式碼

#### A. 迭代法 + 虛擬頭節點 (Dummy Node) —— **工程師必備的最佳實踐**

**思路**：
設置一個 `dummy` 節點。這個節點的值不重要，它存在的目的是作為返回合併結果的定海神針（避免處理頭節點為空的各種邊界條件）。
我們用一個指標 `tail` 隨著比較過程不斷把較小的節點接在後面。
當其中一條鏈比較完後，直接把 `tail.next` 指向另一條剩下的鏈即可，因為剩下的本身就已經是排序過的結構。

* **優點**：不耗費額外的空間建立新節點，時間也是線性。邏輯最穩定。
* **缺點**：無。

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # 建立一個虛擬頭節點
        dummy = ListNode()
        tail = dummy
        
        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
                
            tail = tail.next
            
        # 把剩下的部分直接串上去 (無論是 list1 還是 list2)
        # 如果兩者皆空，這行也不會出錯 (接上 None)
        if list1:
            tail.next = list1
        elif list2:
            tail.next = list2
            
        # 返回 dummy.next，這才是真正合併後的第一個節點
        return dummy.next
```

#### B. 遞迴法 (Recursive) —— **令人驚豔的炫技寫法**

**思路**：
比較 `list1` 和 `list2` 的當前節點。
如果 `list1` 比較小，那合併後的鏈結就是：`list1` 加上合併後的(`list1`的下一個, `list2`)。這就是一個完美的遞迴推導。

* **優點**：程式碼極短，體現對資料結構與遞迴極深的理解。
* **缺點**：如果鏈的長度高達數萬，會引發 Stack Overflow 導致崩潰。實務較少採用。

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # 遞迴的終止條件
        if not list1:
            return list2
        if not list2:
            return list1
            
        # 哪邊比較小，哪邊就當頭，並且讓它去接剩下的比較結果
        if list1.val < list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

---

### 3. 實務應用場景

#### 1. Merge Sort 的基礎核心 (External Sorting)
* **應用**：資料庫系統中要對兩個已經排序完成的小資料表或硬碟區塊進行合併（External Sorting），其核心用的就是這個演算法精神。指標前移避免了將整個大檔案讀進記憶體的窘境。

#### 2. 日誌檔合併 (Log Aggregation)
* **應用**：分散式系統中，從兩台伺服器拉取的 Log 都有獨立的 Timestamp 順序。若要交錯輸出一份全局 Timeline 的日誌流，就是 Merge Two Sorted Lists。

---

### 4. 總結筆記

| 比較維度 | 迭代法 + Dummy Node | 遞迴法 |
| --- | --- | --- |
| **時間複雜度** | $O(M + N)$ | $O(M + N)$ |
| **空間複雜度** | $O(1)$ | $O(M + N)$ (遞迴堆疊) |
| **設計模式** | **Dummy Node** 是解 Linked List 題目的終極殺器 | 狀態組合推導 |
| **面試表現** | 中規中矩，必須要零 Bug 寫出來。 | 若能兩者都寫出來並講出 Call Stack 問題，必定加分。 |
