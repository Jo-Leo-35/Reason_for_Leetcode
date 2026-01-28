def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    # 1. Dummy Node (哨兵節點)：處理刪除頭節點的 Edge Case
    dummy = ListNode(0, head)
    slow = fast = dummy

    # 2. 拉開間距：Fast 先跑 n+1 步
    # 為什麼是 n+1？因為要讓 slow 停在「目標前驅節點」
    for _ in range(n + 1):
        fast = fast.next

    # 3. 同步移動：直到 fast 觸底 (None)
    while fast:
        slow = slow.next
        fast = fast.next

    # 4. 執行刪除：語意化 Dry Run 驗證
    # 假設 [1, 2], n=2，此時 slow 停在 dummy，slow.next 就是節點 1
    slow.next = slow.next.next
    
    return dummy.next