'''
演算法步驟：
1. 目標是找出兩個字串 `text1` 和 `text2` 的最長共同子序列長度。
2. 建立一個二維 DP 陣列 `dp`，大小為 `(text1長度 + 1) x (text2長度 + 1)`，初始化為 0。`dp[i][j]` 代表 `text1` 的前 `i` 個字元和 `text2` 的前 `j` 個字元的 LCS 長度。
3. 使用兩層迴圈走訪兩個字串的所有字元組合：
4. 如果遇到兩個字元相同 (`text1[i-1] == text2[j-1]`)：
   - 代表他們可以共同為 LCS 貢獻長度 1。
   - 所以 `dp[i][j] = dp[i-1][j-1] + 1` (左上角的值加一)。
5. 如果兩個字元不同：
   - 代表當前這兩個字元不能同時為 LCS 做出貢獻，我們必須從「少考慮 text1 的這一個字元」或是「少考慮 text2 的這一個字元」的歷史中挑一個最大的。
   - `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (取正上方或正左方的最大值)。
6. 最終回傳最右下角的 `dp[m][n]`，時間與空間複雜度皆為 O(M * N)。
'''
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                    
        return dp[m][n]
