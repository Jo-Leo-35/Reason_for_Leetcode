'''
演算法步驟：
1. 目標是在時間旅行的單趟走訪中，買低賣高，賺取最大價差。
2. 我們需要兩個變數：`min_price` 紀錄從盤古開天至今碰過「歷史最低的價格」，一開始設為無限大；`max_profit` 記錄「歷史上發生過最賺錢的波段」，一開始是 0。
3. 開始歷遍股價陣列：
   - 今日股價 `price` 跟 `min_price` 做比較。如果今天破底了！太好了，我們把 `min_price` 更新為今天的價格（代表這是未來的最佳買點）。
   - 如果今天沒有破底，這代表我們可以試著在今天「賣出」！
   - 我們計算若在這一天賣出賺到的價差：`price - min_price`。
   - 拿去跟歷史波段神話 `max_profit` 挑戰，如果超過了，則更新破紀錄。
4. 單趟 O(N) 一次掃完，不佔用額外空間 O(1)，回傳 `max_profit`。
'''
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
            
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            if price < min_price:
                min_price = price
            elif price - min_price > max_profit:
                max_profit = price - min_price
                
        return max_profit
