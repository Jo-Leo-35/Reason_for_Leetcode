from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        # Two Pointers: O(N) time, O(1) space
        left, right = 0, len(height) - 1
        max_water = 0
        
        while left < right:
            # Calculate the area
            current_water = (right - left) * min(height[left], height[right])
            max_water = max(max_water, current_water)
            
            # Move the shorter line inward
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_water
