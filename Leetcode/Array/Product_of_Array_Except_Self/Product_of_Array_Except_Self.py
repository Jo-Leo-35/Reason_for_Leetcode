from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # Result array doesn't count towards space complexity
        # O(N) time, O(1) extra space
        answer = [1] * n
        
        # 1. Left prefix product calculation
        left_prod = 1
        for i in range(n):
            answer[i] = left_prod
            left_prod *= nums[i]
            
        # 2. Right suffix product calculation and immediate answer assembly
        right_prod = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right_prod
            right_prod *= nums[i]
            
        return answer
