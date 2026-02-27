'''
演算法步驟（Hash Set）：
1. 在真實的伺服器環境中，與其去跑高深的雙指針數學算法，有時候單純的 Hash Set 會是常數時間最快的（因為不用每次判斷兩個指針是否遇到 None，或是記憶體 Cache Miss 等問題）。
2. 建立一個空的 Python `set`。
3. 走訪 Linked List 的每一個節點。
4. 如果走到這個節點時，發現它已經在 `set` 中出現過，代表我們繞了一圈又回來了，回傳 True。
5. 如果沒有出現過，就把它的「記憶體參考位址 (Object Reference)」或者是物件本身加入 `set`。
6. 一直走到遇到 None 為止，回傳 False。
7. 雖然這會耗費 O(N) 的記憶體空間，但通常能在極短的 CPU 週期內完成，是不折不扣的 "Time Complexity" 高效率解。
'''
from typing import Optional

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen = set()
        curr = head
        
        while curr:
            if curr in seen:
                return True
            seen.add(curr)
            curr = curr.next
            
        return False
