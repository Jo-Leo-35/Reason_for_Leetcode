import collections
import bisect

class TimeMap:

    def __init__(self):
        # 資料結構: Key -> List of [timestamp, value]
        # 例如: "foo" -> [[1, "bar"], [4, "bar2"]]
        self.store = collections.defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # 題目保證: timestamp 嚴格遞增
        # 所以直接 append 就可以保持 List 是有序的 (Sorted)
        # Time: O(1)
        self.store[key].append([timestamp, value])

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        
        values = self.store[key]
        
        # Binary Search (Upper Bound)
        # 尋找第一個 "大於" timestamp 的位置
        # key=lambda x: x[0] 讓 bisect 只看 [time, val] 中的 time
        i = bisect.bisect_right(values, timestamp, key=lambda x: x[0])
        
        # 處理邊界情況:
        # 如果 i == 0，代表所有的歷史時間都比查詢時間還晚 -> 找不到過去的紀錄
        if i == 0:
            return ""
        
        # bisect_right 找到的是「插入點」，所以我們要找的前一個位置 (i-1)
        # 才是「小於等於 timestamp 的最大值」
        return values[i - 1][1]
