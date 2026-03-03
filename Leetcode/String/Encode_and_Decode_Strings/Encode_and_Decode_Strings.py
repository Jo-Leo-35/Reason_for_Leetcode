class Codec:
    def encode(self, strs: [str]) -> str:
        """Encodes a list of strings to a single string."""
        # TLV (Type-Length-Value) style encoding: length + '#' + string
        res = ""
        for s in strs:
            res += str(len(s)) + "#" + s
        return res

    def decode(self, s: str) -> [str]:
        """Decodes a single string to a list of strings."""
        res, i = [], 0
        
        while i < len(s):
            # Find the next delimiter
            j = i
            while s[j] != "#":
                j += 1
                
            # Extract length and read that many characters
            length = int(s[i:j])
            res.append(s[j + 1 : j + 1 + length])
            
            # Move the pointer past the extracted string
            i = j + 1 + length
            
        return res
