from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # HashSet Source Finder: O(N) time, O(N) space
        num_set = set(nums)
        longest = 0
        
        for num in num_set:
            # Check if this num is the start of a sequence
            if (num - 1) not in num_set:
                curr_num = num
                curr_streak = 1
                
                # Keep finding the next contiguous elements
                while (curr_num + 1) in num_set:
                    curr_num += 1
                    curr_streak += 1
                    
                longest = max(longest, curr_streak)
                
        return longest
