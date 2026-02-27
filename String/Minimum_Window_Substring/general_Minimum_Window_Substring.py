'''
演算法步驟：
1. 這一題是滑動窗口 (Sliding Window) 解決涵蓋問題的最經典模板。
2. 首先用一個 Hash Map (字典) `target_counts` 把目標字串 `t` 裡面的每個字元與需求數量統計好。
3. 同時計算一個變數 `required_unique_chars`，代表有幾種「不同」的字元需要被收集滿足。
4. 維護一個滑動窗口：`left` 指針固定，`right` 指針開始向右擴展。
5. 我們用另一個字典 `window_counts` 記錄目前窗口吃進了哪些字元，並準備一個變數 `formed` 來記錄「已經完全達標的字元種類有幾種」。
6. 當 `right` 掃描到一個 `t` 裡面的字元，且吃進來的數量「剛好」等於 `target_counts` 要求的數量時，代表一種字元達標了，`formed += 1`。
7. 【精華】：當 `formed == required_unique_chars` (代表目前窗口已經涵蓋了所有的 `t`)。這時我們發現了一個潛在解。
8. 於是我們嘗試去縮小這個窗口！讓 `left` 開始向右移動，把一些不重要的垃圾字元吐出去，試圖挑戰「更短」的紀錄。如果吐出去的字元是必要的，導致 `formed` 被扣 1，則停止縮小，讓 `right` 繼續往外找。
9. 全域紀錄下每一次嘗試搜縮完成後的歷史最短長度，最後裁切字串回傳。
'''
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(s) < len(t):
            return ""
            
        from collections import Counter
        target_counts = Counter(t)
        required_unique_chars = len(target_counts)
        
        left = 0
        window_counts = {}
        formed = 0
        
        # 紀錄歷史最短字串的資料 (長度, 左邊界, 右邊界)
        ans = (float('inf'), None, None)
        
        for right in range(len(s)):
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            
            if char in target_counts and window_counts[char] == target_counts[char]:
                formed += 1
                
            # 當窗口內的條件完全被滿足時
            while left <= right and formed == required_unique_chars:
                char_left = s[left]
                
                # 如果比歷史最短紀錄還短，就更新
                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right)
                    
                window_counts[char_left] -= 1
                
                if char_left in target_counts and window_counts[char_left] < target_counts[char_left]:
                    formed -= 1
                    
                left += 1
                
        return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]
