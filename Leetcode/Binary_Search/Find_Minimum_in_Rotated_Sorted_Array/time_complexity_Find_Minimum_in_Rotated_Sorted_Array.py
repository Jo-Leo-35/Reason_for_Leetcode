from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        # TIME & SPACE OPTIMAL: Binary Search
        # Time: O(log N) — halve the search space each iteration
        # Space: O(1)
        # Key insight: the minimum is always on the "unsorted" half.
        # If nums[mid] > nums[right], minimum is in right half; else left half.
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[right]:
                left = mid + 1   # min must be in right half
            else:
                right = mid      # mid could be the min; include it

        return nums[left]
