'''
演算法步驟（Hash Set 源頭尋找 O(N)）：
1. 將原本的連續數字找法，轉變成一個圖論中「一筆畫最長連線」的問題。
2. 因為在陣列中找數字是否有出現需要 O(N) 時間，我們先把所有的整數通通倒進 Python 的 `set` 裡面，這樣未來判斷任何數字存不存在，都只需要 O(1) 的完美時間！
3. 我們用 `for num in num_set:` 開始遍歷 Set 裡的每一個數字（可以視為一種節點）。
4. 【精隨】：我們絕不盲目地從任何點開始往上數。
   - 對於 `num`，我們去問 Set 說：「你這裡有出現比這個數字小 1 的傢伙 (`num - 1`) 嗎？」
   - 如果有！代表這個 `num` 根本不配當作一個連續序列的開頭，他只是條跟班狗，我們立刻跳過他 (Continue)。
   - 如果沒有 `num - 1`！代表他就是某條序列真正的創世始祖 (源頭)！
5. 發現始祖後，我們才準備踏上旅程。設 `curr_num = num`，長度計數 `curr_streak = 1`。
6. 開始用 `while` 迴圈往上問 Set：「`curr_num + 1` 在不在你這？」如果在，`curr_num` 就一直往上走，長度 `curr_streak` 就一直加一。
7. 當走投無路斷掉的時候，把這條線的長度跟歷史冠軍對決 `max(longest, curr_streak)`。
8. 由於每一個數字最多只會被身為始祖的人探訪一次，整體時間複雜度 O(N)，空間複雜度 O(N)。
'''
from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0
        
        for num in num_set:
            if (num - 1) not in num_set:
                curr_num = num
                curr_streak = 1
                
                while (curr_num + 1) in num_set:
                    curr_num += 1
                    curr_streak += 1
                    
                longest = max(longest, curr_streak)
                
        return longest
