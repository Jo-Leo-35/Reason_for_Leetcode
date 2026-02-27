### 1. 核心題意與挑戰

你正在爬樓梯。需要 `n` 階才能到達樓頂。
每次你可以爬 `1` 或 `2` 個台階。請問你有多少種不同的方法可以爬到樓頂？

* **關鍵限制**：`n` 為正整數（$1 \le n \le 45$）。
* **隱藏挑戰**：若使用純遞迴，會探尋出指數級別的節點，導致 `Time Limit Exceeded (TLE)`。如何將問題抽象為尋找重疊的子問題？

---

### 2. 解法對比與完整程式碼

#### A. 動態規劃 (Dynamic Programming - Array) —— **基礎思維解法**

**思路**：
到達第 `i` 階的方法，必然是從第 `i-1` 階跨一步，或是從第 `i-2` 階跨兩步而來。
因此狀態轉移方程式為：`dp[i] = dp[i-1] + dp[i-2]`。
這本質上就是費氏數列 (Fibonacci Sequence)。

* **優點**：容易理解，狀態保存完整。
* **缺點**：需要 $O(N)$ 的額外空間。

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
            
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        
        for i in range(3, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
            
        return dp[n]
```

#### B. 空間最佳化 DP (Space-Optimized DP) —— **推薦面試解法**

**思路**：
觀察狀態轉移方程式 `dp[i] = dp[i-1] + dp[i-2]`，我們可以發現，計算當前狀態只需依賴**前兩個**狀態，更早之前的狀態用不到。
因此我們只需要兩個變數來記錄前兩個階梯的方法數即可，這樣能把空間降至 $O(1)$。

* **優點**：時間 $O(N)$、空間 $O(1)$，效率極佳。
* **缺點**：這已是最優解，無明顯缺點。

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
            
        prev1 = 2 # dp[i-1]
        prev2 = 1 # dp[i-2]
        
        for _ in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1
            prev1 = curr
            
        return prev1
```

---

### 3. 實務應用場景

這類「每次可選擇多種步伐，求總共多少種方案」的問題是組合數學的經典模型，對應現實中的：

#### 1. 路徑規劃與決策樹 (Path Planning & Decision Tree)
* **應用**：用於計算導航系統中到達特定節點可能的總決策路徑數。

#### 2. 定寬度排列問題 (Combinatorics)
* **應用**：分析如果商品貨架上可以放置寬度為 1 或為 2 的商品，如何排滿長度為 `n` 的貨架有幾種排法。

---

### 4. 總結筆記

| 比較維度 | Array DP | Space-Optimized DP |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **面試表現** | 合格 | **極佳 (Follow-up 必考)** |
| **核心考點** | 重疊子問題、費氏數列轉換 | 狀態壓縮 (State Compression) |
