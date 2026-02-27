class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # Guarantee text2 is shorter to minimize space
        if len(text1) < len(text2):
            text1, text2 = text2, text1
            
        m, n = len(text1), len(text2)
        # Space optimization using only 1D array of length min(m, n)
        prev = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev = curr
            
        return prev[n]
