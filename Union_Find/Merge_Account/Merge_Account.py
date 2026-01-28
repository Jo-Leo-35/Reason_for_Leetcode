class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, i):
        if self.parent[i] == i:
            return i
        # 路徑壓縮 (Path Compression)
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j

def accountsMerge(accounts):
    email_to_id = {}    # 建立信箱到唯一數字 ID 的映射
    email_to_name = {}  # 快速查找信箱所屬的姓名
    
    id_counter = 0
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_id:
                email_to_id[email] = id_counter
                email_to_name[email] = name
                id_counter += 1
    
    uf = UnionFind(id_counter)
    
    # 溝通前置：遍歷每個帳號，將同帳號下的所有信箱 union 在一起
    for account in accounts:
        first_email = account[1]
        for other_email in account[2:]:
            uf.union(email_to_id[first_email], email_to_id[other_email])
            
    # 整理結果：按 Root ID 分組
    merged_groups = {} # {root_id: [emails]}
    for email, eid in email_to_id.items():
        root = uf.find(eid)
        if root not in merged_groups:
            merged_groups[root] = []
        merged_groups[root].append(email)
        
    # 格式化輸出：[姓名, 排序後的信箱...]
    result = []
    for root_id, emails in merged_groups.items():
        name = email_to_name[emails[0]]
        result.append([name] + sorted(emails))
        
    return result