'''
演算法步驟：
1. 將輸入的區間陣列以「開始時間 (start)」從小到大進行排序。
2. 建立一個 `merged` 陣列做為最終回傳的結果，一開始先將排序後的第一個區間放入 `merged` 中。
3. 開始遍歷剩餘的每一個區間 `curr`：
4. 取出 `merged` 陣列的最末端區間 `last` 進行比對。
5. 判斷是否有交集：如果 `curr` 的起始時間「小於或等於」`last` 的結束時間，代表兩個區間重疊了。
   - 此時進行合併，更新 `last[1] = max(last.end, curr.end)`。注意要取 Max，防範被包含的情況。
6. 如果沒有交集，代表這是一個全新的獨立區間，將 `curr` 接在 `merged` 陣列的後面。
7. 線性走訪完畢，回傳 `merged`。
'''
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
            
        intervals.sort(key=lambda x: x[0])
        merged = [intervals[0]]
        
        for curr in intervals[1:]:
            last = merged[-1]
            
            # 若發生重疊
            if curr[0] <= last[1]:
                last[1] = max(last[1], curr[1])
            else:
                # 無重疊，加入新的區間
                merged.append(curr)
                
        return merged
