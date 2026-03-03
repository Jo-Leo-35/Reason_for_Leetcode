'''
演算法步驟：
1. 目標是合併兩條已排序好的 Linked List。
2. 這題最標準且 O(1) 空間的解法是「Dummy Node 拉鍊法」。我們創造一個沒有實際意義的 `dummy = ListNode()` 作為兩組火車頭掛載前的先導車，免去處理 Head 的邊界條件問題。
3. 準備一個 `tail` 指標，起初它站在 `dummy` 節點上。
4. 進入迴圈（當 `list1` 和 `list2` 還有各自的節點時）：
   - 我們看兩邊最前面車廂的數字，哪個小。
   - 假設 `list1` 比較小，我們就把 `tail.next` 接上 `list1`。然後讓 `list1` 向後走一台車廂 (`list1 = list1.next`)。
   - 反之，就把 `tail.next` 接上 `list2`。然後讓 `list2` 向後走一台車廂。
   - 接著讓 `tail` 前進到剛接好的這台最新車廂上 (`tail = tail.next`)。
5. 等到其中一邊（或兩邊）空了，迴圈結束。
6. 這時可能某一邊後面還掛著長長一串已經排好的車廂。太棒了，我們直接讓 `tail.next` 把整串接過來 (`tail.next = list1 if list1 else list2`)。
7. 回傳 `dummy.next` (跳過先導車，這就是我們接好的完美車頭)。
'''
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
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
            
        tail.next = list1 if list1 else list2
        
        return dummy.next
