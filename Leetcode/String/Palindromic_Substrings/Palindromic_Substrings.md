### 1. 核心題意與挑戰

給定一個字串 `s`，計算這個字串中有**多少個迴文子字串** (Palindromic Substrings)。
即使兩個子字串具有完全相同的字元，只要它們在原字串中開始或結束的位置不同，就被視為不同的子字串。

* **隱藏挑戰**：這題跟上一題 **Longest Palindromic Substring** 的解法有 87% 像！不求「最長」，而求「總數」。

---

### 2. 解法對比與完整程式碼

#### A. 中心擴展法 (Expand Around Center) —— **最佳標準解**

**思路**：
承襲上一題的概念，字串中有 `2N - 1` 個可能的迴文中心。
我們從這 `2N - 1` 個中心向左右擴展，只要擴展出來的字串是迴文，我們就把計數器 `count += 1`。

* **優點**：空間複雜度 $O(1)$，完美解決。

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        if not s:
            return 0
            
        def count_palindromes_around_center(left: int, right: int) -> int:
            count = 0
            # 向外擴展，只要相等就代表找到一個新的迴文
            while left >= 0 and right < len(s) and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count
            
        total_palindromes = 0
        for i in range(len(s)):
            # 計算以 i 為中心的奇數長度迴文數量
            total_palindromes += count_palindromes_around_center(i, i)
            # 計算以 i, i+1 為間隙的偶數長度迴文數量
            total_palindromes += count_palindromes_around_center(i, i + 1)
            
        return total_palindromes
```

#### B. 針對二維 DP 的降維打擊

**思路**：
如果上一題採用 2D DP `dp[i][j]`，那這題就只是在填寫 DP 表格的時候，順便計算有幾個 `True` 而已。
由於中心擴展法實在太優秀，DP 的 $O(N^2)$ 空間反而顯得笨重，故在此略過 DP 的程式碼，面試中強烈建議使用中心擴展即可。

---

### 3. 實務應用場景

本題屬於算法思維的鍛鍊，其「計算所有可能組合體」的模式可見於：
#### 1. 金融反詐欺系統的特徵向量抽取
* **應用**：若將用戶交易路徑轉為序列，迴型結構 (資金 A->B->A 或 A->B->C->B->A) 往往是洗錢的信號。計算有多少次此類對稱折返可以作為機器學習模型的風險特徵。

---

### 4. 總結筆記

| 解題關鍵詞 | 對應思路 |
| --- | --- |
| **2N - 1 個中心點** | 考慮了奇數和偶數長度的對稱中心 |
| **`s[left] == s[right]`** | 迴文的核心定義 |
| **`left -= 1, right += 1`** | 不斷向外擴張的雙指針 |
