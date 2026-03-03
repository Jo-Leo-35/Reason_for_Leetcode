'''
演算法步驟（空間最佳化）：
1. 觀察動態規劃的轉移方程式 `dp[i] = dp[i-1] + dp[i-2]`。
2. 我們發現，計算當前的狀態 `dp[i]` 時，其實只需要用到「前一個」跟「前兩個」的狀態而已，前面的歷史紀錄根本都不需要。
3. 因此我們可以用兩個常數變數 `prev1` 和 `prev2` 來取代長度為 N 的陣列。
4. 每次計算出新的方法數 `curr = prev1 + prev2`。
5. 然後像毛毛蟲一樣往前蠕動：`prev2 = prev1`，`prev1 = curr`。
6. 最後回傳 `prev1` 即可。這樣時間複雜度一樣是 O(N)，但額外空間複雜度降到了極致的 O(1)。
'''
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
            
        prev1 = 2 # 相當於 dp[i-1]
        prev2 = 1 # 相當於 dp[i-2]
        
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
            
        return prev1
