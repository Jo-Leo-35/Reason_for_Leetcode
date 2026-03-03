### 1. 核心題意與挑戰

找出給定字串 `s` 中**不含有重複字元**的最長子字串的長度。
* 子字串 (Substring) 必須是連續的。

* **隱藏挑戰**：如果是暴力解，枚舉所有子字串再檢查是否重複，時間複雜度高達 $O(N^3)$，即使優化成 $O(N^2)$ 也太慢。字串題首選 $O(N)$ 線性解。

---

### 2. 解法對比與完整程式碼

#### A. 集合管理的滑動窗口 (Sliding Window w/ Set) —— **最通用標準解**

**思路**：
維護一個窗口 (Window)，用兩個指針 `left` 和 `right` 表示窗口的左右邊界。
用一個 `Set` 來記錄窗口內出現過的字元。
`right` 指針不斷向右擴展，嘗試把新字元加入窗口。
如果遇到已經存在於 `Set` 的字元，代表發生了重複！此時 `left` 指針必須不斷向右移動，並且沿途把字元從 `Set` 中剔除，直到那個重複的字元被移出窗口為止。
過程中紀錄最大的窗口長度。

* **優點**：邏輯穩定，最符合滑動窗口的思考模型。
* **時間複雜度**：$O(2N) = O(N)$，最差情況下每個字元進出 Set 各一次。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            # 只要新字元有重複，left 就開始收縮，直到沒有重複
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
                
            # 確認無重複後加入，更新最大長度
            char_set.add(s[right])
            max_len = max(max_len, right - left + 1)
            
        return max_len
```

#### B. Hash Map 跳躍優化的滑動窗口 (Optimized Window) —— **面試官最愛的高效解**

**思路**：
前一個解法中，`left` 指針是一步一步慢慢爬的 $(left += 1)$，非常浪費時間。
如果我們用一個字典 (`dict`) 記錄每一個字元「**最後一次出現的 index**」。
當我們在 `right` 位置遇到重複字元 `s[right]` 時，我們可以直接把 `left` **瞬間跳躍**到該字元上次出現位置的「下一個位置」！

* **隱藏細節**：如果那個重複字元上次出現的位置，**已經不在目前的窗口內**（即小於 `left`），那我們就不該跳回去。`left` 只能往前走，不能退後。

* **優點**：時間複雜度嚴格限制在 $O(N)$，指針不會倒退或是一步步爬。

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index_map = {}
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            char = s[right]
            
            # 如果發現重複字元，且該字元上次出現的位置在當前窗口內
            if char in char_index_map and char_index_map[char] >= left:
                # 瞬間跳躍：將 left 移到該重複字元的下一個位置
                left = char_index_map[char] + 1
                
            char_index_map[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len
```

---

### 3. 實務應用場景

#### 1. 網路協定封包解析 (TCP Window)
* **應用**：TCP 傳輸中的 Sliding Window Protocol 用來控制流量與確認封包。當接收端發現重複的 Sequence Number，會對接收窗口的左邊界做出類似 `left = map[char] + 1` 的滑動確認動作。

#### 2. 串流資料去重 (Streaming Deduplication)
* **應用**：在處理感測器即時收到的連續訊號時，若要在一定時間段內找尋不重複的最高峰特徵，這演算法提供了最佳的實時 $O(N)$ 處理框架。

---

### 4. 總結筆記

| 比較維度 | Sliding Window (Set) | Sliding Window (Dict) |
| --- | --- | --- |
| **時間複雜度** | $O(N)$ (常數為 2) | $O(N)$ (常數為 1) |
| **空間複雜度** | $O(\min(N, M))$ （$M$為字符集大小） | $O(\min(N, M))$ |
| **推進方式** | `left` 步步進逼 | `left` 瞬間跳躍 |
| **推薦度** | 邏輯最直覺，好背 | **高鑑別度解答** |
