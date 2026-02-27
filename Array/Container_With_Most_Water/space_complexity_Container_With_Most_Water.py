from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # SPACE OPTIMAL: Two Pointers (same as time-optimal)
        # Time: O(N)
        # Space: O(1) — only two pointer variables, no extra data structures
        left, right = 0, len(height) - 1
        max_water = 0

        while left < right:
            water = min(height[left], height[right]) * (right - left)
            max_water = max(max_water, water)

            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return max_water
