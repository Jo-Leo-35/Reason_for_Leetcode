'''
演算法步驟：
1. 本題是 Merge Two Sorted Lists 的進階版。最直覺但空間複雜度仍為 O(K) 寫遞迴的解法是「分治法 (Divide and Conquer)」。
2. 我們將原本有 K 個串列的陣列，兩兩一組進行合併 (Merge Two Sorted Lists)。
3. 合併完之後，K 個會變成 K/2 個，接著再繼續兩兩合併，變成 K/4... 直到剩下最後一條串列。
4. 每一次合併操作需要花費 O(N) 時間 (N為兩條串列的總節點數)。全域來看，一共有 log(K) 個合併層級。
5. 因此整體時間複雜度為 O(N log K) (N 是所有串列節點的總數)。由於可以用迭代的方式實作，空間複雜度可以達到嚴格的 O(1)。
'''
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        if len(lists) == 1:
            return list(lists)[0]
            
        def mergeTwoLists(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
            dummy = ListNode()
            tail = dummy
            while l1 and l2:
                if l1.val < l2.val:
                    tail.next = l1
                    l1 = l1.next
                else:
                    tail.next = l2
                    l2 = l2.next
                tail = tail.next
            tail.next = l1 if l1 else l2
            return dummy.next
            
        interval = 1
        amount = len(lists)
        
        while interval < amount:
            for i in range(0, amount - interval, interval * 2):
                lists[i] = mergeTwoLists(lists[i], lists[i + interval])
            interval *= 2
            
        return lists[0]
