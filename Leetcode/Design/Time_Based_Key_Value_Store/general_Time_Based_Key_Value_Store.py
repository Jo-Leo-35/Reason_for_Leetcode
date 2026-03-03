'''
演算法步驟：
1. 目標是設計一個資料結構，能夠記錄同一個 key 在不同時間點的值，並且能透過時間戳進行查詢。
2. 因為時間是一直往前推進的（題目保證 `timestamp` 嚴格遞增），所以我們不需要每次塞資料都自己排序。
3. 我們宣告一個 `defaultdict(list)` 的資料結構 `store`。
4. 當呼叫 `set(key, value, timestamp)` 時，我們無腦把 `(timestamp, value)` 這個 Tuple 疊加到對應的 `store[key]` 陣列尾端。這陣列自動會是按照時間小到大排序好的。
5. 當呼叫 `get(key, timestamp)` 時：
   - 如果這家商店根本沒進過這個貨 (`key not in self.store`)，霸氣回傳空字串 `""`。
   - 去倉庫把屬於這個貨品的歷史清單 `values` 調閱出來。
   - 如果客人要的時間，比這東西發明（第一筆紀錄）還要早 `timestamp < values[0][0]`，也回傳空字串。
6. 最精彩的來了：
   - 我們用 `bisect.bisect_right()` 二分搜尋法，在 `values` 歷史清單中，找尋「第一個大於」目標時間的位址。
   - 由於 Python 的 Tuple 比較會先比第一個元素，所以我們丟個 `(timestamp, chr(127))` 進去比。`chr(127)` 是最大的 ASCII 字元，確保時間一樣時也能被當成「大於」。
   - 找到那個「剛好超過目標時間」的 index 後，退一步 `idx - 1`，就是我們要找的「剛好小於等於目標時間」的最新那筆合法紀錄！
   - 回傳 `values[idx - 1][1]`。
7. 時間複雜度：Set O(1)，Get O(log N)。空間 O(N)。
'''
from collections import defaultdict
import bisect

class TimeMap:

    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
            
        values = self.store[key]
        
        if timestamp < values[0][0]:
            return ""
            
        idx = bisect.bisect_right(values, (timestamp, chr(127)))
        
        return values[idx - 1][1]

# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
