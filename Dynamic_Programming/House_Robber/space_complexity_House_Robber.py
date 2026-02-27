'''
演算法步驟（空間最佳化）：
1. 觀察 `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`，我們發現我們只需要維持前兩筆歷史紀錄即可。
2. 我們用 `rob1` 來代表搶到 `i-2` 棟為止的最高金額，用 `rob2` 代表搶到 `i-1` 棟為止的最高金額。
3. 走訪每棟房子的金額 `money`：
   - 當前的最佳選法 `temp = max(money + rob1, rob2)`。
   - 把 `rob1` 的身份讓給 `rob2`。
   - 把 `rob2` 更新為剛剛算出的 `temp`。
4. 走完陣列後，`rob2` 即為最大金額。額外空間複雜度 O(1)。
'''
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        rob1, rob2 = 0, 0
        
        for money in nums:
            temp = max(money + rob1, rob2)
            rob1 = rob2
            rob2 = temp
            
        return rob2
