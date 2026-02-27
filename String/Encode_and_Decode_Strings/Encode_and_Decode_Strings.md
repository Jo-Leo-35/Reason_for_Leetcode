### 1. 核心題意與挑戰

設計一種演算法來編碼和解碼字串陣列。
編碼器 (Encode) 必須將一個字串陣列轉換為單一的字串。
解碼器 (Decode) 必須能夠將該單一字串完美還原回原本的陣列。

* **隱藏挑戰**：
  * 面試常見系統設計題。因為輸入陣列中的字串可能包含任何 ASCII 字元（包括各種詭異的標點符號如 `#`, `/`, `,` 甚至「空字串」），所以你不能隨便挑一個符號例如 `","` 作為分隔符。如果字串本身就含有 `","`，解碼就會出錯。

---

### 2. 解法對比與完整程式碼

#### A. 長度前綴編碼 (Length-Prefix Encoding / TLV) —— **沒有死角的標準協定解**

**思路**：
參考網路傳輸封包的標準設計 (Type-Length-Value, TLV)。
我們在每個字串前面，標示它的 **長度**，並且加上一個特殊的 **界定符 (Delimiter, 例如 `#`)** 作為分隔。
編碼格式：`[長度] + "#" + [字串本身]`
例如：`["lint", "code", "love", "you"]` 會被編碼為 `"4#lint4#code4#love3#you"`。

解碼時：
1. 先找到第一個 `#`，它前面的數字就是下一個字串的長度 `L`。
2. 從 `#` 後面強制讀取精準的 `L` 個字元作為字串。
3. 讀完後，指標跳到 `L` 之後，重複上述動作。
* 這樣就算字串本身包含一大堆 `#` 或數字，也不會被影響，因為我們是**嚴格按照指定的長度 (Length) 去讀取的**！

* **優點**：不依賴任何特殊逃脫字元，時間複雜度為 $O(N)$（$N$ 為所有字串的總長度）。

```python
class Codec:
    def encode(self, strs: [str]) -> str:
        """Encodes a list of strings to a single string."""
        encoded_str = ""
        for s in strs:
            # 格式：長度 + '#' + 字串本身
            encoded_str += str(len(s)) + "#" + s
        return encoded_str

    def decode(self, s: str) -> [str]:
        """Decodes a single string to a list of strings."""
        decoded_strs = []
        i = 0
        
        while i < len(s):
            # 尋找下一個 '#' 的位置
            j = i
            while s[j] != '#':
                j += 1
                
            # 擷取長度資訊
            length = int(s[i:j])
            
            # 從 '#' 之後讀取 length 個字元
            start = j + 1
            end = start + length
            decoded_strs.append(s[start:end])
            
            # 更新指針，準備讀取下一個
            i = end
            
        return decoded_strs
```

#### B. JSON序列化 (JSON Serialization) —— **投機的逃課解法**

**思路**：
直接使用內建函式庫（如 Python 的 `json.dumps` 和 `json.loads`）。
* **缺點**：面試中如果這樣寫通常會被白眼，因為面試官就是想考你如何自己設計 Serialization 協定。

---

### 3. 實務應用場景

這完全就是實體工業界的網路封包設計！

#### 1. 網路傳輸封包 (TCP Packet Framing)
* **應用**：TCP 是一個位元組流協定 (Byte Stream)，沒有訊息邊界的概念。如果送了兩個 Json，接收端可能會把它們黏在一起 (`{"a":1}{"b":2}`)。為了解決這個典型的 **TCP 黏包問題 (TCP Sticky Packet)**，在應用層協定（如 HTTP 的 `Content-Length` 或是 grpc/protobuf 的 Header）都一定會先傳送一段標注「接下來的 Payload 有多長」的整數。

#### 2. 檔案系統區塊儲存 (File Systems Chunking)
* **應用**：在二進位檔案格式 (例如 PNG、MP4) 內部，都是以一個 Chunk Header (裡面寫了 Chunk Size) 再接上 Chunk Data 所構成。解析器只需要不斷將指標往前跳躍 `Size` 的距離即可高速掃瞄整個檔案。

---

### 4. 總結筆記

| 比較維度 | 長度前綴 (Length-Prefix / TLV 思想) |
| --- | --- |
| **時間複雜度** | 編碼 $O(N)$，解碼 $O(N)$ |
| **空間複雜度** | $O(N)$ 用於儲存字串 |
| **防禦力** | **極高**。不怕空字串，不怕字串內容含有特殊符號 |
| **系統設計啟發** | `ChunkHeader(長度) + Body` 是解決序列化的萬用模板 |
