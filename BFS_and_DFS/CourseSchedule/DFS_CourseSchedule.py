from collections import defaultdict

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for course, prereq in prerequisites:
            graph[prereq].append(course)
        
        #0=未訪問, 1=訪問中, 2=已完成
        state = [0] * numCourses
    
        for i in range(numCourses):
            # 如果發現任何一個節點無法完成 (return False)，整題就是 False
            if not self._dfs(i, state, graph):
                return False
                
        return True
    
    def _dfs(self, node , state, graph):
        # 發現環 (死鎖)
        if state[node] == 1: 
            return False
        # 安全
        if state[node] == 2: 
            return True
        
        state[node] = 1
        for neighbor in graph[node]:
            if not self._dfs(neighbor, state, graph): 
                return False
        
        state[node] = 2
        return True