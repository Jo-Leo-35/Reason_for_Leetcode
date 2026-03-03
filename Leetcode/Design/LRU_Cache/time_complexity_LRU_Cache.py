'''
演算法步驟（雙向鏈結串列 + HashMap，所有操作 O(1)）：

核心思路：
  - HashMap (dict): key -> Node，負責 O(1) 查找節點位置。
  - Doubly Linked List: 維護「使用順序」，Head 端最新，Tail 端最舊。
  - 兩者搭配，既能快速查找，又能快速調整順序，缺一不可。

_remove(node) — O(1)：
1. 把 node 的前一個節點 (prev) 的 next 直接接到 node 的下一個節點 (next)。
2. 把 node 的下一個節點 (next) 的 prev 直接接回 node 的前一個節點 (prev)。
3. 這樣 node 就從鏈結串列中「消失」了，不需要遍歷任何節點。
4. 有 dummy head 和 dummy tail，永遠不用擔心邊界為 None 的問題。

_insert_front(node) — O(1)：
1. 把 node 插入到 dummy head 的正後方（成為最新使用的節點）。
2. 調整四條指針：node.next, node.prev, head.next.prev, head.next。

get(key) — O(1)：
1. 若 key 不在 cache 中，返回 -1。
2. 否則，先把 node 從目前位置「移除」，再「插入」到鏈結串列最前端。
3. 這樣每次 get 後，該 key 就成為「最近使用」，排在驅逐順序的最後。
4. 回傳 node.val。

put(key, value) — O(1)：
1. 若 key 已存在，先把舊的 node 從鏈結串列移除（會在下一步覆蓋）。
2. 建立新的 Node(key, value)，存入 cache dict，並插入鏈結串列最前端。
3. 若 cache 大小超過 capacity：
   - 找到 tail.prev，這就是最久未使用的節點（LRU 節點）。
   - 從鏈結串列移除它，並從 dict 中刪除對應的 key。
   - 注意：必須先取 lru.key 再刪除，否則節點斷開後無從找回 key。

空間複雜度：O(capacity) — HashMap 與鏈結串列各存最多 capacity 個節點。
'''
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
