from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # Two Pointers with Dummy Node: O(N) time, O(1) space (One pass)
        dummy = ListNode(0, head)
        fast = dummy
        slow = dummy
        
        # Advance fast pointer by n steps
        for _ in range(n):
            fast = fast.next
            
        # Move both until fast reaches the last node
        while fast.next:
            slow = slow.next
            fast = fast.next
            
        # Delete the nth node
        slow.next = slow.next.next
        
        return dummy.next