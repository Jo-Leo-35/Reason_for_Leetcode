### 1. 核心題意與挑戰

給定一個字串 `s` 和一個字串字典 `wordDict`，請判斷 `s` 是否可以被空格拆分為一個或多個在字典中出現的單字。
注意：字典中的單字可以重複使用。

* **關鍵限制**：
  * $1 \le s.length \le 300$
  * $1 \le wordDict.length \le 1000$
* **隱藏挑戰**：如何避免重複比對相同的子字串？純粹的 DFS/Backtracking 如果沒有加上 Memoization 肯定會遇到 TLE (Time Limit Exceeded)。這是一道經典的「背包問題」變體（字串被單字填滿）。

---

### 2. 解法對比與完整程式碼

#### A. 一維動態規劃 (1D DP) —— **推薦面試解法**

**思路**：
定義 `dp[i]` 為：字串 `s` 的前 `i` 個字元（即 `s[0:i]`）是否能被成功拆分。
對於每個位置 `i`，我們去尋找一個分割點 `j`（$0 \le j < i$），如果 `dp[j]` 是 `True` 且 `s[j:i]` 在字典裡面，那麼 `dp[i]` 也會是 `True`。

為了加速在字典中的查找，我們會將 `wordDict` 轉換成 `Set`。

* **優點**：思路直覺，時間複雜度穩定。
* **缺點**：如果字典裡的單字長度大多很短，但我們一直嘗試到 `j=0` 可能會做白工。

```python
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        n = len(s)
        
        # dp[i] 代表 s[0:i] 是否能被字典拆分
        dp = [False] * (n + 1)
        dp[0] = True # 空字串可以被合法拆分
        
        for i in range(1, n + 1):
            for j in range(i):
                # 如果前半段合法，且後半段在字典裡
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break # 找到一種合法拆分方式即可，跳出內層迴圈
                    
        return dp[n]
```

#### B. 針對單字長度最佳化的 DP (Optimized DP)

**思路**：
在前述的 DP 中，內層迴圈 `j` 會從 `0` 遍歷到 `i-1`，即使 `s[j:i]` 的長度遠超過字典中最長的單字。
我們可以只拿字典中的單字長度去回推前面的 `dp` 狀態，這樣時間複雜度更能貼近 $O(N \times L)$，其中 $N$ 是字串長度、$L$ 是字典數目。

```python
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            for word in wordDict:
                word_len = len(word)
                # 從當前位置 i 往前推一個單字的長度
                # 確保不越界 且 該前置狀態合法 且 字串相符
                if i >= word_len and dp[i - word_len] and s[i - word_len:i] == word:
                    dp[i] = True
                    break # 只要有一個單字能成功接上即可
                    
        return dp[n]
```

---

### 3. 實務應用場景

#### 1. 搜尋引擎的分詞技術 (Query Segmentation)
* **應用**：使用者在搜尋引擎輸入了沒有空格的關鍵字組合（例如 "applewatchband"），系統必須將其斷詞成 ["apple", "watch", "band"] 才能夠精準匹配商品或文章。

#### 2. 密碼暴力破解與字典攻擊 (Password Cracking Analysis)
* **應用**：分析使用者的密碼是否是由常見字典單字拼接而成（例如 "admin123password"）。透過 Word Break 可以快速找出這類防護薄弱的密碼。

---

### 4. 總結筆記

| 比較維度 | 基礎 DP | 單字長度最佳化 DP |
| --- | --- | --- |
| **時間複雜度** | $O(N^3)$ (迴圈 $O(N^2) \times$ 字串切片 $O(N)$) | $O(N \times M \times L)$ ($M$ 是字典大小、$L$ 是單字平均長度) |
| **空間複雜度** | $O(N)$ (給 dp 陣列) | $O(N)$ |
| **面試表現** | 解出來即及格 | **能主動提出根據單字長度縮減搜尋範圍，令人驚豔** |
