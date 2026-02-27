'''
演算法步驟（基於固定大小 Buckets 的空間優先最佳解）：
1. 這是為了應對極致的記憶體限制，並達到所有操作都是 O(1) 等級的最佳解。
2. 我們不把每一次的 hit 都存起來。相反的，我們只準備兩個大小為 300 的固定一維陣列：
   - `times`: 長度為 300，每一格記錄這格「最後被更新的時間戳」。
   - `hits`: 長度為 300，每一格記錄這個「特定的時間點累計了多少次 hit」。
3. 當有 `hit(timestamp)` 進來時：
   - 我們算出它在這 300 格桶子裡的位置 `index = timestamp % 300`。
   - 如果這個位置上面記錄的「最後更新時間」竟然跟這次的 `timestamp` 不一樣，太驚險了！這代表上一輪 5 分鐘循環的舊紀錄還留在這！我們直接把這格重新刷新，將 `times[index]` 設定為新的時間，並重置次數 `hits[index] = 1`。
   - 如果這位置最後記錄的時間跟現在一樣，就代表這是同一秒發生的另外一次點擊，我們只要 `hits[index] += 1` 即可。這也是面對高併發大量點擊的完美解。
4. 當需要 `getHits(timestamp)`：
   - 遍歷我們這精緻可愛永遠只有 300 格長度的小陣列（常數時間 300 步）。
   - 如果發現這格記錄的時間，與現在的時間 `timestamp` 的差距小於 300 秒，代表它沒過期。把次數加總起來。
   - 回傳加總的數字。完美！
   - O(1) 空間與 O(1) 固定時間 (走 300 步是常數)。
'''
class HitCounter:

    def __init__(self):
        self.times = [0] * 300
        self.hits = [0] * 300

    def hit(self, timestamp: int) -> None:
        idx = timestamp % 300
        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1

    def getHits(self, timestamp: int) -> int:
        total = 0
        for i in range(300):
            if timestamp - self.times[i] < 300:
                total += self.hits[i]
        return total
