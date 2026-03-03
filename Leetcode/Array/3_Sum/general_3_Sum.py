'''
演算法步驟：
1. 先將輸入的整數陣列 `nums` 從小到大進行排序。排序是為了能有效率使用雙指針，且能快速略過重複的數字以避免相同的解答。
2. 使用一個迴圈走訪陣列，將選定的當下數字當作解答組合的第一個元素 `nums[i]`。
3. 防止重複：如果 `nums[i]` 跟上一個檢查過的數字 `nums[i-1]` 相同，直接跳過 (continue)。
4. 提早結束：因為陣列已排序，如果第一顆最小的數字 `nums[i]` 就已經大於 0 了，那後面的人不論怎麼加都不可能等於 0，直接跳出迴圈 (break)。
5. 將剩下的尋找範圍設定為 `left = i + 1` 和 `right = len(nums) - 1`，這成了一個 2Sum 問題。
6. 當 `left < right` 時計算三者的總和 `total`：
   - 如果 `total < 0`，代表和太小，將 `left` 往右移去找更大的數字。
   - 如果 `total > 0`，代表和太大，將 `right` 往左移去找更小的數字。
   - 如果 `total == 0`，找到合法解了！把這三個數字存入結果陣列中。
7. 取出合法解後，必須馬上讓 `left` 跟 `right` 越過跟他們長得一模一樣的鄰居，確保答案組合不重複。
8. 兩端點更新後繼續尋找，直到走訪完成。
'''
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()
        
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            if nums[i] > 0:
                break
                
            left, right = i + 1, len(nums) - 1
            
            while left < right:
                total_sum = nums[i] + nums[left] + nums[right]
                
                if total_sum < 0:
                    left += 1
                elif total_sum > 0:
                    right -= 1
                else:
                    res.append([nums[i], nums[left], nums[right]])
                    
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                        
                    left += 1
                    right -= 1
                    
        return res
