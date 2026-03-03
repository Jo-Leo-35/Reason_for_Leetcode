from typing import List
from collections import defaultdict

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
        
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        # Union-Find processing indices instead of raw strings: O(N log N)
        uf = UnionFind(len(accounts))
        email_to_id = {}
        
        # Determine the connected components based on overlapping emails
        for i, account in enumerate(accounts):
            for email in account[1:]:
                if email in email_to_id:
                    uf.union(i, email_to_id[email])
                else:
                    email_to_id[email] = i
                    
        # Group emails together under each unified component's root ID
        id_to_emails = defaultdict(list)
        for email, acc_id in email_to_id.items():
            root_id = uf.find(acc_id)
            id_to_emails[root_id].append(email)
            
        # Format the final result
        result = []
        for root_id, emails in id_to_emails.items():
            name = accounts[root_id][0]
            result.append([name] + sorted(emails))
            
        return result
