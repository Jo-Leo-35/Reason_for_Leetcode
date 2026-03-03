class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == '0':
            return 0
            
        # Space-Optimized DP variables
        prev2 = 1 # corresponds to dp[i-2]
        prev1 = 1 # corresponds to dp[i-1]
        
        for i in range(1, len(s)):
            curr = 0
            
            # Single digit decode
            if s[i] != '0':
                curr += prev1
                
            # Double digit decode
            two_digit = int(s[i-1:i+1])
            if 10 <= two_digit <= 26:
                curr += prev2
                
            prev2 = prev1
            prev1 = curr
            
        return prev1
