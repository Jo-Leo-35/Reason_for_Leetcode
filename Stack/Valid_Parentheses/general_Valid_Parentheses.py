'''
演算法步驟：
1. 這是經典的堆疊 (Stack) 應用。利用 LIFO (後進先出) 的特性來匹配括號。
2. 建立一個 Hash Map (字典) `bracket_map`，把「右括號」當成 Key，「左括號」當成 Value 記錄起來。例如：`{')': '('}`。
3. 建立一個空的 `stack` 陣列。
4. 開始歷遍字串中的每一個字元 `char`：
   - 如果這個字元是「左括號」（也就是說，它不在字典的 Key 裡），那我們就無腦把它投進 `stack` 裡面。
   - 如果這個字元是「右括號」（它在字典的 Key 裡）：
     - 這時候就像是討債的來了，我們必須從 `stack` 頂端拉出一個過去存進去的括號來還債。
     - 從 `stack` `pop()` 出最頂端的元素。如果 `stack` 已經空了，代表還不出債（右括號太多），給他一個假的字元 `#`。
     - 核對債主：字典裡規定這個右括號對應的左括號，是不是剛剛 `pop()` 出來的那個傢伙？如果不是，或根本拿到假字元，直接回傳 `False`。
5. 成功跑完迴圈後，檢查 `stack` 裡面是不是空空如也？如果還有剩（左括號太多），回傳 `False`。若空了代表完美結帳，回傳 `True`。O(N) 時間與空間。
'''
class Solution:
    def isValid(self, s: str) -> bool:
        bracket_map = {
            ')': '(',
            '}': '{',
            ']': '['
        }
        stack = []
        
        for char in s:
            if char in bracket_map:
                top_element = stack.pop() if stack else '#'
                if bracket_map[char] != top_element:
                    return False
            else:
                stack.append(char)
                
        return len(stack) == 0
