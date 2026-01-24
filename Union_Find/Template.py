class UnionFind:
    def __init__(self):
        """
        初始化：
        1. parents: 記錄每個節點的老闆 (key: node, value: parent)
        2. ranks: 記錄該集合的深度/大小，用於優化合併 (key: root, value: rank)
        3. count: 記錄目前有多少個獨立的集合 (連通分量)
        """
        self.parents = {}
        self.ranks = {}
        self.count = 0 

    def add(self, x):
        """
        新增節點 (若不存在才新增)
        初始化時，自己是自己的老闆 (root)，秩 (rank) 為 0
        """
        if x not in self.parents:
            self.parents[x] = x
            self.ranks[x] = 0
            self.count += 1

    def find(self, x):
        """
        尋找 x 的根節點 (Root)
        核心優化：路徑壓縮 (Path Compression)
        """
        if x not in self.parents:
            return None # 或是根據題目需求拋出異常 / 自動 add(x)
        
        # 遞迴查找，回傳時順便把沿途節點直接掛到 Root 下
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        
        return self.parents[x]

    def union(self, x, y):
        """
        合併 x 和 y 所在的集合
        核心優化：按秩合併 (Union by Rank)
        回傳：True 表示合併成功 (原本不同組)，False 表示原本就是同組
        """
        root_x = self.find(x)
        root_y = self.find(y)

        # 1. 如果根本不存在 (防禦性編碼)，可選擇自動 add 或 return
        if root_x is None or root_y is None: return False

        # 2. 已經同組，不做事
        if root_x == root_y:
            return False

        # 3. 按秩合併：將「矮」的樹合併到「高」的樹下
        if self.ranks[root_x] > self.ranks[root_y]:
            self.parents[root_y] = root_x
        elif self.ranks[root_x] < self.ranks[root_y]:
            self.parents[root_x] = root_y
        else:
            # 高度相同，誰併誰沒差，但被併入的 Root 高度要 +1
            self.parents[root_y] = root_x
            self.ranks[root_x] += 1
        
        # 4. 合併成功，連通分量少一個
        self.count -= 1
        return True