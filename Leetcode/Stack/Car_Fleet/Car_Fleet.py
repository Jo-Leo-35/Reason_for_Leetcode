from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # Sort and Monotonic Stack strategy: O(N log N) time, O(N) space
        if not position:
            return 0
            
        cars = sorted(zip(position, speed), reverse=True)
        stack = []
        
        for pos, spd in cars:
            duration = (target - pos) / spd
            
            if not stack:
                stack.append(duration)
            else:
                # If duration > stack[-1], it's a new slower fleet that won't catch up
                if duration > stack[-1]:
                    stack.append(duration)
                    
        return len(stack)
