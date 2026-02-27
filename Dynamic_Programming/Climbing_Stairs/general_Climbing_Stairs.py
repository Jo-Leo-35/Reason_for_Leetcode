'''
演算法步驟：
1. 這是最標準的一維動態規劃，使用一個長度為 N+1 的陣列 `dp` 來紀錄爬到每一階的方法數。
2. 初始條件：`dp[1] = 1`, `dp[2] = 2`。
3. 從第 3 階開始，由於每次只能爬 1 階或 2 階，所以爬到第 `i` 階的方法數必定等於「爬到第 `i-1` 階的方法數」加上「爬到第 `i-2` 階的方法數」。
4. 也就是狀態轉移方程式：`dp[i] = dp[i-1] + dp[i-2]`。
5. 迴圈跑到 `n`，回傳 `dp[n]`。時間複雜度 O(N)，空間複雜度 O(N)。
'''
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
            
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
            
        return dp[n]
