"""
微系統：雲端運算任務調度器 (Cloud Task Scheduler)
直接對應 LC 2402 - Meeting Rooms III 的雙 Heap 解法

對應關係：
    availableRooms  → availableNodes  (Min-Heap by node_id)
    ongoingMeetings → runningTasks    (Min-Heap by end_time)
    會議 [start, end] → Task(submit_time, duration)
"""

import heapq
from dataclasses import dataclass, field


# ─────────────────────────────────────────────
# 資料模型
# ─────────────────────────────────────────────

@dataclass
class Task:
    task_id: str
    submit_time: int   # 任務提交時間（↔ meeting.start）
    duration: int      # 任務執行時長（↔ meeting.end - meeting.start）
    actual_start: int = 0
    actual_end: int = 0
    node_id: int = -1

    @property
    def wait_time(self) -> int:
        return self.actual_start - self.submit_time


# ─────────────────────────────────────────────
# 核心調度器
# ─────────────────────────────────────────────

class CloudTaskScheduler:
    """
    模擬 GCP / AWS Spot Instance 排程器。

    核心不變式：
        1. availableNodes  → 永遠彈出「編號最小」的空閒節點。
        2. runningTasks    → 永遠彈出「最快釋放」的執行中節點。
        兩個 Heap 共同保證：低碎片化 + 零任務遺失。
    """

    def __init__(self, num_nodes: int):
        self.num_nodes = num_nodes
        self.node_task_count = [0] * num_nodes

        # ── 兩個 Heap（直接對應 LC 2402）──
        self.availableNodes: list[int] = list(range(num_nodes))
        heapq.heapify(self.availableNodes)          # Min-Heap by node_id

        self.runningTasks: list[tuple] = []         # Min-Heap: (end_time, node_id)
        # ──────────────────────────────────────

        self._completed: list[Task] = []
        self._logs: list[str] = []

    # ── 公開介面 ────────────────────────────

    def submit(self, task: Task) -> Task:
        """提交一個任務，回傳帶有實際排程資訊的 Task。"""
        self._release_finished_nodes(at_time=task.submit_time)

        if self.availableNodes:
            node_id = heapq.heappop(self.availableNodes)
            actual_start = task.submit_time
            actual_end   = task.submit_time + task.duration
            self._log(task.submit_time,
                      f"Task '{task.task_id}' → Node-{node_id}  "
                      f"[立即執行] start={actual_start} end={actual_end}")
        else:
            # 無空節點：等最早釋放的節點（↔ 會議延遲）
            earliest_end, node_id = heapq.heappop(self.runningTasks)
            actual_start = earliest_end
            actual_end   = earliest_end + task.duration
            self._log(task.submit_time,
                      f"Task '{task.task_id}' → Node-{node_id}  "
                      f"[延遲 +{actual_start - task.submit_time}] "
                      f"start={actual_start} end={actual_end}")

        task.node_id      = node_id
        task.actual_start = actual_start
        task.actual_end   = actual_end

        heapq.heappush(self.runningTasks, (actual_end, node_id))
        self.node_task_count[node_id] += 1
        self._completed.append(task)
        return task

    def busiest_node(self) -> int:
        """回傳處理最多任務的節點編號（↔ LC 2402 的答案）。"""
        max_count = max(self.node_task_count)
        return self.node_task_count.index(max_count)

    def report(self) -> None:
        """輸出調度結果報告。"""
        W = 60
        print("\n" + "=" * W)
        print("  調度報告 (Scheduling Report)")
        print("=" * W)

        # 任務明細
        print(f"\n{'Task ID':<12} {'提交':>5} {'開始':>5} {'結束':>5} {'節點':>7} {'等待':>5}")
        print("-" * W)
        for t in self._completed:
            wait = f"+{t.wait_time}" if t.wait_time > 0 else "-"
            print(f"{t.task_id:<12} {t.submit_time:>5} {t.actual_start:>5} "
                  f"{t.actual_end:>5} {'Node-'+str(t.node_id):>7} {wait:>5}")

        # 節點統計
        print(f"\n{'節點使用統計':}")
        busiest = self.busiest_node()
        for i, count in enumerate(self.node_task_count):
            bar = "█" * count
            tag = "  ← 最忙節點 (LC 2402 答案)" if i == busiest else ""
            print(f"  Node-{i}: {bar} ({count} 個任務){tag}")

        # 執行日誌
        print("\n執行日誌:")
        for log in self._logs:
            print(log)

        print("=" * W)

    # ── 私有方法 ────────────────────────────

    def _release_finished_nodes(self, at_time: int) -> None:
        """將所有在 at_time 之前（含）結束的節點釋放回 availableNodes。"""
        while self.runningTasks and self.runningTasks[0][0] <= at_time:
            end_time, node_id = heapq.heappop(self.runningTasks)
            heapq.heappush(self.availableNodes, node_id)
            self._log(at_time, f"Node-{node_id} 釋放 (原結束 t={end_time})")

    def _log(self, t: int, msg: str) -> None:
        self._logs.append(f"  [t={t:>3}] {msg}")


# ─────────────────────────────────────────────
# Demo：模擬一次任務湧入
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("雲端任務調度器模擬 (Cloud Task Scheduler)")
    print("對應 LeetCode 2402 - Meeting Rooms III\n")

    # 3 個 Worker Node，7 個任務依序提交
    scheduler = CloudTaskScheduler(num_nodes=2)

    tasks = [
        #            task_id   submit_time  duration
        Task(task_id="job-A", submit_time=0,  duration=5),
        Task(task_id="job-B", submit_time=1,  duration=3),
        Task(task_id="job-C", submit_time=2,  duration=4),
        # ↓ t=3：三台節點全忙 → 延遲
        Task(task_id="job-D", submit_time=3,  duration=2),
        Task(task_id="job-E", submit_time=4,  duration=6),
        # ↓ t=10：所有節點空閒 → 立即執行
        Task(task_id="job-F", submit_time=10, duration=3),
        Task(task_id="job-G", submit_time=11, duration=1),
    ]

    for task in tasks:
        scheduler.submit(task)

    scheduler.report()
    print(f"\n最終答案：Node-{scheduler.busiest_node()} 處理了最多任務")
