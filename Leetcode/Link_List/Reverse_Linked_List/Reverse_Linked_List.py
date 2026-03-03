from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Iterative approach using 3 pointers: O(N) time, O(1) space
        prev = None
        curr = head
        
        while curr:
            nxt = curr.next    # Save next
            curr.next = prev   # Reverse the pointer
            prev = curr        # Move prev forward
            curr = nxt         # Move curr forward
            
        return prev
