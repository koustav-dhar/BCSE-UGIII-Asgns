# considering packet size of 32bits
# splitted in 4 rows containing 8bits each
class LRC:
    k = 4
    redbits = 8
    @classmethod
    def generateLRC(cls, data):
        table = []
        for i in range(cls.k):
            table.append([])
        n = len(data)
        m = n // cls.k
        for i in range(n):  # creating the 2d table for generating column wise LRC
            table[i // m].append(int(int(data[i])))
        lrc = ""
        for i in range(m): 
            v = 0
            for j in range(cls.k):  # finding XOR of every column
                v ^= table[j][i]
            lrc += str(v)
        data += lrc
        return data # returning the total data with LRC check bits added
    @classmethod
    def checkLRC(cls, data):
        n = len(data)
        m = n // (cls.k + 1)
        lrc = data[m * cls.k : ]    # getting the old LRC bits
        newdata = cls.generateLRC(data[ : cls.k * m])   # generating the new LRC
        newlrc = newdata[cls.k * m : ]  # extracting the LRC part
        if newlrc != lrc:   # checking if they match
            return False
        return True

'''
data = ""
for i in range(32):
    if i % 2 == 0:
        data += "1"
    else:
        data += "0"
print(data)
ndata = LRC.generateLRC(data)
print(ndata)
adata = ""
for i in range(32):
    if i == 25:
        adata += str((int(ndata[i]) ^ 1))
    else:
        adata += ndata[i]
for i in range(32, 40):
    adata += ndata[i]
print(adata)
print(LRC.checkLRC(adata))
'''