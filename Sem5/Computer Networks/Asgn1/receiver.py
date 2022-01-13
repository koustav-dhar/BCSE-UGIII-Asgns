import vrc
import lrc
import checksum
import crc
import error

import socket

crcpoly = "111010101"
# crcpoly = "10101"

# specify a host network interface, here we use loopback interface whose IPv4 address is 127.0.0.1
# If a hostname is used in the host portion of IPv4/v6 socket address, the program may show a
# non-deterministic behavior, as Python uses the first address returned from the DNS resolution
HOST = '127.0.0.1' 

# reserve a port on local machine for listening to incoming client requests
PORT = 12345

# create a socket object which supports context manager types
# this is used to listen to incoming client connection requests
# AF_INET refers to the address family ipv4. 
# The SOCK_STREAM means connection oriented TCP protocol.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:			

    print("Server started")

    # set socket options, SO_REUSEADDR specifies that the local 
    # address to which the socket binds can be reused
    server.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Next bind to the port
    server.bind((HOST, PORT))		
    print ("Server socket binded to %s" %(PORT))

    # put the socket into listening mode, Its backlog parameter 
    # specifies the number of unaccepted connections that the 
    # system will allow before refusing new connections.
    server.listen(5)	
    print ("Server is waiting for client request...")	

    csocket, caddr = server.accept()
    print('Got new connection from', caddr)

    csocket.send(bytes("You are now connected to server.\n",'utf-8'))

    framesize = [32 + vrc.VRC.redbits, 32 + lrc.LRC.redbits, 32 + checksum.CheckSum.redbits, 32 + len(crcpoly) - 1]
    checkmethods = [vrc.VRC.parityCheck, lrc.LRC.checkLRC, checksum.CheckSum.checkSum, crc.CRC.checkCRC]
    methodname = ["VRC", "LRC", "CheckSum", "CRC"]
    detected = [0, 0, 0, 0]
    totalcnt = 0
    csnotcrc = ""
    ind = 0

    while True:
        stop = True
        checkschemes = [True, True, True, True]
        for i in range(4):
            try:
                msg = csocket.recv(1024)         # a blocking call to receive message from client in bytes form
            except:
                print('Cannot receive data')           # in case the client is abrubtly terminated
            
            if not msg:            # if the message contains no data, it must be due to some error
                stop = False
                break
            print(">> METHOD : " + methodname[i])
            msg = msg.decode()         # decode the message to string format to interpret
            print('From client at', caddr[1], 'received: ', msg)

            ok = True
            if i == 3:
                ok = checkmethods[i](msg, crcpoly)
            else:
                ok = checkmethods[i](msg)
            checkschemes[i] = ok
            ack = ""
            if ok == True:
                ack = "NO ERROR DETECTED"
            else:
                ack = "ERROR DETECTED"
                detected[i] += 1
            print(ack)
            # echo the message sent by client, back to client
            csocket.sendall(bytes(ack, 'UTF-8'))
        if checkschemes[0] == False and checkschemes[3] == True:
            csnotcrc = msg
            ind = totalcnt
        if stop == False:
            break
        totalcnt += 1
    # message to show that the client has disconnected
    print ("Client at ", caddr , " disconnected...")
    
    # close the socket used for connecting to the client at the specific address
    csocket.close()
    
    # Analysis
    print("Total no. of frames:" + str(totalcnt))
    for i in range(4):
        print(methodname[i] + " : " + str(detected[i]) + " Accuracy : " + str(100.0 * detected[i] / totalcnt) + "%")

    # print("VRC but not CRC: Index -> " + str(ind) + " Codeword(Tainted) -> " + csnotcrc)
