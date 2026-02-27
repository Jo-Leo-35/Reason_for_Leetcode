'''
演算法步驟：
1. 直接宣告並配置好要作為結果輸出的陣列 `ans`，這個陣列的空間不計入時間/空間複雜度的計算。
2. 由左到右掃描原陣列，利用一個常數變數 `left_prod` 記錄累積乘積，並在當前位址寫入 `ans`。
3. 由右到左反向掃描，利用一個常數變數 `right_prod` 記錄右方的累積乘積。
4. 在反向掃描的過程中，將 `right_prod` 乘上 `ans` 原有的值（也就是步驟 2 留下的左邊乘積）。
5. 達到 O(1) 的額外空間複雜度和 O(N) 的時間複雜度，直接回傳 `ans`。
'''
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        ans = [1] * n
        
        left_prod = 1
        for i in range(n):
            ans[i] = left_prod
            left_prod *= nums[i]
            
        right_prod = 1
        for i in range(n - 1, -1, -1):
            ans[i] *= right_prod
            right_prod *= nums[i]
            
        return ans
