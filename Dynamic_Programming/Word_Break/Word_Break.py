from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        # 1D DP optimized by checking dictionary words' lengths
        # dp[i] is True if s[0:i] can be broken down
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for word in wordDict:
                word_len = len(word)
                if i >= word_len and dp[i - word_len] and s[i - word_len:i] == word:
                    dp[i] = True
                    break
                    
        return dp[n]
