'''
演算法步驟：
1. 目標是找出能不能用字典裡的單詞拼湊出整個字串 `s`。
2. 建立一個布林值陣列 `dp`，`dp[i]` 代表「字串 s 的前 i 個字元是否可以被成功分割」。
3. 初始條件 `dp[0] = True` (空字串一定可以)。
4. 讓 `i` 從 1 走到 n（字串長度）：
   - 對於每一個 `i`，我們去遍歷字典 `wordDict` 裡的每個單字。
   - 如果當前掃描的總長度 `i` 大於等於這個單字的長度（這代表切得下這個字）。
   - 且「切掉這個字之後，剩下的前面那段 (`dp[i - len(word)]`) 也是可以被完美分割的」。
   - 且「字串從 `i-len(word)` 到 `i` 這段子字串真的完全等於這個單字」。
   - 太棒了！那麼前 `i` 個字元就保證可以被拼湊出來，我們設 `dp[i] = True` 並立刻 `break`（只要有一種成功拼合方式就好）。
5. 最終回傳 `dp[n]`。這是一種剪枝過的高雅 DP 寫法。
'''
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for word in wordDict:
                word_len = len(word)
                if i >= word_len and dp[i - word_len] and s[i - word_len:i] == word:
                    dp[i] = True
                    break
                    
        return dp[n]
