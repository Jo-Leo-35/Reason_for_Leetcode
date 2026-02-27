'''
演算法步驟（差分陣列 / TreeMap 概念）：
1. 在資料流的場景下，會議可能是動態隨機加入的。我們無法預先得知所有的區間並加以排序。
2. 我們使用一個類似 TreeMap (Python 可使用 SortedDict 或一般 Dict 但事後排序) 的結構 `timeline`。
3. 針對資料流進來的每個區間 `[start, end]`，我們在 `timeline[start]` 處加上 +1（代表需求增加一間房），在 `timeline[end]` 處加上 -1（代表釋放一間房）。
4. 當系統需要查詢目前的「最大會議室需求」時，我們只需要將 `timeline` 按照時間點掃描一次（依照 Key 排序）。
5. 累加沿途的所有變更量 `current_rooms += timeline[time]`，其間記錄到的最高值即為答案。
'''
from typing import List
from collections import defaultdict

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # Python 沒有內建的 TreeMap，此處示範 Data Stream 儲存狀態的方法
        timeline = defaultdict(int)
        
        # O(1) 時間紀錄新來的資料事件
        for start, end in intervals:
            timeline[start] += 1
            timeline[end] -= 1
            
        # O(K log K) 時間查詢全局狀態 (K 為獨立的時間點數量)
        max_rooms = 0
        current_rooms = 0
        
        for time in sorted(timeline.keys()):
            current_rooms += timeline[time]
            max_rooms = max(max_rooms, current_rooms)
            
        return max_rooms

# 使用場景：
# 如果有一個 addMeeting(start, end) 的 API 可以立即呼叫，
# 那麼添加會議的時間只需要 O(1) 紀錄在 Hash Map 中，
# 只有在呼叫 getMaxRooms() 時才需要做排序跟遍歷。
