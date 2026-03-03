from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        # Space-Optimized DP: O(1) space, O(N) time
        # rob1 is max money from i-2 houses, rob2 is max money from i-1 houses
        rob1, rob2 = 0, 0
        
        for money in nums:
            # We can either rob the current house + rob1, or just keep rob2
            temp = max(money + rob1, rob2)
            rob1 = rob2
            rob2 = temp
            
        return rob2
