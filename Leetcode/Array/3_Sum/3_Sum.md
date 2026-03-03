### 1. 核心題意與挑戰

給你一個整數陣列 `nums`，請你找出**所有和為 0 且不重複的**三元組 `[nums[i], nums[j], nums[k]]`。

* **關鍵限制**：
  * **不重複**！`[-1, 0, 1]` 和 `[0, -1, 1]` 算作同一個組合。這意味著不能只用暴力找然後丟進 Set，那樣在長陣列下依然可能 TLE 超時並且非常低效。

---

### 2. 解法對比與完整程式碼

#### 唯一面試正解：排序 + 雙向夾擊法 (Sorting + Two Pointers)

**思路**：
1. **排序是濾重的基石**：先將原陣列排序。只要前面的數字固定了，如果後面遇到相同的數字，我們就可以直接 `continue` 跳過，輕易避免重複的三元組。
2. **將 3Sum 降維成 2Sum**：遍歷排序好的陣列，把當前的數字當作靶心 (`target = -nums[i]`)。接下來，只要在剩下的右半部陣列中，尋找某兩個數字相加等於 `target` 即可。
3. **因為已排序，用頭尾雙向指針**：如果 `nums[left] + nums[right] < target`，代表數字太小，`left` 要往右移。如果大於 `target`，`right` 要往左移。一旦等於，就紀錄進入答案。
4. **內外層都要防重複**：找到了答案後，`left` 和 `right` 都要跳過與它們自己相鄰的重複數字。

* **時間複雜度**：$O(N^2)$ (外層迴圈 $N$ * 內層雙指針掃描 $N$。外加一開始的排序 $O(N \log N)$，故整體仍為 $O(N^2)$)
* **空間複雜度**：$O(1)$ 到 $O(N)$ (取決於排序演算法本身是否要求額外空間)。

```python
from typing import List

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()  # 關鍵：排序，讓重複元素相鄰，並支持雙指針
        
        for i in range(len(nums) - 2):
            # 1. 最外層迴圈避免重複解
            if i > 0 and nums[i] == nums[i - 1]:
                continue
                
            # 2. 如果選定的最小數字就已經大於 0 了，後面再怎麼加都不可能等於 0，提早結束
            if nums[i] > 0:
                break
                
            # 3. 進入 2Sum 的雙指針搜索
            left, right = i + 1, len(nums) - 1
            
            while left < right:
                total_sum = nums[i] + nums[left] + nums[right]
                
                if total_sum < 0:
                    left += 1
                elif total_sum > 0:
                    right -= 1
                else: # 找到了和為 0 的三元組！
                    res.append([nums[i], nums[left], nums[right]])
                    
                    # 4. 內層迴圈收縮時，雙指針跳過相鄰的重複數字
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                        
                    # 兩邊指針雙雙推進一步
                    left += 1
                    right -= 1
                    
        return res
```

---

### 3. 實務應用場景

這題表面上是純數字遊戲，但「K-Sum 模型」在科學界極具價值：

#### 1. 碰撞檢測與物理引擎 (Collision & Force Balance)
* **應用**：在圖形學的物理運算引擎中，計算多個質點在某個向量空間下，是否存在「力的完美抵消」（總合為零向量 = 靜力平衡）。透過降維拆解 (從 3D 降成多個 2D 指針推演)，能做高速的空間碰撞剔除。

#### 2. 密碼學系統的解空間探索 (Subset Sum Problem)
* **應用**：3Sum 問題本質上是最簡單的 Subset Sum Problem 的多項式時間特例。這與許多公鑰密碼學加密強度的抗窮舉模型有關。

---

### 4. 總結筆記

| 面試易錯點清單 | 防衛性程式碼 |
| --- | --- |
| 忘了要先排序 | `nums.sort()` |
| 為了濾重複，外層迴圈沒有比較上一位 | `if i > 0 and nums[i] == nums[i-1]: continue` |
| 沒有防呆全正數的情況 | `if nums[i] > 0: break` |
| 在找到解之後，讓指標「跳過所有一樣的連號數字」 | 兩個 `while` 迴圈過濾 `left` 和 `right` 的相鄰重複 |
