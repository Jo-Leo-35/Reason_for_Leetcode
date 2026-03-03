class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Sliding Window with Dictionary (HashMap): O(N) time, O(min(M, N)) space
        char_index_map = {}
        left = 0
        max_len = 0
        
        for right, char in enumerate(s):
            # If we've seen character and its index is inside our current sliding window
            if char in char_index_map and char_index_map[char] >= left:
                # Instantly shrink the window by moving left to right after the duplicate
                left = char_index_map[char] + 1
                
            char_index_map[char] = right
            max_len = max(max_len, right - left + 1)
            
        return max_len
