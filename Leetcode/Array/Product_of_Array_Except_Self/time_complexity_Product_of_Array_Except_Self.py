from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        # TIME OPTIMAL: Two-Pass Prefix + Suffix
        # Time: O(N) — two linear passes
        # Space: O(N) — two explicit arrays (left[], right[])
        # This version is the most readable / interview-explainable form.
        n = len(nums)
        left = [1] * n    # left[i]  = product of all elements to the LEFT of i
        right = [1] * n   # right[i] = product of all elements to the RIGHT of i

        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]

        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]

        return [left[i] * right[i] for i in range(n)]
