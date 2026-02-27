'''
演算法步驟：
1. 這是經典的帶權無向圖 (Weighted Undirected Graph) 問題。我們把變數當成節點，除法的商數當成這條邊的權重 (Weight)！
   - 如果 A / B = 2.0，代表圖中有一條 A 指向 B 的單向邊，權重是 2.0。同時也有一條反向邊 B 指向 A，權重自然是它的倒數 1.0 / 2.0 = 0.5。這就是對稱的藝術！
2. 我們建立一個 `defaultdict(dict)` 型的雙層字典 `graph` 來儲存這個網狀結構。外層 key 是出發節點，內層 key 是目標節點，內層 value 就是他們兩個相處的權重。
3. 把所有的方程式通通灌進去這個雙向圖裡面。
4. 面對 `queries` 丟來的各種疑難雜症 `(C / D)`，我們派出一支名為 `bfs_find_path` 的探險隊：
   - 如果 `C` 或 `D` 根本沒在這個字宙登錄過？抱歉，回傳 -1.0。
   - 把 `C` 與身上帶著的初始積累財富 `1.0` 放進 Queue 裡，然後出發！同時帶著一個 `visited` 的 Hash Set 來留記號，避免自己在同個迴圈裡無盡輪迴。
   - 每次從 Queue 裡拿出一個點，如果這個點就是終點 `D`！那麼他身上背負的財富積累就是答案，直接榮耀回傳！
   - 如果不是終點，就跟他的左鄰右舍打招呼，如果那些鄰居沒拜訪過，就帶上自己的財富乘上那條路的過路費，把它們通通塞進 Queue 裡。
5. 探險隊如果搜遍了世界都找不到終點，就只能落寞地回傳 -1.0。
'''
from collections import defaultdict, deque
from typing import List

class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)
        
        for (u, v), val in zip(equations, values):
            graph[u][v] = val
            graph[v][u] = 1.0 / val
            
        def bfs_find_path(start, end):
            if start not in graph or end not in graph:
                return -1.0
                
            queue = deque([(start, 1.0)])
            visited = set()
            visited.add(start)
            
            while queue:
                curr_node, curr_product = queue.popleft()
                
                if curr_node == end:
                    return curr_product
                    
                for neighbor, weight in graph[curr_node].items():
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, curr_product * weight))
                        
            return -1.0
            
        return [bfs_find_path(c, d) for c, d in queries]
