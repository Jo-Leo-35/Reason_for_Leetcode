from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
            
        # Helper function covering the linear House Robber logic
        def helper(houses: List[int]) -> int:
            rob1, rob2 = 0, 0
            for money in houses:
                temp = max(money + rob1, rob2)
                rob1 = rob2
                rob2 = temp
            return rob2
            
        # Case 1: Rob from house 0 to n-2
        # Case 2: Rob from house 1 to n-1
        # Maximize both cases
        return max(helper(nums[:-1]), helper(nums[1:]))
