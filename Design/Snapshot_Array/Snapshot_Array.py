import bisect

class SnapshotArray:
    def __init__(self, length: int):
        # 核心結構：每個 index 儲存一個歷史紀錄列表
        # 初始狀態：每個 index 在 snap_id 0 時的值都是 0
        self.history = [[(0, 0)] for _ in range(length)]
        self.current_snap_id = 0

    def set(self, index: int, val: int) -> None:
        """語意化：更新特定索引的歷史紀錄"""
        self._update_history(index, val)

    def snap(self) -> int:
        """增加快照計數並回傳前一個 ID"""
        self.current_snap_id += 1
        return self.current_snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        """透過二分搜尋尋找特定快照時的值"""
        return self._binary_search_history(index, snap_id)

    def _update_history(self, index: int, val: int):
        # 如果在同一個 snap_id 內多次 set，只需更新最後一個值
        if self.history[index][-1][0] == self.current_snap_id:
            self.history[index][-1] = (self.current_snap_id, val)
        else:
            self.history[index].append((self.current_snap_id, val) )

    def _binary_search_history(self, index: int, snap_id: int) -> int:
        target_list = self.history[index]
        # bisect_right 找的是第一個大於 snap_id 的位置，索引減一即為所求
        # 因為我們要找的是 <= snap_id 的最後一筆紀錄
        idx = bisect.bisect_right(target_list, (snap_id, float('inf'))) - 1
        return target_list[idx][1]