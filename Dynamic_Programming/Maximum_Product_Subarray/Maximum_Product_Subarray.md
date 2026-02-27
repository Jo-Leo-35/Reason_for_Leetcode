### 1. 核心題意與挑戰

給定一個整數陣列 `nums`，找到一個具有**最高乘積**的連續子陣列（該子陣列最少包含一個數字），返回其最高乘積。

* **隱藏挑戰**：本題是 Maximum Subarray (最大子陣列和) 的變種。與加法不同的是：
  * **負負得正**：一個極小的負數（如 -50），如果再乘上一個負數，反而會變成極大的正數。
  * **零的破壞力**：任何數字補上 0 就會歸零，相當於必須將計算這件事「重置」。

---

### 2. 解法對比與完整程式碼

#### A. 維護極值 DP (Max / Min Tracking) —— **利用狀態機思維的 O(N) 解**

**思路**：
因為「負負得正」，我們不能只像 Maximum Subarray 那樣只維護「最大值」，我們還必須同時維護「**最小值**」（通常是負數，潛在的巨大炸彈）。
當遇到一個負數時，原本的「最大值」乘上它會變「最小值」，而原本的「最小值」乘上它會翻身成為「最大值」。
狀態定義：
* `curr_max`：包含當前數字 `nums[i]` 的最大連續乘積。
* `curr_min`：包含當前數字 `nums[i]` 的最小連續乘積。

當遇到新的數字 `num` 時：
更新選擇有三：自己獨立成軍 `num`、最大值乘自己 `curr_max * num`、最小值乘自己 `curr_min * num`。

```python
from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        # 全局最大值
        res = nums[0]
        # 到目前為止的最大與最小乘積
        curr_max = nums[0]
        curr_min = nums[0]
        
        for num in nums[1:]:
            # 因為 curr_max 會在下一行被修改，先用暫存變數存起來給 curr_min 用
            temp_max = curr_max
            
            # 從「自己」、「最大*自己」、「最小*自己(負負得正)」中挑最大/小值
            curr_max = max(num, temp_max * num, curr_min * num)
            curr_min = min(num, temp_max * num, curr_min * num)
            
            res = max(res, curr_max)
            
        return res
```

#### B. 雙向掃描法 (Forward and Backward Pass) —— **極度直覺且不易寫錯**

**思路**：
如果陣列中沒有 0，只會有兩種情況：
1. 有偶數個負數：全部乘起來就是正的，也是最大值。
2. 有奇數個負數：必須捨棄其中一個負數（以及其左邊或右邊的附屬品）。所以最大乘積一定出現在「從左乘到右」或是「從右乘到左」的過程中。

只要遇到 0 積就會斷掉，此時將乘積重置為 1 重新開始即可。

* **優點**：邏輯無敵簡單，不需要腦筋急轉彎去維護最小值。
* **缺點**：需要掃描兩次，但在時間複雜度上依然是 $O(N)$ 量級，常數稍微大一點。

```python
from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        res = float('-inf')
        
        # 1. 從左掃到右
        prefix = 1
        for i in range(n):
            prefix *= nums[i]
            res = max(res, prefix)
            if prefix == 0:
                prefix = 1 # 遇到 0 就重置
                
        # 2. 從右掃到左
        suffix = 1
        for i in range(n - 1, -1, -1):
            suffix *= nums[i]
            res = max(res, suffix)
            if suffix == 0:
                suffix = 1 # 遇到 0 就重置
                
        return res
```

---

### 3. 實務應用場景

#### 1. 訊號處理中的突發極值濾波 (Signal Amplifier Limit)
* **應用**：當處理經過多次反向放大器 (Inverting Amplifier) 的雜訊訊號時，計算連續段落可能產生的最大輸出電壓，以防系統燒毀。這類模型就像連續乘上負數。

#### 2. 風險利潤的複利波動模型 (Volatility Modelling)
* **應用**：計算投資組合在連續幾週內的波動槓桿，偶爾槓桿會出現反向做空（負數），這類演算法可以用來評估特定周期的極端獲利可能。

---

### 4. 總結筆記

| 比較維度 | 極值並行 DP | 雙向掃描法 |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ (僅走訪一次) | $O(N)$ (走訪兩次) |
| **空間複雜度** | $O(1)$ | $O(1)$ |
| **核心難點** | `temp` 變數的交換，以及乘積的 `max / min` 三者比大小 | 證明為何這題只有遇到零才會中斷，以及為何首尾負數是關鍵 |
| **面試推薦度** | **最佳解**，展現完備的嚴謹邏輯 | 遇到 Bug 寫不出 DP 時的絕佳解套方案 |
