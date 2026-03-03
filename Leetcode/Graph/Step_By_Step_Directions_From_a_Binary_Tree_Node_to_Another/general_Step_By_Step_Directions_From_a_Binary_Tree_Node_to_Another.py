'''
演算法步驟：
1. 本題是經典找路問題。在二元樹中，不管從起點走到終點的路再怎麼崎嶇，本質上就是先從起點一路往上爬到兩人的「最低共同祖先 (Lowest Common Ancestor, LCA)」，然後再從 LCA 像溜滑梯一樣筆直走到終點。
2. 所以，與其花大把時間找 LCA，我們直接寫一個暴力的 DFS（回溯法 Backtracking）：尋找「從最高點 Root 出發，怎麼到達點 A」以及「怎麼到達點 B」。
3. 我們創立一個 `find_path` 的探險隊，帶上繩索陣列 `path`。
   - 每往左走一步，我們就在繩子上綁個 'L'；每往右，綁個 'R'。
   - 如果探頭發現死路，我們就乖乖把結解開（`path.pop()` 代表回溯）。
   - 如果摸到了終點，代表繩子上綁的字串就是偉大的航道，我們宣示成功！
4. 讓我們派出探險隊分別拿回前往 `startValue` 的路徑 `path_s`，以及前往 `destValue` 的路徑 `path_d`。
5. 拿回來後我們發現，因為大家都是從 Root 出發，這兩條路徑前面有一段一定是重疊的（就是大家還沒在岔路 LCA 分手前）。這好辦！用一個 `while` 迴圈把他們兩方前面長得一模一樣的字元通通切掉（抵銷），找到那個真正的分水嶺。
6. 分手之後的 `path_s`，代表從起點要往上看回 LCA 的路。雖然當初是紀錄往下走，但我們可是要往上爬啊！所以大刀闊斧，把這條剩餘的字串長度全部換成大寫的 `'U'` (Up)。
7. 接著再加上剩下的 `path_d`，這字串完美刻畫了從 LCA 直達終點的左右路徑。
8. 兩者拼接在一起，大功告成，順利交差。這解法在時空雙維度上堪稱完美均衡。
'''
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        
        def find_path(node, target, path):
            if not node:
                return False
            if node.val == target:
                return True
                
            path.append('L')
            if find_path(node.left, target, path):
                return True
            path.pop()
            
            path.append('R')
            if find_path(node.right, target, path):
                return True
            path.pop()
            
            return False
            
        path_s = []
        path_d = []
        find_path(root, startValue, path_s)
        find_path(root, destValue, path_d)
        
        i = 0
        while i < len(path_s) and i < len(path_d) and path_s[i] == path_d[i]:
            i += 1
            
        up_moves = 'U' * (len(path_s) - i)
        down_moves = "".join(path_d[i:])
        
        return up_moves + down_moves
