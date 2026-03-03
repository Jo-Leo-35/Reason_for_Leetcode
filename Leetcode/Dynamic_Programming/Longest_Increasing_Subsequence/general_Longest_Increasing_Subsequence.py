'''
演算法步驟：
1. 傳統的 DP 思維。我們準備一個陣列 `dp`，長度等於 `nums`，裡面的每一格 `dp[i]` 代表「以 `nums[i]` 為結尾的子序列，最長的長度是多少」。初始化每格皆為 1。
2. 使用兩層迴圈：外層 `i` 從 0 到 n-1，內層 `j` 從 0 掃描到 `i-1`。
3. 如果發現前面的某個數字 `nums[j] < nums[i]` (代表可以形成嚴格遞增)：
   - 我們就把 `nums[i]` 接在以 `j` 為結尾的子序列後面。
   - `dp[i]` 更新為 `max(dp[i], dp[j] + 1)`。
4. 全局歷史最大的 `dp` 值即為最長遞增子序列長度。
5. 時間複雜度為 $O(N^2)$。如果是面試，這個解法常常只能拿弱聘。
'''
from typing import List

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        dp = [1] * len(nums)
        max_len = 1
        
        for i in range(1, len(nums)):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
                    
            max_len = max(max_len, dp[i])
            
        return max_len
