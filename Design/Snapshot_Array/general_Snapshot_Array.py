'''
演算法步驟（歷史標籤紀錄與二分搜）：
1. 如果要在 O(1) 的空間擴張下實作快照系統，我們就絕對不可以在每一次 Snap() 都建立 Array 的複本。
2. 每一個 index 我們都給他建立一個屬於他的迷你時光機陣列。
   - 在陣列一開始，我們在第 0 代的時候，存放值為 0（例如：[(0, 0)]）。
3. 當呼叫 `set(index, val)`：
   - 我們去他的時光機裡面看看最後一次記錄的修改。
   - 如果最後修改的那一代，跟他現在系統正在處於的 `curr_snap_id` 一模一樣！代表目前他還在同一個宇宙紀元，我們直接覆蓋掉他最後那筆修改成 `val`。
   - 如果大時代已經演進了（這代表自從上次有新一代 Snap 誕生後，這是他第一筆修改），我們就在他個人時光機中追加一條紀錄：`(現在的世代, val)`。
4. 當需要 `snap()` 時，太爽了，時間推進 `curr_snap_id += 1`，並回傳上一個世代編號。O(1) 時間解決。 
5. 當被呼叫 `get(index, snap_id)` 想要查歷史紀錄：
   - 把這個點的迷你時光機陣列調出來看。由於時間一定是不斷往前的，所以時光機陣列裡的世代一定是由小而大排序過的。
   - 使用 `Binary Search (二分搜)`，去找尋這個時光機陣列裡面「小於或等於目標 `snap_id`」的那一筆最新紀錄在哪裡。
6. 這個技巧 (Lazy Initialization with Binary Search lookup) 展現了系統工程中最極致的歷史資源保存術。
'''
import bisect

class SnapshotArray:

    def __init__(self, length: int):
        self.history = [[(0, 0)] for _ in range(length)]
        self.curr_snap_id = 0

    def set(self, index: int, val: int) -> None:
        records = self.history[index]
        if records[-1][0] == self.curr_snap_id:
            records[-1] = (self.curr_snap_id, val)
        else:
            records.append((self.curr_snap_id, val))

    def snap(self) -> int:
        self.curr_snap_id += 1
        return self.curr_snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        records = self.history[index]
        
        # 利用 Binary Search 找剛好大於查找目標值的後一位
        # 退回一步，就是這個時間點當下的合法值
        idx = bisect.bisect_right(records, (snap_id, float('inf')))
        return records[idx - 1][1]
