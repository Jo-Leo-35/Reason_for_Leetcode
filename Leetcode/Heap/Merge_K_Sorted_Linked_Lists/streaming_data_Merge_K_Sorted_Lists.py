'''
演算法步驟（適合大量無窮盡的資料流 / 分散式系統合併）：
1. 準備一個最小堆積 (Min-Heap)。
2. 先把每個 Linked List 的第一個（最小的）節點取出來，放入 Heap 中。
3. 因為在 Python 的 `heapq` 中，如果兩個節點的 `val` 相同，它會去比較 `tuple` 的下一個元素。為了避免它嘗試比對 `ListNode` 物件並報錯，我們把 List 的索引 `i` 也放進 tuple 當作 Tie-breaker。
4. 建立一個 Dummy Node 當作新串列的火車頭，並用一個 `tail` 指標跟著新車廂移動。
5. 當 Heap 不為空時：
   - 彈出 Heap 中最小的節點，接在 `tail` 後面。
   - `tail` 往前進一步。
   - 如果剛剛彈出的節點後面「還有下一個節點」，就把那個「下個節點」推回 Heap 中！這就是資料流 Streaming 讀取的精神。
6. 這個解法的時間複雜度一樣是 O(N log K)，但這是在記憶體裝不下全部資料，只能開 K 個 Socket Streaming 讀取時的最佳解（每次只維持大小為 K 的 Heap，空間極小）。
'''
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy
        min_heap = []
        
        # 初始化：將 K 個頭節點放入 Heap
        for i, l in enumerate(lists):
            if l:
                heapq.heappush(min_heap, (l.val, i, l))
                
        # 開始 Streaming 合併
        while min_heap:
            val, i, node = heapq.heappop(min_heap)
            tail.next = node
            tail = tail.next
            
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))
                
        return dummy.next
