from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        # Binary Search finding inflection point: O(log N) time
        left, right = 0, len(nums) - 1
        
        while left < right:
            # If sub-array is already sorted, the leftmost is the minimum
            if nums[left] < nums[right]:
                return nums[left]
                
            mid = left + (right - left) // 2
            
            # If left half is sorted, min must be in the right half
            if nums[mid] >= nums[left]:
                left = mid + 1
            # If left half is unsorted, min is mid or in the left half
            else:
                right = mid
                
        return nums[left]
