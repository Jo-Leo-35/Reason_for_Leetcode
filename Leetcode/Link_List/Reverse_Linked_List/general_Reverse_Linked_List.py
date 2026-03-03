'''
演算法步驟：
1. 目標是反轉一個單向 Linked List。我們需要用到三個指標：`prev` (前一個節點), `curr` (當前節點), 和 `nxt` (下一個節點)。
2. 初始化：`prev` 設為 `None` (因為反轉後原本的 Head 就會變成 Tail，指向 None)，`curr` 設為 `head`。
3. 開始走訪 Linked List，直到 `curr` 變成 `None`：
   - 第一步：先用 `nxt = curr.next` 把當前節點的原本下家存起來，以免斷線後找不回來。
   - 第二步：霸氣反轉！把當前節點的 Next 指針扭轉，指回前一個節點 (`curr.next = prev`)。
   - 第三步：把 `prev` 指標往前推進一格 (`prev = curr`)。
   - 第四步：把 `curr` 指標也往前推進一格 (`curr = nxt`)，這代表我們邁向剛剛備份存起來的下家繼續工作。
4. 走訪完畢時，`curr` 為 `None`，而 `prev` 正好站在原本串列的最後一個節點，也就是「新串列的頭」。
5. 回傳 `prev`。這個遞迴 O(N) 走完且 O(1) 極致空間的 Iterative 解法，就是真正的最強通用模板。
'''
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
            
        return prev
