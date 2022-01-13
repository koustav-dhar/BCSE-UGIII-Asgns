import string
import random
import re

n = 13 * (32 ** 2)

print(n)

print(type(string.printable))
res = ''.join(random.choices(re.sub(r'\s+', '',string.printable), k = n))
# print(res)

file = open("test.txt", "w")
file.write(res)
file.close()

# file = open("test.txt", "r")
# data = ''.join(format(ord(i), '08b') for i in file.read())
# file.close()

# index = 0
# np = 0
# # a forever loop until we interrupt it or an error occurs
# while index < len(data):
#     msg = data[index : index + 32]
#     index += 32
#     # adata = error.Error.injectError(msg)
#     if np == 106492:
#         print(msg)

#     np += 1