'''
演算法步驟（滑動窗口 + Set 去重）：
1. 維護一個滑動窗口，用兩個指標 `left` 和 `right` 定義視窗邊界，以及一個 `HashSet` 來幫忙 O(1) 檢查字元是否有重複出現在視窗中。
2. 讓 `right` 不斷向右推進：
   - 如果 `s[right]` 不在 Set 裡面，太棒了，把它加進去，並把目前的視窗大小 `right - left + 1` 跟歷史最高 `max_len` 比較。
   - 如果 `s[right]` "已經" 在 Set 裡面了。這代表發生了重複碰撞！
3. 發生碰撞時，我們無條件信任 `right` 必須繼續前進。所以我們只好讓 `left` 往右狂奔，沿途把遇到的字元通通從 Set 裡踢掉，直到把那個跟 `s[right]` 相撞的萬惡字元也踢出窗口為止。
4. 踢掉毒瘤後，放心地把新的 `s[right]` 加進去，繼續循環。
'''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
                
            char_set.add(s[right])
            max_len = max(max_len, right - left + 1)
            
        return max_len
