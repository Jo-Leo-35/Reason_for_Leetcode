### 1. 核心題意與挑戰

給定一個字串 `s`，判斷它是否是**迴文 (Palindrome)**。
在判斷時，只考慮**英文字母和數字字元**（Alphanumeric），並且**忽略大小寫**。

* **隱藏挑戰**：
  * 字串裡面包含一堆空白、逗號、標點符號，需要乾淨地過濾。
  * 能不能不使用額外空間（例如不建立一個全新的乾淨字串）直接在原字串上判斷？

---

### 2. 解法對比與完整程式碼

#### A. 空間換時間：正規化再比較 (Normalize and Reverse)

**思路**：
先過濾掉所有非字母數字的字元，再把它們全部轉為小寫。
最後把這個乾淨的字串跟「它的反轉字串」比對，如果一樣就是迴文。

* **優點**：在 Python 中只要短短兩行就解決，非常 Pythonic。
* **缺點**：開創了新的字串陣列，空間複雜度是 $O(N)$。

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # 使用 list comprehension 過濾並轉小寫
        clean_s = [char.lower() for char in s if char.isalnum()]
        
        # 比較正向與反向是否相等
        return clean_s == clean_s[::-1]
```

#### B. 雙指針法 (Two Pointers) —— **最正統、無額外空間依賴**

**思路**：
使用兩個指針 `left` 和 `right`，分別從字串的最頭跟最尾巴開始往中間走。
如果遇到非字母數字的字元，就直接跳過 (指針前進/後退)。
如果兩個指針停下來的字元（轉成小寫後）不一樣，就回傳 `False`。
相撞則回傳 `True`。

* **優點**：空間複雜度完美的 $O(1)$，不需要對整個字串預處理，只要一發現不符就 Early Return，省時。

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        
        while left < right:
            # left 跳過非字母數字
            # 注意要加上 left < right 防越界
            while left < right and not s[left].isalnum():
                left += 1
                
            # right 跳過非字母數字
            while left < right and not s[right].isalnum():
                right -= 1
                
            # 比較大小寫轉換後是否相同
            if s[left].lower() != s[right].lower():
                return False
                
            left += 1
            right -= 1
            
        return True
```

---

### 3. 實務應用場景

#### 1. DNA 序列比對之回文結構 (Palindrome Sequence in Genomics)
* **應用**：在基因組研究中，回文序列常是限制酶切位點 (Restriction Enzyme Recognition Sites)，透過類似頭尾雙指針的演算法可以高速找出特定長度的回文段落。

#### 2. 資料清理自動化 (Data Cleansing Pipeline)
* **應用**：在處理 NLP 的斷詞前，常會寫類似 `not char.isalnum()` 的雙指針跳躍邏輯來把雜亂網頁爬下的髒資料去除符號。

---

### 4. 總結筆記

| 比較維度 | Pythonic API | 雙指針法 (Two Pointers) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ (走訪三趟：過濾、反轉、比較) | $O(N)$ (只走一趟，且可提早結束) |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **面試表現** | 解答太依賴語言特性 | **最正規解法，推薦** |
| **內建函數提示** | `char.isalnum()` 可以判定字母跟數字 | 記得 `left < right` 越界防護 |
