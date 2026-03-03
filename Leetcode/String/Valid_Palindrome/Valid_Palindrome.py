class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Two Pointers without extra memory allocation: O(N) time, O(1) space
        left, right = 0, len(s) - 1
        
        while left < right:
            # Skip non-alphanumeric characters
            while left < right and not self.is_alnum(s[left]):
                left += 1
            while left < right and not self.is_alnum(s[right]):
                right -= 1
                
            if s[left].lower() != s[right].lower():
                return False
                
            left += 1
            right -= 1
            
        return True
        
    def is_alnum(self, c: str) -> bool:
        return (
            ord('A') <= ord(c) <= ord('Z') or 
            ord('a') <= ord(c) <= ord('z') or 
            ord('0') <= ord(c) <= ord('9')
        )
