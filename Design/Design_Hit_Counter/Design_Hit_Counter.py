from collections import defaultdict

class HitCounter:
    def __init__(self):
        # bucket_id -> { timestamp -> count }
        self.timemap = defaultdict(lambda: defaultdict(int))

    def hit(self, timestamp: int) -> None:
        bucket = timestamp // 300
        self.timemap[bucket][timestamp] += 1

    def getHits(self, timestamp: int) -> int:
        bucket = timestamp // 300
        # 主動清理機制：保留最近兩個區間，刪除其餘
        for old_id in list(self.timemap.keys()):
            if old_id < bucket - 1:
                del self.timemap[old_id]

        total = 0
        # 遍歷當前與上一個桶子的 keys
        for b_id in [bucket, bucket - 1]:
            if b_id in self.timemap:
                for t, cnt in self.timemap[b_id].items():
                    if timestamp - t < 300:
                        total += cnt
        return total