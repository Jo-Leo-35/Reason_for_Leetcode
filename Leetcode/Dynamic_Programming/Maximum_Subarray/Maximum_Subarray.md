### 1. 核心題意與挑戰

給定一個整數陣列 `nums`，找到一個具有**最高總和**的**連續子陣列**（子陣列最少包含一個元素），返回其最高總和。

* **關鍵限制**：
  * $1 \le nums.length \le 10^5$
  * 必須是連續的。
* **隱藏挑戰**：因為存在負數，加了負數總和會變小。如果在遍歷陣列時前面的總和已經變成了負數，它對於未來的子陣列只會是個累贅。

---

### 2. 解法對比與完整程式碼

#### A. 貪婪 / DP：Kadane’s Algorithm —— **極致優雅的 O(N) 一次遍歷**

**思路**：
這是一維 DP 的極致壓縮版。定義 `curr_sum` 為「包含當前數字的連續子陣列最大和」。
當我們走到 `nums[i]` 時，我們只有兩個選擇：
1. **加入前面的子陣列**：`curr_sum = curr_sum + nums[i]`
2. **自己另起爐灶當作新的子陣列的頭**：`curr_sum = nums[i]`
什麼時候要另起爐灶？當前面的 `curr_sum` 小於 0 的時候，因為負數加上自己，只會讓自己變得更小。
轉移式等價於：`curr_sum = max(nums[i], curr_sum + nums[i])`。

* **優點**：時間複雜度 $O(N)$，空間複雜度 $O(1)$。
* **缺點**：無，這就是標準最佳解。

```python
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0
            
        max_sum = nums[0]
        curr_sum = 0
        
        for num in nums:
            # 如果前面累積的是負資產，果斷拋棄，從這一個 num 重新開始
            if curr_sum < 0:
                curr_sum = 0
                
            curr_sum += num
            
            # 隨時更新歷史最大值
            if curr_sum > max_sum:
                max_sum = curr_sum
                
        return max_sum
```

*(註：另一種寫法 `curr_sum = max(num, curr_sum + num)` 也是完全一樣的邏輯。)*

#### B. 分治法 (Divide & Conquer) —— **面試官專屬 Follow-up**

**思路**：
線段樹 (Segment Tree) 的基礎思想。將陣列切成左右兩半，最大子陣列必然存在於：
1. 完全在左半邊。
2. 完全在右半邊。
3. 跨越中間的反折點。
算出這三者的最大值即為答案。

* **優點**：可以延伸至解決「區間查詢最大子陣列和」的系統設計，且適合分散式平行運算。
* **時間複雜度**：$O(N \log N)$

```python
from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        
        def divide_conquer(l, r):
            if l == r:
                return nums[l]
                
            mid = (l + r) // 2
            
            # 1. 遞迴計算左右半部的最大和
            left_max = divide_conquer(l, mid)
            right_max = divide_conquer(mid + 1, r)
            
            # 2. 計算跨越中線的最大和
            # 由中間向左延伸
            best_left_cross = float('-inf')
            curr = 0
            for i in range(mid, l - 1, -1):
                curr += nums[i]
                best_left_cross = max(best_left_cross, curr)
                
            # 由中間向右延伸
            best_right_cross = float('-inf')
            curr = 0
            for i in range(mid + 1, r + 1):
                curr += nums[i]
                best_right_cross = max(best_right_cross, curr)
                
            cross_max = best_left_cross + best_right_cross
            
            return max(left_max, right_max, cross_max)
            
        return divide_conquer(0, len(nums) - 1)
```

---

### 3. 實務應用場景

#### 1. 股票與財報漲跌趨勢分析
* **應用**：找出一支股票在某段時間內（連續天數）波動獲利最大的區間，即將每天的漲跌幅化為陣列中的正負數，然後套用求最大子陣列和。

#### 2. 電腦視覺特徵提取 (Haar-like Features)
* **應用**：在影像處理的積分圖 (Integral Image) 中，尋找對比度反差最大的相鄰區塊，常利用最大連續區域的快速求和技巧。

---

### 4. 總結筆記

| 比較維度 | Kadane's Algorithm | 分治法 (Divide & Conquer) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N \log N)$ |
| **空間複雜度** | $O(1)$ | $O(\log N)$ (遞迴堆疊) |
| **可擴展性** | 靜態資料一次性處理 | 可結合線段樹處理動態修改與區間查詢 |
| **演算法精神** | 「及時止損」(捨棄負和) | 「分而治之，再做整合」 |
