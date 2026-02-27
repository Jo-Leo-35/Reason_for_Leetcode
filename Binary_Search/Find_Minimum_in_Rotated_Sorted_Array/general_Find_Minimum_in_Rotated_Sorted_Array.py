'''
演算法步驟（二分搜尋與斷層分析）：
1. 這是要求 O(log N) 時間找出旋轉陣列最小值的問題。核心精神是「去找那個導致順序崩壞的反曲點」。
2. 準備指針 `left = 0`, `right = len(nums) - 1`。
3. 進入 `while left < right` 迴圈：
4. 第一道防線（極為重要）：如果當下我們涵蓋的這段區間，最左邊的值竟然「嚴格小於」最右邊的值 `nums[left] < nums[right]`！
   - 這代表什麼？這代表這段區間根本沒有旋轉，它是一段完美的上升梯子！
   - 所以最小值毫無疑問就是最左邊的那格 `nums[left]`，直接 return 放工！
5. 若防線沒觸發，我們算出中間點 `mid`。
6. 判斷斷層在哪邊：
   - 拿 `nums[mid]` 和最左邊的 `nums[left]` 比較。如果 `nums[mid] >= nums[left]`，代表左半邊是一路攀升的完美世界，反曲點隱藏在右半邊！
     - 所以我們縮小範圍 `left = mid + 1`。
   - 否則，這代表 `mid` 本身已經掉進懸崖下了，或是左半邊就已經有斷層了！
     - 所以反曲點一定在左半部，或者 `mid` 本身就是那個谷底。
     - 所以我們縮小範圍 `right = mid`。
7. 從迴圈出來時，`left` 和 `right` 一定重疊，那格就是全局最小值。
'''
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        
        while left < right:
            # 區間已經完全遞增，左端點即為最小
            if nums[left] < nums[right]:
                return nums[left]
                
            mid = left + (right - left) // 2
            
            # 左半段遞增，代表最小值在右半段的深淵中
            if nums[mid] >= nums[left]:
                left = mid + 1
            # 否則最小值包藏在左半段或是 mid 本身
            else:
                right = mid
                
        return nums[left]
