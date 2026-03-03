'''
演算法步驟（Manacher's Algorithm - Time Complexity Optimal）：
1. 免責聲明：Manacher(馬拉車)演算法是 O(N) 時間複雜度解決迴文的最強算法，但在面試中若非指定，通常撰寫風險極高（除非你熟記在骨子裡）。
2. Step A: 在字串之間填充無效字元 `#`，解決奇偶長度需要分別處理的麻煩（"aba" 變成 "#a#b#a#"）。
3. Step B: 利用動態規劃的概念宣告長度陣列 `p`，紀錄每個中心點的「迴文半徑」。並追蹤我們至今抵達最遠的右邊界 `R` 以及他的核心 `C`。
4. Step C: 當探索一個新的點 `i`。如果 `i` 在 `R` 的守護範圍內，我們其實可以偷窺鏡像對岸的對稱點 `mirror = 2*C - i`。如果鏡像的半徑沒超過邊界，我們能不費吹灰之力直接繼承它的長度！這就是省下大量 O(N) 時間的奧義。如果超過了，我們再手動向外暴力試探。
5. 當發現新的邊界被往右推，我們就更新王座 `R` 和 `C`。
6. 最後找出 `p` 陣列裡最大的半徑，裁切出對應的字串，就是 O(N) 的最佳解。
'''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Step A: 預處理填充符號
        T = '#'.join('^{}$'.format(s))
        n = len(T)
        P = [0] * n
        C = 0
        R = 0
        
        # Step B & C: 計算每個點臂長
        for i in range(1, n - 1):
            mirror = 2 * C - i
            
            # 若是在有效守護範圍內，先試圖直接繼承鏡像答案
            if R > i:
                P[i] = min(R - i, P[mirror])
                
            # 從保底已知重疊的地方開始暴力向外擴展
            while T[i + 1 + P[i]] == T[i - 1 - P[i]]:
                P[i] += 1
                
            # 當突破天際，推演新的王朝範圍
            if i + P[i] > R:
                C = i
                R = i + P[i]
                
        # 找出最大半徑與最長的中心
        max_len = 0
        center_index = 0
        for i in range(1, n - 1):
            if P[i] > max_len:
                max_len = P[i]
                center_index = i
                
        start = (center_index - 1 - max_len) // 2
        return s[start:start + max_len]
