### 1. 核心題意與挑戰

給定一個整數陣列 `nums`，找到其中**最長嚴格遞增子序列**的長度。
**子序列 (Subsequence)** 是由陣列派生而來的序列，刪除（或不刪除）陣列中的元素而不改變其餘元素的順序。

* **關鍵限制**：
  * $1 \le nums.length \le 2500$
* **隱藏挑戰**：常規的 DP 解法時間複雜度為 $O(N^2)$。這也是許多面試官的底線，但更厲害的面試官會要求挑戰 $O(N \log N)$ 的做法。

---

### 2. 解法對比與完整程式碼

#### A. 一維動態規劃 (1D DP) —— **核心觀念建立**

**思路**：
定義 `dp[i]` 代表「以 `nums[i]` 為結尾的最長嚴格遞增子序列的長度」。
我們對於每一個 `nums[i]`，去檢查它前面的所有數字 `nums[j]` ($0 \le j < i$)。
只要 `nums[i] > nums[j]`，代表 `nums[i]` 可以接在 `nums[j]` 後面形成更長的遞增子序列。因此 `dp[i] = max(dp[i], dp[j] + 1)`。

* **優點**：邏輯容易理解，是不容出錯的經典解。
* **缺點**：時間複雜度 $O(N^2)$，在資料量超過一萬時會非常慢。

```python
from typing import List

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        n = len(nums)
        # 每個數字本身就可以構成長度為 1 的子序列
        dp = [1] * n
        max_len = 1
        
        for i in range(1, n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
            max_len = max(max_len, dp[i])
            
        return max_len
```

#### B. 貪婪演算法 + 二元搜尋 (Greedy + Binary Search) —— **震撼面試官的最佳解**

**思路**：
我們維護一個陣列 `sub`，用來儲存當前構造的「最具潛力成為最長遞增子序列」的元素組合。
* 遍歷 `nums`，如果 `nums[i]` 比 `sub` 的最後一個元素還大，直接將其加入 `sub` 的尾端。
* 如果 `nums[i]` 比較小，我們找出 `sub` 當中**第一個大於等於** `nums[i]` 的元素，並將它替換成 `nums[i]`。
* **原因**：替換不會改變目前 LIS 的長度，但把結尾數字變小，未來更有機會接上其他數字。這個「尋找替換位置」的過程可以使用 Binary Search 來達成 $O(\log N)$。

```python
from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        sub = []
        
        for num in nums:
            # 如果 sub 為空，或 num 大於 sub 中的最大值，直接追加
            if len(sub) == 0 or num > sub[-1]:
                sub.append(num)
            else:
                # 找到 sub 中第一個大於等於 num 的位置並替換
                # 這能讓 sub 的元素盡量小，增加後續接上更大數字的機率
                idx = bisect.bisect_left(sub, num)
                sub[idx] = num
                
        return len(sub)
```

---

### 3. 實務應用場景

#### 1. 版本控制與 Diff 演算法 (Diff Tools)
* **應用**：計算兩個文本或程式碼檔案差異的底層核心 (Git diff) 大量運用了 LIS 與 LCS。當我們要找到最少步驟將檔案 A 轉為檔案 B 時，尋找「最長遞增子序列」能幫助定位不需要修改的基準錨點。

#### 2. 顯示卡渲染的遮擋剔除 (Occlusion Culling)
* **應用**：在電腦圖學處理 3D 場景到 2D 螢幕的映射時，判斷一系列覆蓋物的前後順序（深度測試的優化），可運用 LIS 來找出最長不被破壞的前後層級序列。

---

### 4. 總結筆記

| 比較維度 | 動態規劃 (DP) | 貪婪 + 二分搜尋 |
| --- | --- | --- |
| **時間複雜度** | $O(N^2)$ | $O(N \log N)$ |
| **空間複雜度** | $O(N)$ 給 `dp` 陣列 | $O(N)$ 給 `sub` 陣列 |
| **狀態意義** | 精確包含每一個數字結尾的最佳長度 | `sub` **不一定**是實際的原初子序列，只是長度正確 |
| **實戰心法** | 面試先寫這題保底 | 寫完必定要被 Follow-up $O(N \log N)$ 的寫法 |
