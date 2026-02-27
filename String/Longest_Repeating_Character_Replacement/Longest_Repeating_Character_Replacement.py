class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Sliding Window with max_frequency state tracking: O(N) time, O(1) space
        count = {}
        max_freq = 0
        left = 0
        max_len = 0
        
        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            # Update the max frequency we've seen in the window
            max_freq = max(max_freq, count[s[right]])
            
            # If the number of characters we need to replace exceeds K
            # Then the window is invalid, shrink it
            while (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1
                
            # The window is guaranteed to be valid here
            max_len = max(max_len, right - left + 1)
            
        return max_len
