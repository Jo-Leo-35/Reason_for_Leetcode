### 1. 核心題意與挑戰

給定一個整數陣列 `temperatures` 代表每天的溫度，返回一個陣列 `answer`，其中 `answer[i]` 是指對於第 `i` 天，下一個更高溫出現在幾天之後。
如果氣溫在這之後都不會升高，就用 `0` 來代替。

* **隱藏挑戰**：
  * 暴力解 $O(N^2)$ 每次都往後找一天，必定 TLE。
  * 必須使用 $O(N)$ 線性時間來解決這類「尋找下一個更大/較小元素」的問題。這是 **單調堆疊 (Monotonic Stack)** 橫空出世的招牌代表作。

---

### 2. 解法對比與完整程式碼

#### 唯一面試正解：遞減單調堆疊 (Decreasing Monotonic Stack)

**思路**：
什麼叫單調堆疊？顧名思義就是 Stack 裡面的元素會一直保持一個「單調遞減」或「單調遞增」的關係。

我們維護一個 Stack，裡面存放的是「**還沒找到下一個更高溫的日子 (的索引)**」。
因為還沒找到更高的，所以這個 Stack 裡面的溫度，**由底下到上面，必定是遞減的**（也就是越上面越冷）。

當我們遍歷到今天 `T` 時：
我們去看看 Stack 的頂端（那個最冷的一天）：
* 如果今天 `T` 比頂端還要熱！太棒了！對頂端那一天來說，他終於等到「下一個更高溫」了！
* 我們就可以把那一天 `Pop` 出來，並且計算日子差，記錄進 `answer` 裡面。
* 等等，別急著放下今天，Stack 裡面可能還有其他也需要升溫的日子。只要今天 `T` 一直大於頂端，我們就一直 `Pop` 給他們解脫。
直到今天 `T` 沒辦法再傲視群雄了（或者 Stack 空了），我們才把今天 `T` 滿懷委屈地放進 Stack 裡，等待未來的某一天來解救它。

* **時間複雜度**：$O(N)$。每個元素最多 `Push` 一次，`Pop` 一次，絕不會重複操作。
* **空間複雜度**：$O(N)$，最差情況下氣溫天天驟降，全部塞在 Stack 裡。

```python
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        ans = [0] * n
        stack = []  # 裡面存放的是日子的 索引 (Index)，而不是溫度本身
        
        for i, current_temp in enumerate(temperatures):
            # 只要 stack 不為空，且今天的溫度大於 stack 頂端的溫度
            # 代表這頂端的那一天，終於盼到了比他熱的日子！
            while stack and current_temp > temperatures[stack[-1]]:
                # 把他拿出來結算
                prev_day_index = stack.pop()
                # 紀錄他們相隔了幾天
                ans[prev_day_index] = i - prev_day_index
                
            # 結算完之前的人(或者之前根本沒人)後，把今天也推進去等待未來的救援
            stack.append(i)
            
        return ans
```

---

### 3. 實務應用場景

這套心法是資料探勘與金融量化的絕對基礎。

#### 1. 股票市場的趨勢突破 (Breakout Signals)
* **應用**：尋找「下一根突破前高的 K 線發生在幾天後」。單調堆疊可以在走訪一次歷史股價的過程中，立刻標注出所有波段的高點壓力位。

#### 2. 水壩容積計算與光照掃描 (Ray Casting / Lighting)
* **應用**：在 2D 圖形的著色演算法或物理學的光影投射中，尋找某個建築物發出的光會打到前方「第一棟比他還高的建築物」，這類「Next Greater Element (NGE)」問題全部都是靠這套來做視角剔除的。

---

### 4. 總結筆記

| 解法精神 | 說明 |
| --- | --- |
| **Monotonic Stack (單調堆疊)** | 專門處裡「尋找右(或左)邊第一個比自己大(或小)的元素」。它是解決 NGE 類題型的唯一神兵利器，務必刻在腦海裡。 |
| **裡面存的是 Index** | 新手常犯錯：把實際的值存進 Stack。這題如果不存 Index，你就會不知道這兩天到底相差幾天！ |
| **`hile stack and T > T[stack[-1]]`** | 單調堆疊的靈魂起手式，用 while 一口氣結算積壓多年的爛帳。 |
