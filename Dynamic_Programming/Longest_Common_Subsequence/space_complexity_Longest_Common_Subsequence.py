'''
演算法步驟（空間最佳化 - 滾動陣列）：
1. 觀察 2D DP 的轉移方程：`dp[i][j]` 只需要用到「當前這一列 `dp[i][j-1]`」、「上一列的同一個位置 `dp[i-1][j]`」以及「上一列的前一個位置 `dp[i-1][j-1]`」。
2. 這代表在運算過程中，我們根本不需要存下整個 M * N 的矩陣，我們只需要保留「前一列 (prev)」跟「當前列 (curr)」的長度就夠了。
3. 更進一步，為了讓一維陣列的長度盡可能小，我們讓 `text2` 永遠是指向兩者中較短的那個字串。
4. 初始化前一列 `prev = [0] * (n + 1)`，開始外層迴圈遍歷較長的字串。
5. 內層迴圈產生一個 `curr` 陣列來記錄當前這橫列的結果。
6. 計算邏輯和原本相同。計算完一整排之後，推進狀態 `prev = curr`。
7. 最後回傳 `prev[-1]`。時間複雜度 O(M * N)，空間複雜度降至 O(min(M, N))。
'''
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        if len(text1) < len(text2):
            text1, text2 = text2, text1
            
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                else:
                    curr[j] = max(prev[j], curr[j - 1])
            prev = curr
            
        return prev[-1]
