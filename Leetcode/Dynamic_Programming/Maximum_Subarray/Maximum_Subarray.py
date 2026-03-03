from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        # Kadane's Algorithm: O(N) time, O(1) space
        if not nums:
            return 0
            
        max_sum = nums[0]
        curr_sum = 0
        
        for num in nums:
            if curr_sum < 0:
                curr_sum = 0
                
            curr_sum += num
            
            if curr_sum > max_sum:
                max_sum = curr_sum
                
        return max_sum
