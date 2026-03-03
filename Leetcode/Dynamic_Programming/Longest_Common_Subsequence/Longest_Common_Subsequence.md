### 1. 核心題意與挑戰

給定兩個字串 `text1` 和 `text2`，返回這兩個字串的**最長共同子序列 (Longest Common Subsequence, LCS)** 的長度。
若沒有共同子序列，則返回 0。

* **子序列**：在不改變字元相對順序的情況下，刪除部分或不刪除字元後形成的字串。
* **隱藏挑戰**：字串長度可能高達 1000。如果枚舉所有子序列，時間複雜度高達 $O(2^N)$。如何運用二維 DP 來捕捉這兩個字串配對的最佳解？

---

### 2. 解法對比與完整程式碼

#### A. 經典二維動態規劃 (2D DP) —— **必考標準矩陣解**

**思路**：
建立一個二維陣列 `dp[i][j]`，代表 `text1` 的前 `i` 個字元與 `text2` 的前 `j` 個字元的最長共同子序列長度。
狀態轉移：
1. **若字元相同** (`text1[i-1] == text2[j-1]`)：雙方都貢獻了1個長度，所以 `dp[i][j] = 1 + dp[i-1][j-1]`。
2. **若字元不同** (`text1[i-1] != text2[j-1]`)：當前字元無法配對，必須有一方退一步做妥協，取較大者：`dp[i][j] = max(dp[i-1][j], dp[i][j-1])`。

* **優點**：架構十分規整，非常清晰的網格 (Grid) 探索思路。
* **缺點**：空間複雜度 $O(M \times N)$。

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        
        # 建立 (m+1) x (n+1) 的 DP 表格，多出 1 為了處理空字串的邊界條件
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    # 相等，往斜上方拿值 + 1
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    # 不等，取其左邊或上面的最大值
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                    
        return dp[m][n]
```

#### B. 壓縮空間動態規劃 (Space-Optimized 1D DP)

**思路**：
觀察轉移方程式可以發現，計算第 `i` 列的 `dp` 值時，只會用到第 `i-1` 列（上一列）的狀態。
因此我們不需要保存整個矩陣，只需要保存「現在這列」跟「上一列」的狀態即可，將空間複雜度從 $O(M \times N)$ 降至 $O(\min(M, N))$。

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # 確保 text2 一直是較短的，省下更多空間
        if len(text1) < len(text2):
            text1, text2 = text2, text1
            
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                if text1[i-1] == text2[j-1]:
                    curr[j] = prev[j-1] + 1
                else:
                    curr[j] = max(prev[j], curr[j-1])
            prev = curr
            
        return prev[n]
```

---

### 3. 實務應用場景

本題是計算機科學領域中極為基礎且偉大的演算法之一。

#### 1. 版本控制系統 (Git Merge & Diff)
* **應用**：`git diff` 指令要在兩個檔案之間比對出新增及刪除的行數，底層就是使用 LCS 演算法或者是 Myers Diff Algorithm（LCS 的變體）。共同子序列代表「沒有改變的程式碼」。

#### 2. 生物資訊學 (Bioinformatics)
* **應用**：DNA 序列比對。比對兩條 DNA 鏈（字串僅含 A/C/G/T）的相似度，從而判斷親緣關係或是尋找基因變異（突變、缺失或插入）。LCS 是基礎，後續延伸為 Needleman-Wunsch 演算法。

---

### 4. 總結筆記

| 比較維度 | 2D DP | 1D DP (空間最佳化) |
| --- | --- | --- |
| **時間複雜度** | $O(M \times N)$ | $O(M \times N)$ |
| **空間複雜度** | $O(M \times N)$ | $O(\min(M, N))$ |
| **打底觀念** | `dp[i][j] = 1 + dp[i-1][j-1]` or `max(dp[i-1][j], dp[i][j-1])` | 只保留兩列滾動 |
| **面試表現** | 必須要秒殺 | 若面試官提出 O(N) 空間要求，即切換此解法 |
