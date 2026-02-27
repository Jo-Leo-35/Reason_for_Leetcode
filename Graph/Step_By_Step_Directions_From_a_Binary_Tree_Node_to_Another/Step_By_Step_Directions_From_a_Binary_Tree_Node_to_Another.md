### 1. 核心題意與挑戰

隨便給定一棵二元樹，然後給你兩個特定的節點值 `startValue` 和 `destValue`。
請你找出從 `start` 走到 `dest` 的**最短路徑**。路徑用字串表示：
* 往左下走是 `'L'`
* 往右下走是 `'R'`
* 往祖先上面走是 `'U'`

* **隱藏挑戰**：
  * 在一棵只有向下的樹中，要怎麼「往上走」？
  * 這是 2021 年 Google 經典面試題，融合了「LCA (最近共同祖先)」和「樹狀搜索」兩大重點。

---

### 2. 解法對比與完整程式碼

#### 第一性原理拆解法 —— **思路最清晰的面試滿分解**

**思路**：
兩個節點在樹中最近碰面的地方叫做**最近共同祖先 (Lowest Common Ancestor, LCA)**。
如果我們要從 `S` 走到 `D`，那這條路徑必然可拆解為：
1. **爬坡段**：從 `S` 一路往上爬，直到遇見 LCA（這一段全部都是 `'U'` 步！）。
2. **下坡段**：從 LCA 開始，往下抵達 `D`（這一段只會有 `'L'` 和 `'R'`）。

所以我們其實**不需要真的跑一次 LCA 演算法！**
我們只需要：
1. 把從 `Root` 出發，到達 `S` 的路徑找出來（例如字串：`"LRL"`）。
2. 把從 `Root` 出發，到達 `D` 的路徑找出來（例如字串：`"LRR"`）。
3. **消除前綴**：你看這兩個字串都有共同的前綴 `"LR"`。這代表什麼？代表他們都在跨過 `"LR"` 之後才開始分道揚鑣（而這個分道揚鑣的岔路口就是 LCA！）。
4. 我們把共同的前置路徑 `"LR"` 砍掉！
   * 那 `S` 剩下來特有的路徑就是 `"L"`，長度是 1。這意味著：從 LCA 落實到他家，要走 1 步。反過來說，他要爬回家長 LCA 的身邊，就必須走出同等長度的 `'U'`。
   * 那 `D` 剩下來特有的路徑就是 `"R"`。我們完全不用改變它的字母，因為從 LCA 出發本來就是要按照這些方向走！

* **時間複雜度**：$O(N)$ (走進去樹幾次找字串)
* **空間複雜度**：$O(N)$

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        
        # 1. 輔助函式：用來找出從 root 到 targetNode 的路徑
        def find_path(node, target, path):
            if not node:
                return False
                
            if node.val == target:
                return True
                
            # 嘗試往左走
            path.append('L')
            if find_path(node.left, target, path):
                return True
            path.pop() # 此路不通，退回
            
            # 嘗試往右走
            path.append('R')
            if find_path(node.right, target, path):
                return True
            path.pop() # 此路不通，退回
            
            return False
            
        # 分別找出到起點跟到終點的完整路線
        path_s = []
        path_d = []
        find_path(root, startValue, path_s)
        find_path(root, destValue, path_d)
        
        # 2. 去除兩條字串的「共同前綴 (LCA 之前的路段)」
        i = 0
        while i < len(path_s) and i < len(path_d) and path_s[i] == path_d[i]:
            i += 1
            
        # 3. 把剩下的 path_s 全部轉換成 'U'
        up_moves = 'U' * (len(path_s) - i)
        
        # 4. 把剩下的 path_d 直接轉為字串接上去
        down_moves = "".join(path_d[i:])
        
        return up_moves + down_moves
```

---

### 3. 實務應用場景

#### 1. DOM 節點導航 (Relative DOM Element Traversal)
* **應用**：在寫前端 React 測試或網頁爬蟲時。你拿到了一個超深層的 Footer 元素，你想透過 XPath 或是 `parentElement` 找到另外一個掛在隔壁的 Header 內的按鈕。「向上尋找直到共用 Layout 容器再向下挖」，這是不給絕對 ID 情況下的唯一導航法。

#### 2. 版本控制分支尋址 (Git Cherry-pick / Diff Target)
* **應用**：你在 git branch A，要在這個分支合流 Branch B。Git 的底層必須找出兩個分支最後一次的共同 Commit (LCA Base)，然後把你從共同點分岔開始的 `path_s` 解除了衝突變成 Reverse 的操作，合併上 `path_d` 的 Diff 修改。

---

### 4. 總結筆記

| | DFS 直接建反向邊 | 共同路徑消解法 |
| --- | --- | --- |
| **面試喜好度** | 較低。因為你必須為每個節點掛上 `.parent` 變成雙向圖再跑 BFS。會讓本來輕薄短小的樹變得很胖。 | **絕佳優雅。** 充分展現你對「樹就是唯一無環單一路徑」特性的掌握。 |
| **心法公式** | N/A | `S 特有路徑換成 U` + `D 特有路徑保留` |
