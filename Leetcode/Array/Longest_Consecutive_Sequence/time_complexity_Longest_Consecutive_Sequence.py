from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # TIME OPTIMAL: HashSet — O(N) time
        # Time: O(N) — each number is visited at most twice
        # Space: O(N) — store all numbers in a set
        # Key insight: only start counting from a sequence's beginning
        # (i.e., when num-1 is NOT in the set)
        num_set = set(nums)
        longest = 0

        for num in num_set:
            if num - 1 not in num_set:   # start of a sequence
                length = 1
                while num + length in num_set:
                    length += 1
                longest = max(longest, length)

        return longest
