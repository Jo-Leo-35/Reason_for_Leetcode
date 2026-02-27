'''
演算法步驟（DFS 遞迴解法 - Time Complexity Equivalent 但常數極小）：
1. 對於判斷圖中是否有 Cycle，有些場合下使用 DFS 的「走訪狀態標記法」會是最迅速的。
2. 我們建立 Graph 的相鄰串列 `adj_list`。
3. 準備一個陣列 `state`，每個節點有三種狀態：
   - `0`: 尚未走訪 (Unvisited)
   - `1`: 正在目前的這條遞迴路徑中盤旋 (Visiting)
   - `2`: 已經完全探索完畢它底下的所有路線且安全無環 (Visited_and_Safe)
4. 對每一堂尚未走訪的課發起 DFS 探索：
   - 進入函數時，立即把這堂課標記為 `1 (Visiting)`。
   - 開始歷遍它的所有相鄰分支。
   - 如果在遞迴往下鑽的過程中，遇到分支的狀態「剛好也是 1 (Visiting)」！這代表我們撞鬼了，從自己身上繞了一圈回來撞到了還沒結束的自己，Cycle 成立！回傳 `False`。
   - 走訪完所有分支都安全無虞後，任務完成，把狀態標記為 `2 (Safe)`，回傳 `True`。
5. 所有課程安全過關，代表圖中無死胡同，回傳 True。
'''
from collections import defaultdict
from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj_list = defaultdict(list)
        for dest, src in prerequisites:
            adj_list[src].append(dest)
            
        state = [0] * numCourses
        
        def has_cycle(node):
            if state[node] == 1:
                return True
            if state[node] == 2:
                return False
                
            state[node] = 1
            
            for neighbor in adj_list[node]:
                if has_cycle(neighbor):
                    return True
                    
            state[node] = 2
            return False
            
        for i in range(numCourses):
            if state[i] == 0:
                if has_cycle(i):
                    return False
                    
        return True
