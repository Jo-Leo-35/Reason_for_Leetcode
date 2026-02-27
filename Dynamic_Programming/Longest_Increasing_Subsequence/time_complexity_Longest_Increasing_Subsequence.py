'''
演算法步驟（Patience Sorting / 二分搜尋法）：
1. 這是要求 $O(N \log N)$ 時間複雜度的面試魔道最佳解。
2. 建立一個輔助陣列 `sub`，用來儲存潛在的最長遞增子序列元素（注意：裡面放的數字可能不是真實的子序列組合，但其『長度』絕對跟真實答案一樣長！）。
3. 走訪 `nums` 裡的每一個數字 `num`：
   - 如果 `sub` 是空的，或是 `num` 嚴格大於 `sub` 裡面的最後（也是最大）的一個元素，那就直接把它接在 `sub` 後面（擴充最大長度！）
   - 否則，拿這個 `num` 在 `sub` 內部進行「二分搜尋」，找到**第一個大於等於** `num` 的位置，然後無情地「取代」它。
4. 取代的精神在於：留得青山在。用越小的數字當樁腳，未來能接納更多數字來增長長度的潛力就越大。
5. 掃描完畢，回傳 `len(sub)`。
'''
from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []
        
        for num in nums:
            # 第一個數字，或大於尾端數字
            if not sub or num > sub[-1]:
                sub.append(num)
            else:
                # 二分搜找到第一個大於等於它的障礙物位置，替換掉使其變小
                idx = bisect.bisect_left(sub, num)
                sub[idx] = num
                
        return len(sub)
