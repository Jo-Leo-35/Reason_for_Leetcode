'''
演算法步驟（二分搜尋的相對順序判別）：
1. 給定一個被旋轉過的遞增陣列，要求在 O(log N) 內搜尋 `target`。
2. 配置左右指針 `left = 0`, `right = len(nums) - 1`。
3. 進入 `while left <= right:` 迴圈，算出中间位址 `mid`。
4. 買中樂透：如果 `nums[mid] == target`，歡呼並回傳 `mid`。
5. 沒中樂透的話，我們必須判斷現在自己到底站在左半邊峭壁，還是右半邊峽谷。
6. 情況 A：如果 `nums[left] <= nums[mid]`，這代表從左邊到中間這塊地盤是「完美排序、沒有斷層」的！
   - 我們接著可以安心地去判斷 `target` 有沒有剛好落在這個完美地盤內：
   - 如果 `nums[left] <= target < nums[mid]`，那我們大聲宣告標的物就在這裡面，`right = mid - 1`。
   - 否則，標的物一定在另一半荒野，`left = mid + 1`。
7. 情況 B：如果不是 A，那代表從中間到右邊 `nums[mid:right+1]` 這塊地盤是完美排序的！
   - 同理，我們查驗 `target` 是否舒舒服服地躺在右邊這段完美範圍內：
   - 如果 `nums[mid] < target <= nums[right]`，鎖定範圍 `left = mid + 1`。
   - 否則標的物在左半邊荒野，`right = mid - 1`。
8. 迴圈找不到就回傳 -1。
'''
from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
                
            # 左半段呈現完美遞增
            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            # 右半段呈現完美遞增
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
                    
        return -1
