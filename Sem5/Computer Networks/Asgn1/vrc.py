class VRC:
    redbits = 1
    @classmethod
    def getParity(cls, data):
        parity = 0
        for c in data:
            parity ^= int(c)  # finding the parity by XORing the set bits
        return (data + str(parity))
    @classmethod
    def parityCheck(cls, data):
        ndata = cls.getParity(data[0:len(data) - 1])
        if ndata == data:  # odd parity VRC
            return True
        return False  

