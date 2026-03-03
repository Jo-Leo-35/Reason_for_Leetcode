from typing import List

class IntervalManager:
    """
    這是一個處理區間問題的通用模板。
    核心理念：將邏輯拆分為『排序』、『重疊判斷』與『合併/處理』。
    """

    def process_intervals(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []

        # 1. 前置處理：確保區間按起點排序 (這是 90% 題目的起點)
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        
        results = []
        # 初始化第一個區間作為當前比較的基礎
        current_interval = sorted_intervals[0]

        for i in range(1, len(sorted_intervals)):
            next_interval = sorted_intervals[i]

            # 2. 核心判斷：是否重疊？
            if self._is_overlapping(current_interval, next_interval):
                # 3. 執行合併邏輯 (例如 Merge Intervals)
                current_interval = self._merge(current_interval, next_interval)
            else:
                # 4. 若不重疊，則將舊區間存入結果，並移動指針
                results.append(current_interval)
                current_interval = next_interval

        # 加入最後一個處理中的區間
        results.append(current_interval)
        return results

    def _is_overlapping(self, a: List[int], b: List[int]) -> bool:
        """判斷兩區間是否重疊：前一個的結束點 >= 後一個的起始點"""
        return a[1] >= b[0]

    def _merge(self, a: List[int], b: List[int]) -> List[int]:
        """合併兩重疊區間：起點取最小（已排序則維持不變），終點取最大"""
        return [a[0], max(a[1], b[1])]

# Dry Run 演示：
# Input: [[1,3], [2,6], [8,10]]
# 1. current = [1,3], next = [2,6]. 重疊！merge -> [1,6]
# 2. current = [1,6], next = [8,10]. 不重疊！append [1,6], current = [8,10]
# 3. loop 結束, append [8,10]. Result: [[1,6], [8,10]]