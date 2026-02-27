'''
演算法步驟：
1. 建立一個長度為 `amount + 1` 的陣列 `dp`，`dp[i]` 代表「湊出金額 i 最少需要幾枚硬幣」。
2. 將陣列初始化為一個大到不可能的數字，例如 `amount + 1`，用來在最後判斷此金額是否無解。初始化 `dp[0] = 0` (湊 0 元不需硬幣)。
3. 外層迴圈歷遍所有的金額：`a` 從 1 一路數到 `amount`。
4. 內層迴圈歷遍所有的硬幣面額 `c`：
   - 確認這個硬幣真的塞得下：如果 `a - c >= 0`。
   - 這代表如果我們選擇撿起這枚硬幣 `c`，那麼剩下的金額就是 `a - c`。
   - 所以湊出金額 `a` 的選項之一，就是「湊出金額 `a-c` 的最少硬幣數加上這枚硬幣 (也就是 + 1)」。
   - `dp[a] = min(dp[a], 1 + dp[a - c])`，從所有的硬幣中挑出能給出最小數字的途徑。
5. 最後如果 `dp[amount]` 還是當初那個荒謬的大數字，代表所有的硬幣都湊不出這個金額，回傳 -1。否則回傳 `dp[amount]`。
'''
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # 初始化為絕對達不到的上限值
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        
        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])
                    
        return dp[amount] if dp[amount] != amount + 1 else -1
