'''
演算法步驟：
1. 這一題其實是在找尋圖論中的連通單元 (Connected Components)，當牽涉到群組歸屬，首選兵器永遠是神聖的「並查集 Union Find (Disjoint Set)」。
2. 由於字串運算不僅耗記憶體又沒效率，我們巧妙地運用數字編號 `0 ~ N-1` 來代表這 `N` 個人名帳號，用數字來做 Union Find！
3. 我們宣告一個 `UnionFind` 類別，賦予他尋根 `find` (含路徑壓縮 Path Compression) 的天賦，與聯姻 `union` 的本領。
4. 建立一本電話簿 `email_to_id`：Key 是 Email，Value 是這信箱最初被誰 (帳號編號) 所見。
5. 開始歷遍每個帳號的所有 Email 財產：
   - 如果這個 Email 從沒有出現過，我們趕快把它記錄在電話簿 `email_to_id[email] = 當前的帳號 i`。
   - 如果這個 Email 竟然被人捷足先登出現過了！這絕對是抓到了同一個人的小辮子！我們馬上呼叫大祭司 `uf.union(i, 電話簿上的那位老兄)`！他們兩人的靈魂因此永遠糾纏聯集在同一棵樹上了。
6. 將所有人合併完後，我們再建立一本新的花名冊 `id_to_emails`，把世上散落的 Email 全部回歸給他們的大宗主（最終歸屬的 Root ID）。
7. 最後我們把宗主的名字抓出來，並按照規矩把底下的 Email 從小到大排序好，優雅地包裝成陣列端出去。
8. 這套帶有路徑壓縮神技的演算法，時間複雜度近乎完美的 O(N * M * α(N))，這是這張圖能達到的速度巔峰。
'''
from typing import List
from collections import defaultdict

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        
    def find(self, x):
        if self.parent[x] != x:
            # 神聖路徑壓縮 (Path Compression)
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        email_to_id = {}
        
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_id:
                    uf.union(i, email_to_id[email])
                else:
                    email_to_id[email] = i
                    
        id_to_emails = defaultdict(list)
        for email, acc_id in email_to_id.items():
            root_id = uf.find(acc_id)
            id_to_emails[root_id].append(email)
            
        result = []
        for root_id, emails in id_to_emails.items():
            name = accounts[root_id][0]
            result.append([name] + sorted(emails))
            
        return result
