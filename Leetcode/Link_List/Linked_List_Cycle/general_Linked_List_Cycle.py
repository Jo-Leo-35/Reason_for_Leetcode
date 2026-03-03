'''
演算法步驟：
1. 這是經典的 Floyd's Tortoise and Hare (龜兔賽跑) 演算法。
2. 準備兩個指標：`slow` 和 `fast`。初始都指向起點 `head`。
3. 烏龜 `slow` 每次只走一步 (`slow = slow.next`)。
4. 兔子 `fast` 每次走兩步 (`fast = fast.next.next`)。
5. 在迴圈中檢查，如果 `fast` 或是 `fast.next` 碰到了 `None`，代表兔子跑到了終點，這條 Linked List 是直線沒有環的，回傳 False。
6. 如果兩者在途中的某個時刻相遇了 (`slow == fast`)，代表兔子在操場裡繞了一大圈從後面追上並撞到了烏龜。這證明結構裡必定有環，回傳 True。
7. 時間複雜度 O(N)，完全不需要額外紀錄狀態，空間複雜度是完美的 O(1)。
'''
from typing import Optional

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            
            if slow == fast:
                return True
                
        return False
