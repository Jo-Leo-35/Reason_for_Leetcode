### 1. 核心題意與挑戰

給定一個鏈結串列的頭節點，判斷鏈結串列中**是否有環** (Cycle)。
如果鏈結串列中有某個節點，可以通過連續跟蹤 `next` 指針再次到達，則鏈結串列中存在環。返回 `True` 否則 `False`。

* **隱藏挑戰**：能用 $O(1)$ 的記憶體來解決嗎？因為如果使用 HashSet 存下所有走訪過的節點，$O(N)$ 空間雖然好懂但無法展現鑑別度。

---

### 2. 解法對比與完整程式碼

#### A. 空間換取時間 (HashSet) —— **最直覺的解法**

**思路**：
走訪整個鏈結串列，每走過一個節點就把它的**記憶體位址** (Node 實體) 丟進 Set 中。
如果走到一個節點它已經存在於 Set 中，代表我們繞了一個圈又回來了。

* **優點**：不須動腦，非常無腦直觀。
* **缺點**：空間複雜度 $O(N)$。

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        visited = set()
        curr = head
        
        while curr:
            if curr in visited:
                return True
            visited.add(curr)
            curr = curr.next
            
        return False
```

#### B. 龜兔賽跑演算法 (Floyd's Cycle-Finding Algorithm) —— **最佳面試正解**

**思路**：
使用兩個指針：
* **慢指針 (Tortoise/Slow)**：每次走 1 步。
* **快指針 (Hare/Fast)**：每次走 2 步。

把它想像成兩人在操場跑步。如果跑道是直的（沒有環），跑得快的人絕對不會被超越，且會先抵達終點 (`fast` 變成 Null)。
如果跑道是一個環狀操場，跑得快的人終究會「套圈」從背後追上跑得慢的人。
換成數學語言：快指針每回合會拉近跟慢指針的距離 1 個節點，如果距離是一個環的長度，則必定在有限步數內相遇。

* **優點**：空間複雜度 $O(1)$ 且時間複雜度依然是 $O(N)$。

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        # 如果頭為空或只有一個節點無法成環
        if not head or not head.next:
            return False
            
        slow = head
        fast = head
        
        # fast 跑到終點前，或者是 fast 的下一步是終點前，迴圈繼續
        while fast and fast.next:
            slow = slow.next          # 走一步
            fast = fast.next.next     # 走兩步
            
            # 兩者在環內相遇了
            if slow == fast:
                return True
                
        # 只要能走出 while 迴圈，代表碰到了 Null，也就是沒有環
        return False
```

---

### 3. 實務應用場景

#### 1. 死鎖檢測 (Deadlock Detection)
* **應用**：在作業系統與資料庫設計中，如果有個資源分配圖 (Resource Allocation Graph) 形成了環，這就代表發生了死鎖（行程 A 等 B 的資源，B 等 C 的資源，C 卻在等 A）。Cycle Finding 是檢測死鎖的基石。

#### 2. 無窮迴圈檢測與偽亂數生成器分析
* **應用**：用於分析 Pseudo-Random Number Generator (PRNG) 是否進入了循環週期，這與密碼學的安全性息息相關 (Pollard's rho algorithm)。

---

### 4. 總結筆記

| 比較維度 | HashSet 解法 | 龜兔賽跑 (Fast/Slow Pointer) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ | $O(N)$ (快指針最多追逐 N 步即可相遇) |
| **空間複雜度** | $O(N)$ | $O(1)$ |
| **原理模型** | 記憶力好的探險家走過必留下痕跡 | 繞圈賽跑中的套圈相遇 |
| **面試加分項** | 僅暖身用 | 準確說出 **Floyd's Algorithm** 這個專有名詞 |
