from collections import defaultdict, deque
from typing import List

class Solution:
    """
    通用 Khan's Algorithm (Topological Sort) 學習模板
    
    核心思想:
    1. 計算每個節點的入度 (Indegree)。
    2. 入度為 0 的節點表示沒有依賴 (或依賴已解決)，可以被 "處理" (放入 Queue)。
    3. 處理節點時，將其從圖中 "移除" (即減少其鄰居的入度)。
    4. 如果鄰居的入度變為 0，則該鄰居也可以被處理。
    
    適用場景:
    - 依賴關係解析 (Dependency Resolution)
    - 課程安排 (Course Schedule)
    - 編譯順序 (Compilation Order)
    - 檢測有向圖是否有環 (Cycle Detection)
    """
    
    def khanAlgorithmTemplate(self, numCourses: int, prerequisites: List[List[int]]) -> any:
        # ---------------------------------------------------------
        # Step 1: 建立 Graph 與 Indegree Table
        # ---------------------------------------------------------
        graph = defaultdict(list)
        indegree = [0] * numCourses
        
        # 額外資料結構 (依題目需求選用)
        # order = []                                  # For Course Schedule II (紀錄順序)
        # item_ancestors = [set() for _ in range(n)]  # For Course Schedule IV (紀錄所有前置依賴)

        for dest, src in prerequisites:
            # 題目通常給 [course, prerequisite]，代表 src -> dest
            # 視題目定義調整方向
            graph[src].append(dest)
            indegree[dest] += 1
            
        # ---------------------------------------------------------
        # Step 2: 初始化 Queue
        # ---------------------------------------------------------
        # 將所有 "初始可執行" (Indegree == 0) 的節點加入 Queue
        queue = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                queue.append(i)
        
        # 用於計算已處理的節點數量 (判斷是否有環)
        processed_count = 0
        
        # ---------------------------------------------------------
        # Step 3: BFS 處理
        # ---------------------------------------------------------
        while queue:
            current = queue.popleft()
            processed_count += 1
            
            # [Optional] 紀錄順序 (Course Schedule II)
            # order.append(current)

            for neighbor in graph[current]:
                # 關鍵操作: 減少鄰居的 Indegree (模擬移除依賴)
                indegree[neighbor] -= 1
                
                # [Optional] 傳遞依賴資訊 (Course Schedule IV)
                # item_ancestors[neighbor].add(current)
                # item_ancestors[neighbor].update(item_ancestors[current])
                
                # 如果 Indegree 歸零，表示所有前置依賴已解決，加入 Queue
                if indegree[neighbor] == 0:
                    queue.append(neighbor)
        
        # ---------------------------------------------------------
        # Step 4: 回傳結果 (依題目需求)
        # ---------------------------------------------------------
        
        # 判定是否有環 (Course Schedule I):
        # 如果處理的節點數 != 總數，代表有環 (Cycle Detected)
        if processed_count != numCourses:
            return False # 或 return []
            
        # Course Schedule I: Return True/False
        return True 

        # Course Schedule II: Return Topological Order
        # return order
        
        # Course Schedule IV: Return Reachability Map
        # return item_ancestors
