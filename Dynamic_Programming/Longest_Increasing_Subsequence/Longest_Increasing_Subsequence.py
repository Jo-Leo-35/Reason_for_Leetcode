from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []
        
        for num in nums:
            # If sub is empty or num is strictly greater than the last element
            if not sub or num > sub[-1]:
                sub.append(num)
            else:
                # Find the first element in sub that is >= num and replace it
                idx = bisect.bisect_left(sub, num)
                sub[idx] = num
                
        # Length of sub matches the length of the longest increasing subsequence
        return len(sub)
