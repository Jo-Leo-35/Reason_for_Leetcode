class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
            
        # Space-Optimized DP: O(1) space, O(N) time
        prev1 = 2 # f(n-1)
        prev2 = 1 # f(n-2)
        
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
            
        return prev1
