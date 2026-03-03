from typing import List

class Solution:
    def climbStairs(self, n: int) -> int:
        # TIME & SPACE OPTIMAL: O(1) space rolling DP
        # Time: O(N)
        # Space: O(1) — only two variables track the last two Fibonacci-like values
        # Note: O(log N) via matrix exponentiation exists but is overly specialized for interviews.
        if n <= 2:
            return n

        prev2, prev1 = 1, 2
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr

        return prev1
