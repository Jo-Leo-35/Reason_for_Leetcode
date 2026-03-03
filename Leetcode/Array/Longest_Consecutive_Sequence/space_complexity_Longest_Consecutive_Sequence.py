from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # SPACE OPTIMAL: Sort in-place — O(1) extra space
        # Time: O(N log N) — dominated by sort
        # Space: O(1) extra (sort is in-place; O(log N) for Timsort stack, counted as O(1))
        # Trade-off: sacrifices time (N log N vs N) to eliminate the O(N) hash set
        if not nums:
            return 0

        nums.sort()
        longest = 1
        current = 1

        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                continue            # skip duplicate
            elif nums[i] == nums[i - 1] + 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1         # sequence broken

        return longest
