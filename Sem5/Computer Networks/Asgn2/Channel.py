import socket
# import select
from threading import Thread, Lock
import ErrorInsertion
import random
import time

# Dictionary to store each connection information i.e. - ' address : [self connection, name, friend connection] '
client_map={}

# Dictionary to store current state of a client i.e. - ' address : state '
# 0 indicates either it's idle or sending data
# 1 indicates it's working as a receiver
# receiver_index={}

# Define the lock object
my_lock=Lock()

# Function to select if original packet or tainted packet or no packet will be sent
def process_packet(packet:str):
    # Randomly generate what would be done
    flag=random.randint(0,100)

    # If flag is 0-70, original packet will be sent
    # If flag is 71-80, taint the packet and send
    # If flag is 81-99, drop the packeth
    if(flag >= 0 and flag < 100):
        return packet
    elif(flag >= 70 and flag < 80):
        return ErrorInsertion.Error.injectError(packet)
    elif(flag >= 80 and flag < 90):
        time.sleep(0.5)
        return packet
    else:
        return ''

class ConnectionThread (Thread) :
    def __init__ (self, clientSocket, clientAddress) -> None :
        Thread.__init__ (self)

        # save the properties of the incoming client communication
        self.csocket = clientSocket
        self.caddr = clientAddress
        print ('\nGot new connection from', clientAddress)

    def setConnection (self):
        availableClients = []
        availableClientNames = []
        for address in client_map:
            if address != self.caddr and client_map[address][2] == None:
                availableClients.append(address)
                availableClientNames.append(client_map[address][1])

        if (len(availableClients) == 0):
            self.csocket.send(bytes("No client is available",'utf-8'))
        else:
            self.csocket.send(bytes('$'.join(availableClientNames),'utf-8'))
            choice = int(self.csocket.recv(1024).decode())

            my_lock.acquire()
            raddr = availableClients[choice]
            
            if (client_map[raddr][2] == None):
                rsocket = client_map[raddr][0]
                client_map[raddr][2] = self.caddr
                client_map[raddr][3] = 384
                client_map[self.caddr][2] = raddr
                client_map[self.caddr][3] = 576
                self.csocket.send (bytes(str(raddr[1]), 'utf-8'))
                rsocket.send (bytes(str(self.caddr[1]),'utf-8'))
                print(self.caddr,"is sending data to",raddr)
            else:
                print("receiver is busy")
            my_lock.release()

    def revokeConnection (self) -> None:
        my_lock.acquire()
        raddr = client_map[self.caddr][2]
        
        client_map[raddr][2] = None
        client_map[self.caddr][2] = None
        client_map[raddr][3] = client_map[self.caddr][3] = 1024
        self.csocket.send(str.encode("Sending completed"))
        
        # Print end of data transfer
        print(self.caddr,' ended transferring data to ',raddr)
        my_lock.release()

    # override the run method to specify the code that the thread would run on
    def run (self) -> None:
        # send a message to indicate that the server is ready to respond
        self.csocket.send(bytes("You are now connected to server.\nWrite your name: ",'utf-8'))

        # receive client name from client and send port-number to it
        name=self.csocket.recv(1024).decode()
        
        self.csocket.send(bytes(str(self.caddr[1]), 'UTF-8'))

        # update client_map and receiver_index list with the new client
        client_map[self.caddr]=[self.csocket,name,None,1024]
        data = "open"

        while data!="close":
            inputBuffer = client_map[self.caddr][3]
            data = self.csocket.recv(inputBuffer).decode()

            if (client_map[self.caddr][2] == None):
                if data == "request for sending":
                    self.setConnection ()
                else:
                    pass
            
            else:
                rsocket = client_map[client_map[self.caddr][2]][0]
                # print (data)
                if data == "start":
                    rsocket.send(str.encode(data))
                elif data == "end":
                    rsocket.send(str.encode(data))
                    self.revokeConnection()
                else:
                    newData = process_packet(data)
                    if(newData!=''):
                        rsocket.send(str.encode(newData))

        # close the connection
        self.csocket.close()

        # message to show that the client has been disconnected
        print ("Client at", self.caddr, "disconnected")

        # remove map entries
        client_map.pop(self.caddr) 


