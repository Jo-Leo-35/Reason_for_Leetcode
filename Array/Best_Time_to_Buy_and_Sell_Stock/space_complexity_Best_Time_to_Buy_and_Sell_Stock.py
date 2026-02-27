from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        # SPACE OPTIMAL: Single Pass (same as time-optimal — O(1) space, O(N) time)
        # Time: O(N)
        # Space: O(1) — tracking only min_price and max_profit
        # No meaningful space/time trade-off exists for this problem;
        # one pass is already optimal in both dimensions.
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            min_price = min(min_price, price)
            max_profit = max(max_profit, price - min_price)

        return max_profit
