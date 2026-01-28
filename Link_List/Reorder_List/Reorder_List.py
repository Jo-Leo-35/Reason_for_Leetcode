class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head or not head.next: return

        # 1. 找中點 (Fast pointer 從 head.next 開始，確保 slow 停在前半段結尾)
        slow, fast = head, head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2. 切斷與反轉 (物理意義：拔掉掛鉤，調轉車頭)
        curr = slow.next
        slow.next = None  # 重要！切斷前半段，防止環產生
        prev = None
        while curr:
            next_tmp = curr.next
            curr.next = prev
            prev = curr
            curr = next_tmp
        
        # 3. 交錯合併 (while second 決定邊界)
        first, second = head, prev
        while second:
            first_tmp_next = first.next
            second_tmp_next = second.next
            
            first.next = second
            second.next = first_tmp_next
            
            first, second = first_tmp_next, second_tmp_next