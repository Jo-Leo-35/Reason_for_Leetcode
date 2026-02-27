from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # TIME & SPACE OPTIMAL: Binary Search on Rotated Array
        # Time: O(log N)
        # Space: O(1)
        # Determine which half is sorted, then check if target lies in it.
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            # Left half is sorted
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
