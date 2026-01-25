import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        minheap = []

        for idx, node in enumerate(lists):
            if node:
                heapq.heappush(minheap, (node.val, idx, node)) # 把 minheap = [], 用 heappush 的方式存
            
        dummy = ListNode(0)
        current = dummy

        while minheap:
            val, idx, smallest_node = heapq.heappop(minheap)

            current.next = smallest_node
            current = current.next # 用於紀錄下一個點的指標

            if smallest_node.next:
                next_node = smallest_node.next
                heapq.heappush(minheap, (next_node.val, idx, next_node))

        return dummy.next

"""
1. 先初始化 minheap 並且填入 list 的開頭, 注意是 tuple, 所以要填入 idx, 用於表示第幾個 heap element, 避免 Node, Node 於 tuple[2] 比較但不能比較
2. 初始化 dummy 用於當 List 的開頭, 數值任意填
3. heapq.pop 最小值, 並且接上 response 的 Linked-List
4. 用 current 去紀錄 Linked-List 的位置, 用 dummy 去初始化 Linked-List
5. 如果 smallest_node 有下一個點, 就將   smallest_node.next heapqpush回去
Note: heapq 就是 minheap, 你要 maxheap 就自己取  -val 於 val 值
"""