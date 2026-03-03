from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        # SPACE OPTIMAL: Binary Search (same as time-optimal — already O(1) space)
        # Time: O(log N)
        # Space: O(1) — only left/right/mid pointer variables
        left, right = 0, len(nums) - 1

        while left < right:
            mid = left + (right - left) // 2  # avoids integer overflow (good habit)
            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid

        return nums[left]
