### 1. 核心題意與挑戰

給定一個字串 `s`，找到 `s` 中最長的**迴文子字串**。

* **隱藏挑戰**：
  * 「子字串」必須是連續的。
  * 迴文可能長度為奇數（以一個字元為中心，如 "aba"）或偶數（以兩個字元間隙為中心，如 "abba"）。如何優雅地同時處理這兩種情況？

---

### 2. 解法對比與完整程式碼

#### A. 中心擴展法 (Expand Around Center) —— **時間O(N^2)、空間O(1)的絕佳解**

**思路**：
迴文是左右對稱的，與其「從頭尾往中間檢查」，不如「**從中間往頭尾擴展**」。
迴文的中心總共有 `2N - 1` 個。因為除了以每個字元為中心（共 $N$ 個），還有以兩個相鄰字元為中心（共 $N-1$ 個）。
我們只要以每一個中心點出發，向左右擴展，直到不再對稱為止，並且紀錄最長的那次擴展。

* **優點**：比起動態規劃省去了 $O(N^2)$ 的空間限制，極度純粹。

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or len(s) < 2:
            return s
            
        def expand_around_center(left: int, right: int) -> str:
            # 當左右未越界，且字元相同時，持續向外擴張
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # 迴圈打破時，left 與 right 都已經多走了一步，所以退回擷取
            return s[left + 1:right]

        longest = ""
        for i in range(len(s)):
            # 奇數長度的迴文（以 i 為中心）
            odd_pal = expand_around_center(i, i)
            # 偶數長度的迴文（以 i, i+1 的間隙為中心）
            even_pal = expand_around_center(i, i + 1)
            
            if len(odd_pal) > len(longest):
                longest = odd_pal
            if len(even_pal) > len(longest):
                longest = even_pal
                
        return longest
```

#### B. 二維動態規劃 (2D DP) —— **觀念紮實的題型**

**思路**：
定義 `dp[i][j]` 表示：字串從索引 `i` 到 `j` 的子字串是否為迴文 (`True`/`False`)。
狀態轉移：
1. 如果長度為 1 (`i == j`)，一定是迴文。
2. 如果長度為 2 (`j - i == 1`)，且 `s[i] == s[j]`，則是迴文。
3. 如果長度大於 2，只要頭尾字元相同 `s[i] == s[j]`，而且「去掉頭尾的內部子字串」也是迴文 (`dp[i+1][j-1]` == True)，這串就是迴文！

* **缺點**：消耗了 $O(N^2)$ 的陣列空間，效率反而沒有中心擴展法高。

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s
            
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1
        
        # 對角線都是長度 1 的迴文
        for i in range(n):
            dp[i][i] = True
            
        # 遍歷右邊界 j，填寫右上半部矩陣
        for j in range(1, n):
            # 填寫左邊界 i
            for i in range(j):
                if s[i] == s[j]:
                    # 只有兩個字元 (j-i == 1) 或三個字元 (j-i == 2) 直接 True
                    # 或者從左下角的狀態轉移上來
                    if j - i <= 2 or dp[i+1][j-1]:
                        dp[i][j] = True
                        if j - i + 1 > max_len:
                            max_len = j - i + 1
                            start = i
                            
        return s[start:start + max_len]
```

*(註：還有一種 Manacher's Algorithm 可以做到 $O(N)$，但在面試中被認為太過刁鑽，不強求)*

---

### 3. 實務應用場景

#### 1. 自然語言的詞根解析器 (Morphological Parsing)
* **應用**：中心擴展法的思想常用於字串處理引擎中。在進行多語系構詞學分析時，針對綴詞 (Affixes) 的擴展與對比，也是由中心詞幹開始向外對應規則。

#### 2. 音訊波形的對稱特徵辨識
* **應用**：找尋聲音檔案陣列中符合完美迴音反射 (Symmetrical Echo) 的區段，用於聲學空間的濾波器建模。

---

### 4. 總結筆記

| 比較維度 | 中心擴展法 | 2D 動態規劃 |
| --- | --- | --- |
| **時間複雜度** | $O(N^2)$ | $O(N^2)$ |
| **空間複雜度** | $O(1)$ | $O(N^2)$ |
| **邏輯起點** | **從中心出發** | 從長度短的子字串出發 |
| **面試實戰** | **程式碼乾淨、無額外空間，強烈推薦** | 架構嚴謹，可展現對 State Transition 的掌控 |
