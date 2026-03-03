'''
通用解法：使用 Python OrderedDict

Python 的 OrderedDict 內建維護插入順序，並支援 move_to_end()，
可以用極少的程式碼實現 LRU Cache，是面試「快速實現」的捷徑。

缺點：面試官可能要求你不使用標準庫的有序字典，親手實現底層邏輯。
'''
from collections import OrderedDict


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # 移到尾端 = 最近使用
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 移除頭端 = 最久未使用
