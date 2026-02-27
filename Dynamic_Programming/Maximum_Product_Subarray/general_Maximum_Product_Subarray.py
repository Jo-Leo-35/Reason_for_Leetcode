'''
演算法步驟：
1. 本題是 Maximum Subarray 的乘法變體。難點在於「負負得正」：一個很小的負數，如果未來遇到另一個負數，會瞬間暴增成極大的正數。
2. 所以我們必須同時精準地維護兩個狀態：「到達目前這個元素時的最大可能乘積 `curr_max`」與「最小可能乘積 `curr_min`」。
3. 初始化 `res`, `curr_max`, `curr_min` 為陣列的第一個元素。
4. 走訪陣列剩下的元素：
   - 當前遇到一個數字 `num`，如果它是「負數」，太刺激了！因為乘上負數會讓最大變最小、最小變最大。所以我們把 `curr_max` 和 `curr_min` 互換。
   - 接著更新極值：`curr_max = max(num, curr_max * num)` (到底是要跟前面手牽手，還是放棄前面自己開新局？)
   - 同理更新極值：`curr_min = min(num, curr_min * num)`
   - 每次順便挑戰歷史最高紀錄 `res = max(res, curr_max)`。
5. 單純的 O(N) 走訪與 O(1) 的空間開銷。
'''
from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        res = nums[0]
        curr_min, curr_max = nums[0], nums[0]
        
        for i in range(1, len(nums)):
            num = nums[i]
            
            # 若為負數，未來的最大跟最小會顛倒
            if num < 0:
                curr_min, curr_max = curr_max, curr_min
                
            curr_max = max(num, curr_max * num)
            curr_min = min(num, curr_min * num)
            
            res = max(res, curr_max)
                
        return res
