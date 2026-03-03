'''
演算法步驟（Type-Length-Value 編碼法）：
1. 這一題在真實系統設計中對應的是網路協議層的「資料序列化 (Serialization)」。
2. 【編碼 Encode】：
   - 由於陣列裡的字串可能包含任何阿貓阿狗的符號（甚至是我們想當作分隔符的符號），所以單純用 `,` 或 `|` 來 join 絕對會死得很慘。
   - 我們採用工業界通用的 TLV (Type-Length-Value) 精神。
   - 走訪每一個字串：在每個字串前面，黏上它的「長度」，再加上一個特殊的「分隔符」（例如 `#`）。
   - 這樣編碼出來會變成 `長度#字串長度#字串...`。例如 `["hello", "world"]` 變成 `5#hello5#world`。
3. 【解碼 Decode】：
   - 我們用一個指標 `i = 0` 從頭開始讀取字串。
   - 先找到第一個遇到的 `#`，那麼從 `i` 到 `#` 之間的字串，就是下一個單字的「長度」。
   - 用 `int()` 把它轉成數字 `length`。
   - 接著我們就可以大膽地從 `#` 的下一格開始，精準地往後切出長度為 `length` 的子字串！這時候就算這段裡面有一大堆 `#` 也完全不會混淆。
   - 讀完了之後，把指標 `i` 瞬間移動到這個單字的尾巴，繼續從下一單字的長度區塊開始讀取。
'''
class Codec:
    def encode(self, strs: [str]) -> str:
        """Encodes a list of strings to a single string."""
        res = ""
        for s in strs:
            res += str(len(s)) + "#" + s
        return res

    def decode(self, s: str) -> [str]:
        """Decodes a single string to a list of strings."""
        res, i = [], 0
        
        while i < len(s):
            j = i
            while s[j] != "#":
                j += 1
                
            length = int(s[i:j])
            
            # 從分隔符後面開始切出準確長度的字串
            res.append(s[j + 1 : j + 1 + length])
            
            # 將指針移動到下一個資料塊的開頭
            i = j + 1 + length
            
        return res
