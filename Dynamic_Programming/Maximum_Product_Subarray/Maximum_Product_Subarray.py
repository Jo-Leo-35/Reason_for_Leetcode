from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        # O(N) time, O(1) space
        # Track both min and max because multiplying two negatives yields a positive
        res = nums[0]
        curr_min, curr_max = nums[0], nums[0]
        
        for i in range(1, len(nums)):
            num = nums[i]
            # When multiplied by a negative, the max and min swap
            if num < 0:
                curr_min, curr_max = curr_max, curr_min
                
            curr_max = max(num, curr_max * num)
            curr_min = min(num, curr_min * num)
            
            if curr_max > res:
                res = curr_max
                
        return res
