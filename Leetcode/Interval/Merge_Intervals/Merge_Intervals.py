from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
            
        # Sort by start time: O(N log N) time, O(N) space for result
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        
        for curr in intervals[1:]:
            last = merged[-1]
            
            if curr[0] <= last[1]:
                # Overlap, merge them
                last[1] = max(last[1], curr[1])
            else:
                # No overlap, add to result
                merged.append(curr)
                
        return merged