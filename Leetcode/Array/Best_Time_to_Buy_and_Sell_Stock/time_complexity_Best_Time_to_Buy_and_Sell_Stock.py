from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # TIME & SPACE OPTIMAL: Single Pass
        # Time: O(N) — one scan, optimal since we must read every price
        # Space: O(1) — two variables only
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price

        return max_profit
