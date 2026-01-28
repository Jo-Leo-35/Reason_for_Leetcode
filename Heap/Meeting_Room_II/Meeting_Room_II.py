import heapq

class Solution:

    def minMeetingRooms(self, intervals: list[list[int]]) -> int:

        intervals.sort(key = lambda x: x[0]) # 排序 intervals

        heap = [] # 初始化 heap

        heapq.heappush(heap, intervals[0][1]) # 紀錄最早的結束時間

       

        for i in range(1, len(intervals)):

            if intervals[i][0] >= heap[0]:

                heapq.heappop(heap)

            heapq.heappush(heap, intervals[i][1])

       

        return len(heap)