'''
演算法步驟：
1. 長度為 N 的動態規劃陣列 `dp`，`dp[i]` 代表「搶劫前 i 棟房子所能得到的最高金額」。
2. 對於每一棟房子，小偷有兩個選擇：
   - 選擇A：「不搶」這棟房子，則目前的最高金額就等於搶前一棟的金額 `dp[i-1]`。
   - 選擇B：「搶」這棟房子，因為不能連續搶兩棟，所以必須加上搶「前兩棟」的金額 `dp[i-2] + nums[i]`。
3. 狀態轉移方程式為：`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`。
4. 初始化 `dp[0]` 與 `dp[1]`，然後從第 2 棟房子走到最後一棟，回傳最後的最高金額。
'''
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums: return 0
        if len(nums) == 1: return nums[0]
        
        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        
        for i in range(2, len(nums)):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
            
        return dp[-1]
