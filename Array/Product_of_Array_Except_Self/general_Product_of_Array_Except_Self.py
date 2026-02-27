'''
演算法步驟：
1. 建立兩個與原陣列等長的陣列 `left` 和 `right`，用來記錄該位置「左邊所有數字的乘積」與「右邊所有數字的乘積」。
2. 由左至右掃描 `nums`，將前綴乘積依序寫入 `left` 陣列（`left[i] = left[i-1] * nums[i-1]`），`left[0]` 預設為 1。
3. 由右至左掃描 `nums`，將後綴乘積依序寫入 `right` 陣列（`right[i] = right[i+1] * nums[i+1]`），`right[-1]` 預設為 1。
4. 再次掃描長度為 N 的陣列，將對應的 `left[i]` 與 `right[i]` 相乘，即為去除自己以外的總乘積。
5. 回傳結果陣列。
'''
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        left = [1] * n
        right = [1] * n
        res = [0] * n
        
        # 建立左前綴陣列
        for i in range(1, n):
            left[i] = left[i - 1] * nums[i - 1]
            
        # 建立右後綴陣列
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] * nums[i + 1]
            
        # 左右相乘
        for i in range(n):
            res[i] = left[i] * right[i]
            
        return res
