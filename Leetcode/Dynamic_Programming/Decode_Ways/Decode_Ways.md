### 1. 核心題意與挑戰

一條包含字母 `A-Z` 的訊息經由 `A -> 1`, `B -> 2`, ..., `Z -> 26` 的規則編碼成數字字串。
給定一個只包含數字的字串 `s`，計算能夠解碼的方法總數。

* **關鍵限制**：
  * `"0"` 沒有對應的字母，也不能組成 `"06"` 這種數字，前導零無效。
  * 只有 `10-26` 的組合是有效的兩位數解碼。
* **隱藏挑戰**：零 (`0`) 是本題最大的陷阱。若你遇到連續的 0 或是無法與前面配對的 0 (像是 `"30"`)，將導致整條字串解碼數為 0。

---

### 2. 解法對比與完整程式碼

#### A. 一維陣列動態規劃 (Array DP) —— **易懂的標準解法**

**思路**：
對於字串中的第 `i` 個字元，它的解碼方式數量 `dp[i]` 取決於：
1. **單一字元解碼**：只要 `s[i]` 不是 `"0"`，那麼可以繼承 `dp[i-1]` 的解碼數。
2. **雙字元解碼**：只要 `s[i-1]` 和 `s[i]` 組成的數字介於 `10` 到 `26` 之間，那麼可以繼承 `dp[i-2]` 的解碼數。

`dp[i] = (dp[i-1] 可以單讀) + (dp[i-2] 可以雙讀)`

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
            
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1 # basis
        dp[1] = 1 # 第一個字元若非0就是1種
        
        for i in range(2, n + 1):
            # i 是一個長度，轉回 index 需減 1
            # 1. 檢查單一字元
            if s[i-1] != '0':
                dp[i] += dp[i-1]
                
            # 2. 檢查雙字元
            two_digit = int(s[i-2:i])
            if 10 <= two_digit <= 26:
                dp[i] += dp[i-2]
                
        return dp[n]
```

#### B. 空間最佳化 DP (Space-Optimized DP) —— **推薦面試解法**

**思路**：
如同 Fibonacci 和 House Robber，本題狀態也只依賴前一步 `dp[i-1]` 與前兩步 `dp[i-2]`。
所以我們同樣可以使用兩個變數 `prev2`, `prev1` 來滾動狀態，把空間降為 $O(1)$。

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
            
        prev2 = 1 # 相當於 dp[i-2]
        prev1 = 1 # 相當於 dp[i-1]
        
        for i in range(1, len(s)):
            curr = 0
            # 單一字元
            if s[i] != '0':
                curr += prev1
                
            # 雙字元
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                curr += prev2
                
            prev2 = prev1
            prev1 = curr
            
        return prev1
```

---

### 3. 實務應用場景

#### 1. 壓縮與解壓縮協定 (Data Compression)
* **應用**：解碼二進制流或符號時的歧義解析 (Ambiguity Resolution)。像 Huffman Coding 就必須保證 Prefix-free 以確保唯一解碼，而本題故意留下類似歧義讓我們計算可能性。

#### 2. 自然語言處理 (NLP - Tokenizer)
* **應用**：分詞系統 (Word Segmentation)，尤其在沒有空白分隔符的語系（如中文日文），一個字串有多少種拆解出合法詞彙的方法，與 Decode Ways 的邏輯非常相似。

---

### 4. 總結筆記

| 比較維度 | Array DP | Space-Optimized DP |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **邊界條件 (Edge Case)** | 處理字首是 0 會直接回傳 0 | 必須把 `int(s)` 字串切割轉換寫穩 |
| **面試常犯錯誤** | 把 Invalid 的 `"0"` 也當成一種解碼步數加上去。 | |
