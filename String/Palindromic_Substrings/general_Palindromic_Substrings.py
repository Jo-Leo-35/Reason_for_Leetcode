'''
演算法步驟：
1. 這一題其實是 Longest Palindromic Substring 的計數版。
2. 同樣採用 O(N^2) 運行的 Expand Around Center 中心擴展法。這種演算法的好處是幾乎等同空間複雜度 O(1)，而且可以避免極致刁鑽的 Manacher’s Algorithm。
3. 設立一個計數器 `count` = 0。
4. 以每個字串索引 `i` 作為核心：
   - 先挑戰「奇數」迴文：`l = i`, `r = i`。只要 `s[l] == s[r]`，這就是一組迴文！`count += 1`，然後我們讓手冊往兩側再多探一點路 `l -= 1`, `r += 1`。
   - 再挑戰「偶數」迴文：`l = i`, `r = i+1`。一樣的規矩，如果他們長得一樣，就算找到另一種長度的迴文！`count += 1`，然後一樣兩端拉開試探。
5. 等我們把字串徹底每個坑都鑽過一遍，`count` 就是最終答案了。
'''
class Solution:
    def countSubstrings(self, s: str) -> int:
        count = 0
        
        for i in range(len(s)):
            # 奇數長度探測
            l, r = i, i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                count += 1
                l -= 1
                r += 1
                
            # 偶數長度探測
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                count += 1
                l -= 1
                r += 1
                
        return count
