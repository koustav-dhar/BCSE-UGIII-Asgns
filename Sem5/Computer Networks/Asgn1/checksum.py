# considering packet size of 32bits
# splitted in 4 rows containing 8bits each
class CheckSum:
    k = 4
    redbits = 8
    @classmethod
    def generateCheckSum(cls, data):
        table = []
        for i in range(cls.k):
            table.append([])
        n = len(data)
        m = n // cls.k
        for i in range(n):  # creating a 2d table for column wise checksum
            table[i // m].append(int(int(data[i])))
        checksum = [0 for i in range(m)]
        carry = 0
        for i in range(cls.k):
            for j in range(m - 1, -1, -1):
                checksum[j] += carry + table[i][j]
                carry = checksum[j] // 2
                checksum[j] %= 2
        while carry != 0:
            for i in range(m - 1, -1, -1):
                checksum[i] += carry
                carry = checksum[i] // 2
                checksum[i] %= 2
        for i in range(m):
            checksum[i] ^= 1
        cs = ""
        for i in range(m):
            cs += str(checksum[i])
        data += cs
        return data # returning the total data with LRC check bits added
    @classmethod
    def checkSum(cls, data):
        table = []
        for i in range(cls.k + 1):
            table.append([])
        n = len(data)
        m = n // (cls.k + 1)
        for i in range(n):  # creating a 2d table for column wise checksum
            table[i // m].append(int(int(data[i])))
        checksum = [0 for i in range(m)]
        carry = 0
        for i in range(cls.k + 1):
            for j in range(m - 1, -1, -1):
                checksum[j] += carry + table[i][j]
                carry = checksum[j] // 2
                checksum[j] %= 2
        while carry != 0:
            for i in range(m - 1, -1, -1):
                checksum[i] += carry
                carry = checksum[i] // 2
                checksum[i] %= 2
        for i in range(m):
            checksum[i] ^= 1
        for i in range(m):
            if checksum[i] == 1:
                return False
        return True

'''
data = "10011001111000100010010010000100"
ndata = CheckSum.generateCheckSum(data)
print(data)
print(ndata)
adata = ""
for i in range(len(ndata)):
    if i == 7 or i == 15:
        adata += str((int(ndata[i]) ^ 1))
    else:
        adata += ndata[i]
print(adata)
print(CheckSum.checkSum(adata))
'''