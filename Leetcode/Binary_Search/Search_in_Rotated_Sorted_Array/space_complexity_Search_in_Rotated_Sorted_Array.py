from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # SPACE OPTIMAL: Binary Search (same as time-optimal — already O(1))
        # Time: O(log N)
        # Space: O(1) — iterative, no recursion stack
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = left + (right - left) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:          # left half sorted
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:                                # right half sorted
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
