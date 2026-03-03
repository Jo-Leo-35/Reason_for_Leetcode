from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # TIME & SPACE OPTIMAL: Two Pointers
        # Time: O(N) — single pass shrinking window from both ends
        # Space: O(1)
        # Greedy insight: always move the shorter side inward because
        # moving the taller side can only decrease or maintain area.
        left, right = 0, len(height) - 1
        max_water = 0

        while left < right:
            width = right - left
            water = min(height[left], height[right]) * width
            max_water = max(max_water, water)

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water
