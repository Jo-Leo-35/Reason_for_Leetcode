'''
演算法步驟：
1. 先將所有會議的區間，依照「開始時間」由小到大進行排序。
2. 準備一個 Min-Heap（最小堆積），用來存放目前正在使用中的會議室的「結束時間」。
3. 把第一場會議的結束時間 Push 進 Heap 中（代表開出了第一間房間）。
4. 遍歷剩下的每一場會議：
   - 查看 Heap 的頂端（也就是最早結束的房間）。
   - 如果頂端的結束時間「小於或等於」當前會議的開始時間，代表房間空出來了！將該元素 Pop 彈出。
5. 不管有沒有空出房間，都將當前會議的結束時間 Push 進 Heap，代表佔用了一間房間直到該時間點。
6. 最後 Heap 中剩餘的元素個數，就是歷史上同時開出的最大房間數（至少需要的會議室總數）。
'''
from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
            
        intervals.sort(key=lambda x: x[0])
        free_rooms = []
        
        heapq.heappush(free_rooms, intervals[0][1])
        
        for meeting in intervals[1:]:
            if free_rooms[0] <= meeting[0]:
                heapq.heappop(free_rooms)
            
            heapq.heappush(free_rooms, meeting[1])
            
        return len(free_rooms)
