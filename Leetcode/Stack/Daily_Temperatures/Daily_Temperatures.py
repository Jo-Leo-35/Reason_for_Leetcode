from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # Monotonic Decreasing Stack storing indices: O(N) time, O(N) space
        n = len(temperatures)
        ans = [0] * n
        stack = []
        
        for i, current_temp in enumerate(temperatures):
            while stack and current_temp > temperatures[stack[-1]]:
                prev_day_index = stack.pop()
                ans[prev_day_index] = i - prev_day_index
            stack.append(i)
            
        return ans
