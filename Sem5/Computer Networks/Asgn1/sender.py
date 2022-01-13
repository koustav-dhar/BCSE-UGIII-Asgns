import vrc
import lrc
import checksum
import crc
import error

# import socket module
import socket			

crcpoly = "111010101"
# crcpoly = "10101"

SERVER = "127.0.0.1"        # host interface of the server
PORT = 12345                # port on which the server listens

# create a new socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # connect to server
    client.connect((SERVER, PORT))

    # data = "01001100010100000100100101100111"
    # for i in range (256):
    #     if i % 2 == 0 or i % 5 == 0:
    #         data += "1"
    #     else:
    #         data += "0"

    file = open("test.txt", "r")
    data = ''.join(format(ord(i), '08b') for i in file.read())
    file.close()

    scheme = [vrc.VRC.getParity, lrc.LRC.generateLRC, checksum.CheckSum.generateCheckSum, crc.CRC.generateCRC]
    methodname = ["VRC", "LRC", "CheckSum", "CRC"]

    index = 0
    # a forever loop until we interrupt it or an error occurs
    while index < len(data):
        msg = data[index : index + 32]
        index += 32
        # adata = error.Error.injectError(msg)
        for i in range(4):
            # recieve data from server
            in_data =  client.recv(1024)
            print("From Server :" ,in_data.decode())
            print(">> METHOD : " + methodname[i])
            ndata = ""
            if i == 3:
                ndata = scheme[i](msg, crcpoly)
            else:
                ndata = scheme[i](msg)
            print(ndata + " <- Untainted")
            edata = error.Error.injectError(ndata)
            # edata = "01001100010100000100100101100101" + ndata[32:]
            # edata = adata + ndata[32 : ]
            print(edata + " <- Tainted")

            # send it to server
            client.sendall(bytes(edata,'UTF-8'))
    in_data =  client.recv(1024)
    print("From Server :" ,in_data.decode())
        # break

