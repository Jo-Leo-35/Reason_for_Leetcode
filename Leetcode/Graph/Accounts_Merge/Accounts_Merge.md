### 1. 核心題意與挑戰

給定一個清單 `accounts`，每個元素是一個帳戶，其中：
`accounts[i][0]` 是該帳戶的名稱 (Name)。
`accounts[i][1:]` 是一堆屬於這個人的 Email 信箱。

* **挑戰規則**：如果兩個帳戶有一個**共同的 Email**，我們就可以斷定這兩個帳戶其實是**同一個人**的。但是，如果只是「名字」剛好一樣（例如叫 John），不代表他們是同一個人！
* 你的任務是把所有屬於同一個人的 Email **合併**在一起。並保證合併後 Email 按照字母升序 (Lexicographical order) 排列。

---

### 2. 解法對比與完整程式碼

#### 唯一正解：並查集 (Union Find) —— **解決分群與連通的最佳利器**

**思路**：
這是一道把零散的 Email 聚攏起來的問題。「我們兩個有交集，所以我們屬於同一個大家族」。這句話就是 Disjoint Set (Union-Find) 的精神。

但是我們要以「誰」為依歸去合併呢？名字會重複不靠譜。
所以我們要**替每一個 Email 綁定它所屬的帳號 ID (0, 1, 2...)**！
1. **建立 Email -> 帳號 ID 的反射鏡面**：
   我們遍歷陣列。對於每個 Email，我們看看它以前出現過嗎？
   如果沒有，我們記錄下 `email_to_id[email] = i`。
   如果出現過了！那就代表我發現了「第 `i` 個帳號」其實跟以前紀錄過的那個帳號是一家人！我們趕快把它們兩個的帳號 ID 進行 `Union(i, 老朋友的ID)` 串連起來。
2. **聚沙成塔**：將整張表的 ID 合併乾淨後。我們再走一次資料，這次不是找老朋友了，我們把每封 Email 都丟去問並查集的頭目：「這封信最古老的太祖父 ID 是幾號？」把它歸檔進 `id_to_emails[太祖父ID].append(email)` 裡面。
3. **結算報告**：把 `id_to_emails` 裡面的清單拿出來排序，並補上原先他們的大名，回傳。

* **時間複雜度**：$O(N \log N)$ （$N$ 為 Email 總數，主要花在最後對 Email 清單的字串排序）。

```python
from typing import List
from collections import defaultdict

class UnionFind:
    def __init__(self, size):
        # 一開始每個帳號的祖先都是自己
        self.parent = list(range(size))
        
    def find(self, x):
        # 路徑壓縮優化 (Path Compression)
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # 將 x 接到 y 身上
            self.parent[root_x] = root_y


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        # email 映射到第一次出現時的 account index
        email_to_id = {}
        
        # 1. 找出連通的家族關係
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_id:
                    # 這封信以經被其他人報過了，代表我們是同一個人！快把兩個帳號做連接
                    uf.union(i, email_to_id[email])
                else:
                    email_to_id[email] = i
                    
        # 2. 將所有的 Email 歸給同一位最老的祖先
        id_to_emails = defaultdict(list)
        for email, acc_id in email_to_id.items():
            # 找到這封信最終的大本營
            root_id = uf.find(acc_id)
            id_to_emails[root_id].append(email)
            
        # 3. 排序並掛上名字
        result = []
        for root_id, emails in id_to_emails.items():
            name = accounts[root_id][0]
            # 題目要求對 Email 排序 (不含名字)
            result.append([name] + sorted(emails))
            
        return result
```

---

### 3. 實務應用場景

本題就是各大資料庫工程師經常接觸的超級苦工：
#### 1. 跨平台帳號自動歸戶與合併 (Account Unification)
* **應用**：在開發電商平台時，一個客人可能今天用 Google 登入結帳，明天又開了一個同名的信箱去註冊 Apple 登入。過了一個月用手機號碼找回密碼。他們往往擁有互相關聯的電話、信箱、信用卡卡號指紋等資訊（本題的 Emails）。系統必須依據這些「重疊片段」在後台將所有的零散會員紀錄合併成唯一的「實體客戶輪廓 (Single Customer View)」以精準投放廣告。這往往是靠大數據 Hadoop 跑 Union-Find MapReduce 來每晚重整。

---

### 4. 總結筆記

| | DFS vs. Union Find |
| --- | --- |
| **面試表現** | Union Find 優於 DFS。因為 DFS 建圖需要雙向 HashMap 甚至字串節點，太花記憶體了。 |
| **Union Find 心法** | 我們不需要把 "john@gmail.com" 跟 "johnny@gmail.com" 合併。**我們合併的是數字 ID 0 號 跟 ID 1 號**！這大大的簡化了演算法，也是為什麼第一週要背出標準 UF 的原因。 |
