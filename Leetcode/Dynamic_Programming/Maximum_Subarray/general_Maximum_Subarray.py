'''
演算法步驟（Kadane's Algorithm）：
1. 這是解決最大子陣列和的傳奇演算法。核心精神是「如果前面積累的財富是負債，那就勇敢切斷過去，從現在重新開始」。
2. 用兩個變數：`max_so_far` 記錄歷史觀測到的最大子陣列和（初始化為數組第一個元素）；`current_max` 記錄「以當前元素作為結尾時」的最大和。
3. 開始遍歷陣列剩下的元素：
   - 面對當下這個元素，如果你把它和上一手（`current_max`）加在一起，比它自己單兵作戰（`num`）還要慘！這代表上一手是拖油瓶（負數）。
   - 所以我們選擇拋棄過去：`current_max = max(num, current_max + num)`。
   - 每次決定完 `current_max` 的新身份，就去挑戰並更新歷史最高 `max_so_far`。
4. O(N) 一次遍歷，O(1) 空間。
'''
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        max_so_far = nums[0]
        current_max = nums[0]
        
        for num in nums[1:]:
            current_max = max(num, current_max + num)
            max_so_far = max(max_so_far, current_max)
            
        return max_so_far
