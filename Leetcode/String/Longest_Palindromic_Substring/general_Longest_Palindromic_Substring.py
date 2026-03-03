'''
演算法步驟（Expand Around Center 強棒解法）：
1. 我們把每個字元都當成「可能是迴文大爆發的中心點」。但迴文有兩種：奇數長度（如 "aba"，以 b 為中心），和偶數長度（如 "abba"，以中間空隙為中心）。
2. 用一個迴圈 `i` 橫掃整個字串長度。
3. 對於每個 `i`，我們進行兩次向外擴張 (Expand)：
   - 奇數長度擴張：把 `l` 和 `r` 都設在 `i` 的位置，向兩旁查看字符是否相同 (`s[l] == s[r]`)。
   - 偶數長度擴張：把 `l` 設在 `i`，`r` 設在 `i+1`，一樣向兩旁查看字符是否相同。
4. 在擴張的每一次迴圈中，如果比對成功，我們就紀錄 (或挑戰更新) 歷史最長長度 `res_len`，並記下當時被認證為合法迴文的這段字串。隨後 `l -= 1`, `r += 1` 繼續挑戰極限。
5. 掃蕩完所有的可能中心點後，回傳紀錄下的那段子字串。這個解法的時間複雜度 O(N^2)，但因為是 In-Place 計算常數極小，空間複雜度是完美的 O(1)。
'''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ""
        res_len = 0
        
        for i in range(len(s)):
            # 奇數長度迴文的擴展
            l, r = i, i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > res_len:
                    res = s[l:r+1]
                    res_len = r - l + 1
                l -= 1
                r += 1
                
            # 偶數長度迴文的擴展
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > res_len:
                    res = s[l:r+1]
                    res_len = r - l + 1
                l -= 1
                r += 1
                
        return res
