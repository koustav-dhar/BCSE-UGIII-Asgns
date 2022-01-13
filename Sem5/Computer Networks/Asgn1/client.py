# import lrc
# import vrc
# import crc
# import checksum
# # import socket module
# import socket			

# SERVER = "127.0.0.1"        # host interface of the server
# PORT = 12345                # port on which the server listens

# # create a new socket object
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
#     client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
#     # connect to server
#     client.connect((SERVER, PORT))

#     data = ""
#     for i in range (256):
#         if i % 2 == 0 or i % 5 == 0:
#             data += "1"
#         else:
#             data += "0"

#     index = 0
#     # a forever loop until we interrupt it or an error occurs
#     while index < len(data):
#         # recieve data from server
#         in_data =  client.recv(1024)
#         print("From Server :" ,in_data.decode())

#         msg = data[index : index + 32]
#         index += 32
#         ndata = lrc.LRC.generateLRC(msg)
#         print(ndata)
#         adata = ""
#         for i in range(32):
#             if i == 25:
#                 adata += str((int(ndata[i]) ^ 1))
#             else:
#                 adata += ndata[i]
#         for i in range(32, 40):
#             adata += ndata[i]
#         print(adata)

#         # send it to server
#         client.sendall(bytes(adata,'UTF-8'))

#         # break

import socket 
# from error_modules import *
# from error_injection import *

HOST = "127.0.0.1"  #host interface of sever
PORT = 12345                                          #port on which client listens
ADDR = (HOST,PORT)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client :
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.connect((HOST, PORT))


    file = open("test.txt","r")
    data = ''.join(format(ord(i),'08b') for i in file.read())
    file.close()

    methodname = ["VRC", "LRC", "CheckSum", "CRC"]
    index = 0

    # a forever loop until we interrupt it or an error occurs
    while index<len(data):
        packet = data[index : index + 16]
        index += 16
    
        for i in range(4):
            #recieve data from server
            serv_data = client.recv(1024) 
            print("From server :" ,serv_data.decode())
            print(">> Method: "+methodname[i])
        
            new_data =packet
            # if(i==0):
            #     new_data = vrc_generator(packet)
            # elif(i==1):
            #     new_data = lrc_generator(packet)
            # elif(i==2):
            #     new_data = checksum_generator(packet)
            # else:
            #     new_data = crc_generator(packet)
            
            print("Untained -> " + new_data)
        
            err_data = new_data
            # err_data = inject_error(new_data)
            # print("Tainted  -> " + err_data)
        
            client.sendall(bytes(err_data,'UTF-8'))
        
    serv_data = client.recv(1024)
    print("From server :" ,serv_data.decode())