# Function to specify server functionality
def server():
    # define server IP address
    SERVER_IP='127.0.0.1'
    # Define server port address
    SERVER_PORT=1232
    # maximum number of clients waiting to connect to server
    MAXIMUM_WAITING = 5

    # Initialize server
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
        # notify server started
        print("Server started")
        
        # set socket options, SO_REUSEADDR specifies that the local 
        # address to which the socket binds can be reused
        server.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind server to the address
        server.bind((SERVER_IP,SERVER_PORT))

        print ("Server socket binded to %s" %(SERVER_PORT))

        # put the socket into listening mode, Its backlog parameter 
        # specifies the number of unaccepted connections that the 
        # system will allow before refusing new connections.
        server.listen (MAXIMUM_WAITING)	
        print ("Server is waiting for client request...")	

        while True:
            # Establish connection with client
            # a new socket is returned for connecting to the client
            # which is different from the listening socket
            conn,addr=server.accept()

            newThread = ConnectionThread (conn, addr)
            newThread.start()


# Main function
if __name__=='__main__':
    server()













# # Function to handle channel actions for data passing
# def channel(sender,receiver):
#     # Initialize lists of input and output event generators
#     inputs=[sender,receiver]
#     outputs=[]
#     data='start'

#     # Tell sender to start transmitting
#     sender.send(str.encode('start'))

#     # loop until all data is sent from sender to receiver
#     while(data!="end"):
#         # Wait for an event (Data come from sender/Ack come from receiver)
#         readable, writable, exceptionals=select.select(inputs,outputs,inputs)

#         # Handle the incoming data
#         for s in readable:
#             # If data was sent by sender, deliver it to receiver (vice-versa)
#             if s is sender:
#                 # Receive, decode and process the data packet
#                 data=s.recv(576)
#                 data=data.decode()
#                 new_data=''
#                 if(data!="end"):
#                     new_data=process_packet(data)
#                 if(data=="end"):
#                     receiver.send(str.encode(data))
#                 elif(new_data!=''):
#                     receiver.send(str.encode(new_data))
#             if s is receiver:
#                 data=s.recv(384)
#                 data=data.decode()
#                 new_data=''
#                 new_data=process_packet(data)
#                 if(new_data!=''):
#                     sender.send(str.encode(new_data))

#         # If any error occurs in sender/receiver connection, close that connection
#         for s in exceptionals:
#             inputs.remove(s)
#             s.close()


# # Function for controlling data passing using thread lock
# def send_handler(client,address):
#     # Check if any other client is connected or not
#     if(len(client_map.keys())==1):
#         client.send(str.encode("No other client is available"))
#         return
    
#     # Try to get the lock for data transfer
#     my_lock.acquire()
    
#     # Notify sender that lock acquired
#     client.send(str.encode("Sending permission granted-----"))
#     # Just a simple sender reply
#     inp=client.recv(1024)
    
#     # Get all available client addresses
#     dummy=list(client_map.keys())
    
#     # Remove it's own address from the list
#     dummy.remove(address)
    
#     # Convert all addresses into '$' separated string
#     total=''
#     for index in range(0,len(dummy)):
#         total+=(client_map[dummy[index]][1]+'$')
    
#     # Send the available clients list to sender for choosing it's client
#     client.send(str.encode(str(total)))
    
#     # Get sender choice
#     inp=client.recv(1024)
#     inp=int(inp.decode())
    
#     # Get the receiver connection from address
#     receiver=client_map[dummy[inp]][0]
#     recv_addr=dummy[inp]

#     # Send receiver address to sender
#     client.send(str.encode(str(recv_addr[1])))

#     # Notify receiver about this and change it's state to receiving
#     receiver.send(str.encode(str(address[1])))
#     receiver_index[dummy[inp]]=1

#     # Wait for receiver 'ok' reply
#     inp=receiver.recv(1024)

#     # Print sender and receiver info
#     print(address,' is sending data to ',recv_addr)

#     # Complete data transfer using channel
#     channel(client,receiver)

#     # Print end of data transfer
#     print(address,' ended transferring data to ',recv_addr)
    
#     # Notify sender about completion
#     client.send(str.encode("Sending permission revoked-----"))
    
#     # Change receiver state to idle/sending
#     receiver_index[recv_addr]=0

#     # Release lock
#     my_lock.release()