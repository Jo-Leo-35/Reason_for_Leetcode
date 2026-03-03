'''
演算法步驟：
1. 這一題是滑動窗口 (Sliding Window) 加上頻率統計的經典題型。
2. 我們用一個 Hash Map (或是長度 26 的陣列) `count` 來記錄目前窗口內每個字元出現的次數。
3. 同時維護一個整數 `max_freq`，代表「在目前這個視窗中，出現最多次的那個字元的次數」。
4. 設立左右指針 `left = 0`, `right = 0`。讓 `right` 不斷向右推進：
   - 把 `s[right]` 收進字典裡 `count[s[right]] += 1`。
   - 更新歷史最大頻率：`max_freq = max(max_freq, count[s[right]])`。
5. 判斷這個窗口是不是「不合法」了？
   - 不合法的條件是：「視窗長度」減掉「出現最多次的字元數」，剩下的所有廢物字元數量，大於我們可以替換的額度 `k`。
   - 也就是 `(right - left + 1) - max_freq > k`。
6. 如果不合法了，這時候我們不需要像普通 Sliding Window 一樣把 `left` 縮到合法為止。我們只需要把 `left` 往右平移一格就好！
   - 因為我們只關心「歷史上出現過最大的窗口」，所以當窗口不合法時，我們整體往右滑動（不縮小長度），看看能不能剛好接住一個合法的新字元。
   - `count[s[left]] -= 1`
   - `left += 1`
7. 過程中記錄最大的視窗長度 `max_len = max(max_len, right - left + 1)`。O(N) 時間，O(1) 空間（因為只有 26 個字母）。
'''
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        max_freq = 0
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            max_freq = max(max_freq, count[s[right]])
            
            # 若需替換的字元數 > k，代表此子串不合法，平移窗口
            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
                
            max_len = max(max_len, right - left + 1)
            
        return max_len
