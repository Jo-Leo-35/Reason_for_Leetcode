'''
演算法步驟（基於 Queue/Deque 的時間優先解法）：
1. 我們利用一個雙向佇列 (Deque) 來儲存歷史資料。每次有人呼叫 `hit`，我們就把當前的 timestamp 加進 Deque 的尾巴。
2. 由於 timestamp 保證是嚴格遞增的（時間只會往前走），Deque 裡的數字自然就是從小到大排序的。
3. `hit` 的時間複雜度是 O(1)。
4. 當有人呼叫 `getHits(timestamp)` 時，我們開始檢查 Deque 的「頭部」。
5. 因為頭部是最早發生 hit 的地方，如果發現 `timestamp - 佇列頭部的時間 >= 300`，代表這筆記錄已經超過 300 秒（5 分鐘）過期了！我們直接把它從頭部 Pop 彈出。
6. 這個「檢查並彈出」的過程一直持續，直到佇列頭部的資料是在 300 秒內為止，或者滿載而歸佇列清空了。
7. 清理完畢後，直接回傳 `len(Deque)`，這個長度就是 5 分鐘內的所有命中次數！
8. 這個做法好在處理 getHits 時非常直覺，但極端情況下如果有數以萬計的 hit，會吃掉 O(N) 的記憶體空間。
'''
from collections import deque

class HitCounter:

    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        while self.hits and timestamp - self.hits[0] >= 300:
            self.hits.popleft()
            
        return len(self.hits)
