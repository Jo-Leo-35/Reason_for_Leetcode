### 1. 核心題意與挑戰

給定不同面額的硬幣陣列 `coins` 和一個總金額 `amount`。
計算可以湊成總金額所需的 **最少硬幣個數**。如果沒有任何硬幣組合能組成總金額，返回 `-1`。
你可以認為每種硬幣的數量是無限的。

* **隱藏挑戰**：貪婪演算法（Greedy）在這裡會失敗！如果硬幣面額是 `[1, 3, 4]`，目標是 `6`。貪婪會先拿 `4`，然後只能拿兩個 `1`，總共 3 枚。但最佳解是拿兩個 `3`，總共 2 枚。必須使用 DP 或 BFS。

---

### 2. 解法對比與完整程式碼

#### A. 一維動態規劃 (1D DP - Bottom Up) —— **本題首選，必備模板**

**思路**：
定義 `dp[i]` 為湊成金額 `i` 所需要的最少硬幣數量。
對於每一個金額 `i`，我們遍歷所有可能的硬幣面額 `c`。只要 `i >= c`，那麼 `dp[i]` 可以從 `dp[i - c] + 1` 轉移過來。
狀態轉移方程式：`dp[i] = min(dp[i], dp[i - c] + 1)`

* **優點**：架構十分穩定，完全避免了貪婪演算法的陷阱。
* **缺點**：時間複雜度為 $O(S \times n)$，其中 $S$ 是金額 $n$ 是硬幣總數。

```python
from typing import List

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # 初始化 DP 陣列為一個不可能達成的大數字 (amount + 1)
        # 不要用 float('inf')，在加 1 時可能會有效能折損或型別問題
        dp = [amount + 1] * (amount + 1)
        
        # 湊成金額 0 需要的硬幣數是 0
        dp[0] = 0
        
        # 從 1 塊錢開始算到 amount 塊錢
        for i in range(1, amount + 1):
            for c in coins:
                # 當前金額比硬幣面額大或相等，才能使用該硬幣
                if i - c >= 0:
                    dp[i] = min(dp[i], dp[i - c] + 1)
                    
        # 如果 dp[amount] 沒被更新過，代表湊不出來
        return dp[amount] if dp[amount] != amount + 1 else -1
```

#### B. 廣度優先搜尋 (BFS) —— **最短路徑思維**

**思路**：
把 `amount` 想成起點，把 `0` 想成終點。每次減去一個 `coin` 的面額相當於走一步。
尋找「最少硬幣數」其實就是在尋找圖論中無權重圖的「最短路徑」。可以使用 Queue 來實作 BFS。

* **優點**：在面試中能展現不同於 DP 的圖論思維。如果是問「能否湊出」，此解法通常能更快遇到解而提早結束 (Early Return)。

```python
from typing import List
from collections import deque

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0
            
        queue = deque([(0, 0)]) # (當下累積金額, 使用硬幣數)
        visited = set([0])
        
        while queue:
            curr_sum, steps = queue.popleft()
            
            for coin in coins:
                next_sum = curr_sum + coin
                
                if next_sum == amount:
                    return steps + 1
                    
                if next_sum < amount and next_sum not in visited:
                    visited.add(next_sum)
                    queue.append((next_sum, steps + 1))
                    
        return -1
```

---

### 3. 實務應用場景

#### 1. 虛擬貨幣或遊戲幣兌換系統
* **應用**：玩家用現金儲值遊戲幣，系統需要計算出給予玩家各種面額代幣組合的最少 Token 發放數量。

#### 2. 包裝與裝箱最佳化 (Bin Packing Problem)
* **應用**：在物流系統中，若有各種固定容積的標準箱，給定商品的總容積，如何使用最少數量的標準箱裝載完畢，即為完全背包問題的延伸。

---

### 4. 總結筆記

| 比較維度 | DP (Bottom-Up) | BFS |
| --- | --- | --- |
| **時間複雜度** | $O(S \times N)$ | $O(S \times N)$ 但因剪枝可能提早結束 |
| **空間複雜度** | $O(S)$ | 最差 $O(S)$ (Queue 佔用) |
| **實戰選擇** | 程式碼極短，必定優先寫 | 遇到變形題 (如硬幣數量有限) 時可切換 |
| **經典題型歸類** | 無界背包問題 (Unbounded Knapsack) | 無權重最短路徑 |
