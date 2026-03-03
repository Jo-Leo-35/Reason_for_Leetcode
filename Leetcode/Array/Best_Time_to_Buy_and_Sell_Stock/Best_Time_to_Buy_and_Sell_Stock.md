### 1. 核心題意與挑戰

給定一個陣列 `prices`，它的第 `i` 個元素 `prices[i]` 表示一支給定股票第 `i` 天的價格。
你只能選擇**某一天**買入這隻股票，並選擇在**未來的某一個不同的日子**賣出該股票。設計一個演算法來計算你所能獲取的最大利潤。
如果你不能獲取任何利潤，返回 `0`。

* **關鍵限制**：
  * 不能時光倒流（買入一定要在賣出之前）。
  * 只能交易「一次」！
* **隱藏挑戰**：
  * 這是所有股票買賣系列題型 (Best Time to Buy and Sell Stock I ~ IV, Cooldown, Fee) 的最基礎班。不可用 $O(N^2)$ 的找最大差值法。

---

### 2. 解法對比與完整程式碼

#### 貪婪法維護極值 (Greedy Min-Tracking) —— **最漂亮的一維狀態機**

**思路**：
我們不需要去比較每一天的差值組合。
我們只要維護一個歷史指標：`min_price` (到目前為止的最低買價)。
對於每一天 `prices[i]`，我們只會做一件事：
* 如果今天的價格比 `min_price` 還低，我們當然不會賣出，我們會把今天當作新的 `min_price` 買點！
* 如果今天的價格比較高，我們就試算：**「如果我用歷史最低買價 `min_price` 買，然後在今天賣出，利潤會不會破紀錄？」**

* **時間複雜度**：$O(N)$
* **空間複雜度**：$O(1)$

```python
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
            
        # 初始最低價定為無限大
        min_price = float('inf')
        max_profit = 0
        
        for p in prices:
            if p < min_price:
                # 發現更便宜的進場點
                min_price = p
            elif p - min_price > max_profit:
                # 若今天賣出的獲利超越歷史紀錄，則更新獲利
                max_profit = p - min_price
                
        return max_profit
```

---

### 3. 實務應用場景

#### 1. 數據流的最大下降/上升偏差度 (Max Drawdown / Max Run-up)
* **應用**：在計量金融與回測系統 (Backtesting) 中，要評估一個策略的穩定性，最重要的指標叫 Max Drawdown（最大交易回檔），它的底層數學邏輯與這道題求「給定最低點後的最大飆升值」是完全對稱的演算法模型。

#### 2. 日誌分析中的尖刺異常偵測 (Spike Detection)
* **應用**：尋找在伺服器用量日誌中，由最低負載急遽攀升到最高點的瞬間。

---

### 4. 總結筆記

| 解法精神 | `min_price` 維護法 |
| --- | --- |
| **直覺比喻** | 若你想在最高點賣掉，你一定希望自己曾經買在最低點。所以你只要一直記住生命中遇過最低的點就好啦！ |
| **與 DP 題的關聯** | 此題其實等於連續找尋差值陣列 `差值 = prices[i] - prices[i-1]` 的 **Maximum Subarray (最大子陣列和)**。 |
| **時間與空間** | 時間 $O(N)$，空間 $O(1)$ |
