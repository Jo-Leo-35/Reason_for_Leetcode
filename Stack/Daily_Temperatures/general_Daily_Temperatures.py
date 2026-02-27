'''
演算法步驟（嚴格遞減單調棧 Monotonic Decreasing Stack）：
1. 我們建立一個和原陣列等長的解答陣列 `ans`，預設全填 0。
2. 建立一個空的 `stack`。注意：我們在 Stack 裡存放的是溫度的「Index (索引)」，而不是溫度本體！因為要算天數差距，Index 是必備的。
3. 歷遍所有的溫度陣列：
   - 每拿到今天的新溫度 `current_temp`，我們就去問 Stack 這個「歷史包袱回收站」。
   - 如果 Stack 裡面有東西，而且今天的溫度「大於」Stack 頂端的那位老兄（昨天或更早以前的某個低溫）。
   - 太好了！那位老兄終於等到比他溫暖的日子了！我們把他從 Stack 裡面 `pop()` 出來，獲得他當初的 `prev_day_index`。
   - 解答來了：他等了幾天？就是 `今天 Index - 過去 Index`。我們把這個差距寫進解答陣列裡：`ans[prev_day_index] = i - prev_day_index`。
   - 只要 Stack 裡面的老兄一直比今天冷，我們就持續進行這個解放儀式。
4. 儀式結束後，把今天的 `Index` 也推入 Stack 裡等待未來的解放。
5. O(N) 一擊必殺的時間複雜度。
'''
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        stack = []
        
        for i, current_temp in enumerate(temperatures):
            while stack and current_temp > temperatures[stack[-1]]:
                prev_day_index = stack.pop()
                ans[prev_day_index] = i - prev_day_index
            stack.append(i)
            
        return ans
