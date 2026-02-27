from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Sorting + Two Pointers: O(N^2) time, O(1) auxiliary space (excluding timsort)
        res = []
        nums.sort()
        
        for i in range(len(nums) - 2):
            # Avoid duplicate target loops
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            # Quick exit if the minimum element is already positive
            if nums[i] > 0:
                break
                
            left, right = i + 1, len(nums) - 1
            
            while left < right:
                total_sum = nums[i] + nums[left] + nums[right]
                
                if total_sum < 0:
                    left += 1
                elif total_sum > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    
                    # Skip duplicate numbers inside the loop
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                        
                    left += 1
                    right -= 1
                    
        return res
