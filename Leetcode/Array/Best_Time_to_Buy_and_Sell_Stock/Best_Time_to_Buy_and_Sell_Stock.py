from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # Greedy tracker: O(N) time, O(1) space
        if not prices:
            return 0
            
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
                
        return max_profit
