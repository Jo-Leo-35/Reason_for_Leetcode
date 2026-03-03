'''
演算法步驟：
1. SnapshotArray 的通用最佳解 (利用二分搜尋的 Delta Update) 已經是時空的顛峰，但這支檔案作為提醒紀錄這題的禁忌(Taboo)。
2. 本檔案使用 Deep Copy 進行模擬，僅供反思：如果在真實的大型面試場合給出這套方案，這絕對會導致 Memory Limit Exceeded (MLE) 或 Time Limit Exceeded (TLE) 並拿 到 Lean Hire / Rejection。
3. 暴力複製法：
   - 準備一個二維陣列 `self.snapshots`。
   - 一個當下的操作副本 `self.current_array`。
   - 每次 `snap()` 就把整個 `current_array` Deep Copy（透過 `list()` 或是 `[:]`）並儲存。這是一維度上佔用 O(N) 空間，整體隨快照次數 O(S * N) 爆炸。
'''
class SnapshotArray_BAD_EXAMPLE_ONLY:

    def __init__(self, length: int):
        self.current_array = [0] * length
        self.snapshots = []
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        self.current_array[index] = val

    def snap(self) -> int:
        # 浪費空間的行為：完全拷貝未修改過的無用 0 值以及重複資訊
        self.snapshots.append(self.current_array[:])
        
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        return self.snapshots[snap_id][index]
