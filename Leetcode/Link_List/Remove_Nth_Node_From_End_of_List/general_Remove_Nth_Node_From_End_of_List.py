'''
演算法步驟：
1. 目標是刪除 Listed List 倒數第 N 個節點。要達到單趟 O(N) 掃描且 O(1) 空間，必須使用「雙指針 (Two Pointers)」與「Dummy Node」技巧。
2. 因為可能要刪除的是第一個節點呀！在 Head 前面擺一個 `dummy` 可以拯救我們不會遇到 Head 被刪掉後難以回傳的窘境。
3. 讓 `fast` (快指標) 和 `slow` (慢指標) 一開始都站在 `dummy` 身上。
4. 為了讓 `fast` 和 `slow` 中間卡著「剛好 N 步」的距離差，我們讓 `fast` 先無情往前走 N 步。
5. 接著，讓 `fast` 和 `slow` 以相同的速度（一步一步）往前走。
6. 當 `fast.next` 變成 None（也就是 `fast` 踏上了這串列最後一節車廂）時，停！
7. 由於一開始刻意拉出的距離差，這時候 `slow` 剛好會站在「即將被刪除的那個悲劇節點的『前方一格』」。
8. 我們只要切斷連結：`slow.next = slow.next.next`，這個倒數第 N 格就從 Linked List 裡人間蒸發了。
9. 完美達成一次走訪刪除的成就，最後端出 `dummy.next`。
'''
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy
        
        for _ in range(n):
            fast = fast.next
            
        while fast.next:
            slow = slow.next
            fast = fast.next
            
        slow.next = slow.next.next
        
        return dummy.next
