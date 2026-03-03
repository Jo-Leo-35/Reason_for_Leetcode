from typing import List
import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
            
        # Min-Heap sorting by end times: O(N log N) time, O(N) space
        intervals.sort(key=lambda x: x[0])
        free_rooms = []
        
        # Add the first meeting's end time
        heapq.heappush(free_rooms, intervals[0][1])
        
        for meeting in intervals[1:]:
            # If the earliest ending meeting ends before or when this one starts
            if free_rooms[0] <= meeting[0]:
                heapq.heappop(free_rooms)
            
            # Add the current meeting's end time
            heapq.heappush(free_rooms, meeting[1])
            
        return len(free_rooms)
