class UnionFind:
  def __init__(self):
    self.groups = {}
  
  def find(self, x:str) -> str:
    """ 找 x 最大的 parent 並且路徑壓縮 """
    if x not in self.groups:
      self.groups[x] = x
    
    if self.groups[x] != x: #如果 x 不等於x自己, x還有parent, 去path compression
      self.groups[x] = self.find(self.groups[x])

    return self.groups[x]
  
  def union(self, x:str, y:str) -> None:
    root_x = self.find(x)
    root_y = self.find(y)
    if root_x != root_y:
      self.groups[root_y] = root_x

import collections
class Solution:
  
  def accountsMerge(self, accounts: list[list[str]]) -> list[list[str]]:
    
    unionTool = UnionFind()
    email_to_name = {}

    for account in accounts:
      name = account[0]
      first_email = account[1]

      for email in account[1:]:
        email_to_name[email] = name #紀錄每一個email所對應的name
        unionTool.union(first_email, email)
    
    compoents = collections.defaultdict(list)

    for email in email_to_name:
      root = unionTool.find(email)
      compoents[root].append(email)

    response = []
    
    for root_email, email_list in compoents.items():
      name = email_to_name[root_email]
      response.append([name] + sorted(email_list))
    
    return response
