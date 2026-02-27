'''
演算法步驟（雙指針法）：
1. 我們有兩根柱子要形成一個水桶。水桶能裝的水量公式是 `底部寬度 * 左右較矮的那根柱子的高度`。
2. 要裝最多的水，我們一開始先窮極「寬度」的極限。所以把 `left` 放在最左邊(0)，把 `right` 放在最右邊(N-1)。
3. 當 `left < right` 迴圈持續運行：
   - 先計算當下這兩根柱子能裝的水量：`(right - left) * min(height[left], height[right])`。
   - 挑戰歷史最高水量 `max_water` 並且更新它。
4. 【貪婪精神】：現在我們必須捨棄一根柱子並往內移動，該動誰呢？
   - 由於寬度注定會縮小，我們要讓水量變大唯一的希望，就是期盼未來的柱子「越高越好」。
   - 如果我們動了已經比較高的那根，水位天花板還是受限於原來的矮子，水量絕對縮水！
   - 所以，我們毫無懸念地把「比較矮的那根柱子」淘汰掉，往內尋找下一個潛在的高個子。
   - 若 `height[left] < height[right]`，則 `left += 1`；否則 `right -= 1`。
5. O(N) 走訪完成後回傳 `max_water`。
'''
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        max_water = 0
        
        while left < right:
            current_water = (right - left) * min(height[left], height[right])
            max_water = max(max_water, current_water)
            
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_water
