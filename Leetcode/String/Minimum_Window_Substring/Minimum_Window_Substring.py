class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(s) < len(t):
            return ""
            
        from collections import Counter
        target_counts = Counter(t)
        required_unique_chars = len(target_counts)
        
        # Sliding Window tracking state variables: O(N) time
        left = 0
        window_counts = {}
        formed = 0
        
        # (length, starting idx, ending idx)
        ans = (float('inf'), None, None)
        
        for right in range(len(s)):
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1
            
            if char in target_counts and window_counts[char] == target_counts[char]:
                formed += 1
                
            # Try and contract the window till it ceases to be 'desirable'
            while left <= right and formed == required_unique_chars:
                char_left = s[left]
                
                # Save the smallest window
                if right - left + 1 < ans[0]:
                    ans = (right - left + 1, left, right)
                    
                window_counts[char_left] -= 1
                if char_left in target_counts and window_counts[char_left] < target_counts[char_left]:
                    formed -= 1
                    
                left += 1
                
        return "" if ans[0] == float('inf') else s[ans[1]:ans[2]+1]
