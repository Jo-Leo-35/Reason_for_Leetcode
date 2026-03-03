import bisect

class SnapshotArray:

    def __init__(self, length: int):
        # Store a history of (snap_id, value) per index
        self.history = [[(0, 0)] for _ in range(length)]
        self.curr_snap_id = 0

    def set(self, index: int, val: int) -> None:
        records = self.history[index]
        # Overwrite if we are repeatedly setting within the same snapshot ID
        if records[-1][0] == self.curr_snap_id:
            records[-1] = (self.curr_snap_id, val)
        else:
            records.append((self.curr_snap_id, val))

    def snap(self) -> int:
        self.curr_snap_id += 1
        return self.curr_snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        records = self.history[index]
        # Find the rightmost insertion point where the historical snap_id <= target snap_id
        idx = bisect.bisect_right(records, (snap_id, float('inf')))
        return records[idx - 1][1]

# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_3 = obj.snap()
# param_4 = obj.get(index,snap_id)