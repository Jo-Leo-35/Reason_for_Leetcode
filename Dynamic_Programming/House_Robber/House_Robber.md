### 1. 核心題意與挑戰

你是一個專業的小偷，計畫偷竊沿街的房屋。每間房內都藏有一定的現金。
影響你偷竊的唯一制約因素就是相鄰的房屋裝有相互連通的防盜系統，**如果兩間相鄰的房屋在同一晚上被小偷闖入，系統會自動報警**。
給定一個代表每個房屋存放金額的非負整數陣列，請計算你在**不觸動警報裝置的情況下**，今晚能夠偷竊到的最高金額。

* **關鍵限制**：不能偷相鄰的房屋。
* **隱藏挑戰**：每一間房屋只能選擇「偷」或「不偷」，而這個決定會影響到相鄰房屋的決策。如何尋找最大化利益的子結構？

---

### 2. 解法對比與完整程式碼

#### A. 動態規劃 (Dynamic Programming - Array) 

**思路**：
走到第 `i` 間房屋時，小偷有兩個選擇：
1. **偷這家**：那就不能偷第 `i-1` 家，獲得的金額是 `nums[i] + dp[i-2]`。
2. **不偷這家**：獲得的金額等同於在前 `i-1` 家偷到的最高金額 `dp[i-1]`。
因此狀態轉移方程式為：`dp[i] = max(dp[i-1], nums[i] + dp[i-2])`。

* **優點**：簡單直觀，完整記錄了到每一棟房子為止的最高獲利。
* **缺點**：空間複雜度 $O(N)$。

```python
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
            
        dp = [0] * len(nums)
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        
        for i in range(2, len(nums)):
            dp[i] = max(dp[i-1], nums[i] + dp[i-2])
            
        return dp[-1]
```

#### B. 空間最佳化 DP (Space-Optimized DP) —— **推薦面試解法**

**思路**：
同 Climbing Stairs，狀態轉移只依賴於 `dp[i-1]` 和 `dp[i-2]` 兩個歷史狀態。
我們只用兩個指針 `rob1`（代表 `dp[i-2]`）和 `rob2`（代表 `dp[i-1]`）來滾動儲存。

* **優點**：時間複雜度 $O(N)$，空間被壓縮至 $O(1)$。
* **缺點**：無。

```python
from typing import List

class Solution:
    def rob(self, nums: List[int]) -> int:
        rob1, rob2 = 0, 0
        
        for money in nums:
            # [rob1, rob2, money, ...]
            # 計算如果偷當前這家的最大獲益
            temp = max(money + rob1, rob2)
            # 狀態滾動前進
            rob1 = rob2
            rob2 = temp
            
        return rob2
```

---

### 3. 實務應用場景

本題核心思想是「相鄰互斥的最大化收益規劃」，概念可延伸至：

#### 1. 排程與資源分配 (Scheduling & Resource Allocation)
* **應用**：在伺服器叢集中部署任務。為避免特定衝突（如相鄰機架散熱不足），不能將高功耗任務排在相鄰機器上，求最大整體效能。

#### 2. 活動規劃 (Event Management)
* **應用**：你有多場可舉辦的演講活動（有各自預期收益），但為確保演講品質，不允許連著兩天辦活動，如何安排最高總收益？

---

### 4. 總結筆記

| 比較維度 | Array DP | Space-Optimized DP |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **面試題眼** | 找出 `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` | 狀態壓縮的 `rob1`, `rob2` 推進法 |
