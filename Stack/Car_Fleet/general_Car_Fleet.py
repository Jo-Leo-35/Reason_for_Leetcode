'''
演算法步驟（排序 + 單調棧）：
1. 我們把每輛車子的「起點位置」和「速度」打包成 Tuple，建立一個車隊陣列。
2. 按照起點位置「由大到小（從靠近終點到遠離終點）」進行掃描（Sorted 降冪）。這是最關鍵的思想！因為後面的快車如果追上前方的慢車，必須遷就慢車的速度。
3. 準備一個 `stack` 來裝載最終形成的車隊。
4. 對於每一輛車（從最靠近終點的一路往後）：
   - 計算這輛車在「沒有任何人阻擋」的情況下，到達終點所需的真實秒數：`duration = (target - pos) / spd`。
   - 如果 `stack` 是空的，代表它是這條路最前面的車，成為一個新車隊的隊長，直接加入 `stack.append(duration)`。
   - 否則，這輛車是在隊長的後面。它能不能追上前方的最後一團車隊（也就是 `stack[-1]` 的秒數）？
   - 如果這輛車需要花費的秒數 `duration`「大於」前方車隊抵達終點的秒數，代表它比較慢，這輩子都追不上前方的車！
   - 所以，它自己獨立成為了一個「新的車隊」，我們把它 `stack.append(duration)`。
   - 反之，如果它比較快（所需時間少），那它必定會在終點前撞上前方車隊，所以它直接融入了前方的車隊中（不加入 stack）。
5. 歷遍完後，Stack 裡面有幾種行駛時間，就代表最終有幾個車隊 `len(stack)`。O(N log N) 時間。
'''
from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        if not position:
            return 0
            
        cars = sorted(zip(position, speed), reverse=True)
        stack = []
        
        for pos, spd in cars:
            duration = (target - pos) / spd
            
            if not stack:
                stack.append(duration)
            else:
                if duration > stack[-1]:
                    stack.append(duration)
                    
        return len(stack)
