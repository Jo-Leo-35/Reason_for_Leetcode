'''
演算法步驟（HashMap 跳躍查找）：
1. Set 去重法的缺點是，當發生碰撞時，`left` 得一格一格慢慢往前走並刪除 Set 中的元素。如果衝突的字元正好在很左邊，我們浪費了大量 O(N) 一步一步走的迴圈次數。
2. 我們改用一個 `HashMap` (字典)，不僅紀錄了字元，更記錄了該字元「最後一次出現所在的 Index」。
3. 讓 `right` 不斷向右掃描。
4. 如果我們發現 `s[right]` 出現在字典中，而且它在字典記錄的位置「大於等於現今的 left」：
   - 這直接宣判了我們正在維護的有效視窗內真的包進了一顆毒瘤！
   - 我們不浪費時間一步步踢人，我們直接讓 `left` 瞬間移動，飛越避開那顆毒瘤，降落在「衝突字元的原始索引 + 1」的位置。
5. 每次不管有沒有衝突，都把 `s[right]` 更新進字典裡。並挑戰歷史最長長度。
6. 這個技巧達成了嚴格且極致的單次 O(N) 走訪時間複雜度。
'''
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            if char in char_index_map and char_index_map[char] >= left:
                # 瞬間跳躍閃避
                left = char_index_map[char] + 1
                
            char_index_map[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len
