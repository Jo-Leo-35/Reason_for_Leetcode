from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # SPACE OPTIMAL: Sort + Two Pointers (same algorithm — already O(1) auxiliary)
        # Time: O(N^2)
        # Space: O(1) auxiliary (sorting in-place; output array not counted)
        # Note: No hash-based approach can beat this in space because two pointers
        #       achieves O(1) extra — there is no space/time trade-off here.
        res = []
        nums.sort()

        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            if nums[i] > 0:
                break

            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1

        return res
