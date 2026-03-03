'''
演算法步驟：
1. 將所有會議的「開始時間」萃取出來組成一個陣列，並從小到大排序。
2. 將所有會議的「結束時間」萃取出來組成另一個獨立的陣列，並從小到大排序。
3. 準備兩個指標：`s_ptr` 指向開始時間的頭，`e_ptr` 指向結束時間的頭。另外準備 `rooms` 記錄當前人數，`max_rooms` 記錄歷史最高人數。
4. 當 `s_ptr` 還沒走完時（類似雙指針掃描線）：
   - 如果當前的開始時間「小於」當前的結束時間，代表有一場新會議加入了但沒人出去。`rooms += 1`，並讓 `s_ptr` 往前推進。
   - 否則，代表有一場較早的會議已經結束，房間空出來了。`rooms -= 1`，並讓 `e_ptr` 往前推進。
   - 每次變動都更新 `max_rooms`。
5. 這個演算法在極端密集的活動事件中，避免了 Heap 開銷，僅需要單純的比較，時間常數極小。
'''
from typing import List

class Solution:
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals:
            return 0
            
        starts = sorted([i[0] for i in intervals])
        ends = sorted([i[1] for i in intervals])
        
        s_ptr = 0
        e_ptr = 0
        rooms = 0
        max_rooms = 0
        
        while s_ptr < len(starts):
            if starts[s_ptr] < ends[e_ptr]:
                rooms += 1
                s_ptr += 1
            else:
                rooms -= 1
                e_ptr += 1
                
            max_rooms = max(max_rooms, rooms)
            
        return max_rooms
