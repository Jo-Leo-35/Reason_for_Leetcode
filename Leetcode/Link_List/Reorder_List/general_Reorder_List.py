'''
演算法步驟：
1. 這是要求空間為 O(1) 且禁止修改 Node 的 Value，而是硬把記憶體參照「穿插」改寫的經典題。
2. 「Reorder List」可以精準地被切分為三個基礎演算法的綜合運用：
   - 階段 A：尋找中點。使用龜兔賽跑指針 (`slow`, `fast`)。兔子走兩步烏龜走一步，兔子撞牆時，`slow` 就站在前半段的尾巴，`slow.next` 就是後半段的頭。
   - 階段 B：反轉後半段。將 `second = slow.next`，並狠狠地把 `slow.next = None` 切斷！然後用 Reverse Linked List 的 Iterative 招式反轉以 `second` 為首的下半段，最後 `prev` 會成為反轉後下半段的 Head。
   - 階段 C：穿梭合併。準備兩根針，`first` 指在原本開頭，`second` (此時的 `prev`) 指在反轉後的後半段開頭。不斷交替相接：先記住 `first.next`，讓 `first` 指向 `second`，再讓 `first` 變回原本儲存的下一步；再記住 `second.next`，讓 `second` 指向 `first`...。
3. 把這三大 O(N) 模組巧妙呼叫後，整個 List 即在原地被重組完畢。
'''
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next:
            return
            
        # 1. 尋找 Linked List 的中點 (找分割點)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
        # 2. 將後半段切斷，並進行 Reverse 反轉
        second = slow.next
        slow.next = None
        prev = None
        
        while second:
            tmp = second.next
            second.next = prev
            prev = second
            second = tmp
            
        # 3. 將兩條 List 重新交叉合併
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first = tmp1
            second = tmp2
