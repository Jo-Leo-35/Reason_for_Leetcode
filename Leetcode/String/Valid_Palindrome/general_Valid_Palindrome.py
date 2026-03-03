'''
演算法步驟（雙指針法擴散）：
1. 字串是不是迴文？其實如果過濾掉所有奇怪的符號跟大小寫，它不就是「左邊跟右邊」對稱長得一樣嗎！
2. 我們用兩個指針 `left = 0` 和 `right = len(s) - 1`，從字串的頭跟尾開始往中間走。
3. 先排除白嫖：如果 `left` 對應的不是英文或數字，`left` 前進。如果 `right` 對應的不是英文或數字，`right` 後退。（這裡要注意條件邊界，不能讓 `left` 因為連續非字母而衝過 `right`）
4. 等到左邊跟右邊真的都是紮實的字母數字後，我們把它們小寫化 (`.lower()`) 然後比對。
5. 如果不一樣！這字串就沒救了，是個冒牌的迴文，回傳 `False`。
6. 如果一樣，雙手互相往中間逼近 (`left += 1`, `right -= 1`)。
7. 直到走破紅塵相遇的時候 (left >= right)，我們就證明了它是迴文，回傳 `True`。此解法只佔 O(1) 空間。
'''
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        
        while left < right:
            while left < right and not self.is_alnum(s[left]):
                left += 1
            while left < right and not self.is_alnum(s[right]):
                right -= 1
                
            if s[left].lower() != s[right].lower():
                return False
                
            left += 1
            right -= 1
            
        return True
        
    def is_alnum(self, c: str) -> bool:
        return (
            ord('A') <= ord(c) <= ord('Z') or 
            ord('a') <= ord(c) <= ord('z') or 
            ord('0') <= ord(c) <= ord('9')
        )
