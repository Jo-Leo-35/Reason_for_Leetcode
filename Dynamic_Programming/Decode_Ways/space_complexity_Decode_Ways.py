'''
演算法步驟（狀態滾動壓縮 O(1) 空間）：
1. 觀察轉移方程 `dp[i] += dp[i-1]` 與 `dp[i-2]`。
2. 這跟 Climbing Stairs 一模一樣，我們只依賴前兩個狀態。
3. 宣告 `prev2` 代表 i-2 的方法數，`prev1` 代表 i-1 的方法數。
4. 每次迴圈產生 `curr = 0`，若單位數字合法則 `curr += prev1`，若雙位數字合法則 `curr += prev2`。
5. 推移狀態 `prev2 = prev1`, `prev1 = curr`。 
'''
class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
            
        prev2 = 1 
        prev1 = 1 
        
        for i in range(1, len(s)):
            curr = 0
            
            if s[i] != '0':
                curr += prev1
                
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                curr += prev2
                
            prev2 = prev1
            prev1 = curr
            
        return prev1
