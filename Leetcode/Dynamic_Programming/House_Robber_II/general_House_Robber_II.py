'''
演算法步驟：
1. 房子變成了環形（第一棟跟最後一棟相連），這代表我們「絕對不能同時搶第一棟跟最後一棟」。
2. 所以我們把問題拆解成兩個傳統的線性 House Robber 問題：
   - 情境一：忍痛放棄最後一棟，只考慮搶 Array 的範圍 `nums[0]` 到 `nums[N-2]`。
   - 情境二：忍痛放棄第一棟，只考慮搶 Array 的範圍 `nums[1]` 到 `nums[N-1]`。
3. 建立一個 helper function 用 O(1) 空間運算線性的最高搶劫金額。
4. 對上面兩種情境分別呼叫 helper function，並取出這兩個情境的最大值 `max(Case1, Case2)` 即可。
'''
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0: return 0
        if n == 1: return nums[0]
            
        def helper(houses: List[int]) -> int:
            rob1, rob2 = 0, 0
            for money in houses:
                temp = max(money + rob1, rob2)
                rob1 = rob2
                rob2 = temp
            return rob2
            
        return max(helper(nums[:-1]), helper(nums[1:]))
