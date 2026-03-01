import heapq


class Solution:

    # 直覺解：暴力陣列掃描 (Brute Force) - Lean Hire
    # 時間複雜度：O(M log M + M * N)，空間複雜度：O(N)
    def mostBooked_brute(self, n: int, meetings: list[list[int]]) -> int:

        meetings.sort()

        roomEndTimes = [0] * n  # roomEndTimes[i] = 會議室 i 的最早可用時間
        count = [0] * n         # count[i] = 會議室 i 舉辦的會議數

        for start, end in meetings:
            duration = end - start
            chosen = -1

            # 優先尋找編號最小的空閒房間
            for i in range(n):
                if roomEndTimes[i] <= start:
                    chosen = i
                    break

            if chosen == -1:
                # 無空房間：延遲會議，分配給最早結束的房間
                min_end = float('inf')
                for i in range(n):
                    if roomEndTimes[i] < min_end:
                        min_end = roomEndTimes[i]
                        chosen = i
                roomEndTimes[chosen] = min_end + duration  # 延遲後的結束時間
            else:
                roomEndTimes[chosen] = end

            count[chosen] += 1

        return count.index(max(count))

    # 最佳解：雙優先佇列 (Two Heaps) - Strong Hire
    # 時間複雜度：O(M log M + M log N)，空間複雜度：O(N)
    def mostBooked(self, n: int, meetings: list[list[int]]) -> int:

        meetings.sort()

        availableRooms = list(range(n))  # Min-Heap：空閒房間（by 編號）
        heapq.heapify(availableRooms)

        ongoingMeetings = []             # Min-Heap：[endTime, roomNumber]
        count = [0] * n

        for start, end in meetings:
            duration = end - start

            # 將所有在 start 之前已結束的會議室釋放回 availableRooms
            while ongoingMeetings and ongoingMeetings[0][0] <= start:
                endTime, room = heapq.heappop(ongoingMeetings)
                heapq.heappush(availableRooms, room)

            if availableRooms:
                # 有空房間：分配編號最小的房間
                room = heapq.heappop(availableRooms)
                heapq.heappush(ongoingMeetings, [end, room])
            else:
                # 無空房間：延遲會議，等最早結束的房間
                endTime, room = heapq.heappop(ongoingMeetings)
                newEnd = endTime + duration  # 注意：延遲後結束時間 = 舊結束時間 + 持續時長
                heapq.heappush(ongoingMeetings, [newEnd, room])

            count[room] += 1

        return count.index(max(count))
