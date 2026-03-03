### 1. 核心題意與挑戰

已知一個長度為 `n` 的陣列，原本是遞增排序的。但是它被在某個未知的位置**旋轉**了。
例如 `[0,1,2,4,5,6,7]` 可能會變成 `[4,5,6,7,0,1,2]`。
給你這個被旋轉過的陣列，請你找出其中的**最小元素**。

* **關鍵限制**：
  * **必須**在 $O(\log N)$ 時間複雜度內解決。
  * 陣列中的所有元素都是**唯一**的。
* **隱藏挑戰**：不能用 $O(N)$ 線性掃描。只要看到「排序」與「$O(\log N)$」，就要條件反射想到**二元搜尋 (Binary Search)**。不過這題的陣列已經不純淨了，如何依然利用 BS？

---

### 2. 解法對比與完整程式碼

#### 唯一正解：變形二元搜尋 (Modified Binary Search)

**思路**：
不論陣列怎麼旋轉，我們都可以保證：**若把它從中間切一半，一定有一半是連續嚴格遞增的**，而另一半則包含了旋轉的斷點（也就是最小值的所在地）。

我們設立左右雙指針 `left = 0`, `right = len(nums) - 1`。
1. 若 `nums[left] < nums[right]`，這代表從 left 到 right 根本沒有被轉斷，是一個完美升序陣列！那最小值毫無疑問就是 `nums[left]`，直接回傳。
2. 否則，找出中間點 `mid`。
3. **判斷斷點在哪裡：**
   * 如果 `nums[mid] >= nums[left]`：代表從 `left` 到 `mid` 這一整段是**連續遞增**的（這是一段完美無瑕的爬坡）。既然是連續遞增，那真正的低谷（斷點）一定不在這邊，一定在 `mid` 的**右邊**。所以 `left = mid + 1`。
   * 如果 `nums[mid] < nums[left]`：代表從 `left` 到 `mid` 之間摔了一跤（斷點在這裡）。所以最小值一定在 `mid` 本身，或者是 `mid` 的**左邊**。所以 `right = mid`。注意這裡不能是 `mid - 1`，因為 `mid` 有可能剛好就是那個最小值！

* **時間複雜度**：$O(\log N)$
* **空間複雜度**：$O(1)$

```python
from typing import List

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1
        
        while left < right:
            # 提早結束：如果這段已經是完全遞增的，最左邊的就是最小的
            if nums[left] < nums[right]:
                return nums[left]
                
            mid = left + (right - left) // 2
            
            if nums[mid] >= nums[left]:
                # 代表左半段是遞增的，真正的斷崖 (最小值) 在右半段
                left = mid + 1
            else:
                # 代表斷崖在左半段 (包含 mid 在內)，所以往左邊收縮
                right = mid
                
        # 迴圈結束時 left == right，該位置就是最小值
        return nums[left]
```

---

### 3. 實務應用場景

#### 1. 循環緩衝列表 (Circular Buffer / Ring Buffer) 的頭部定位
* **應用**：在作業系統底層或高效能日誌寫入時，常常使用固定大小的 Circular Array 來蓋層舊資料。由於被不斷覆寫，最新的 Log 和最舊的 Log 形成了一個被切斷的排序陣列 (依 Timestamp 排列)。透過 $O(\log N)$ 定位斷層，可以極速找出第一筆 (最舊) Log 的起始點。

---

### 4. 總剪筆記

| 面試易錯盲點 | 解說 |
| --- | --- |
| `mid` 的條件判斷 | 每次只和 `left` 或 `right` "其中一方" 進行比較即可。和 `left` 比是業界最慣用的寫法。 |
| 為什麼是 `right = mid`？ | 因為在旋轉陣列中，如果 `nums[mid]` 破壞了左半段的單調性，代表它是一路跌下來的。它**極度有可能是谷底本身**，所以不可把它從嫌疑名單中剃除。 |
| 沒有處理「完全沒旋轉」的情況 | `if nums[left] < nums[right]: return nums[left]` 這個 Early Return 雖然不是必需（就算不寫，跑完全局也是對的），但能省下大量不必要的搜尋。 |
