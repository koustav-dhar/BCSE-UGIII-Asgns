import socket
import time
import PacketManager
import Analysis
import random

# Define default data bytes in a packet
defaultDataPacketSize=46

# Define propagation time
propagation_time = 0.1

# Define file name where analyses will be stored
analysis_file_name='SWARQ.txt'

# Define Sender class for data sending management
class Sender:
    # Function for initializing sender object
    def __init__(self, sender_no:int, fileName:str, method:int, totalSender:int):
        # Get the client/sender connection and other informations (name, receive name, data file name)
        self.connection         = 0 
        self.fileName           = fileName
        self.senderNo           = sender_no
        self.senderAddress      = 0
        self.receiverAddress    = 0
        self.method             = method
        self.totalSender        = totalSender
        self.report             = Analysis.Report(0, 0, 0)

        # Define transmission management variables (sequence no, total packet sent and collision count)
        self.seqNo              = 0
        self.collisionCount     = 0
        self.pktCount           = 0


    # Function to send data using one persistent method
    def sendDataOnePersistent(self):
        # Notify about the start of sending
        print("\n",self.senderNo," starts sending data\n")
        
        # open data file for reading
        file = open(self.fileName,'r')

        # Read data of size of frame from file
        data_frame = file.read(defaultDataPacketSize)
        
        # Initialize sequence number and other variables
        self.seqNo = 0
        self.pktCount = 0
        self.collisionCount = 0
        previousPkt = False

        # Loop until whole data is sent
        while data_frame:
            time.sleep(0.005)
            # Get the current status of the channel (busy/idle)
            self.connection.send(str.encode('status'))
            reply = self.connection.recv(1024)
            reply = reply.decode()

            # If channel is busy, loop until it becomes idle
            if reply == 'Busy':
                continue

            # If channel is idle, send data
            else:
                if not previousPkt:
                    # Build packet using data, type and sequence number
                    packet = PacketManager.Packet(self.senderAddress, self.receiverAddress, 0, self.seqNo, data_frame)

                    # Increment sequence number and other parameters accordingly
                    self.seqNo += 1
                    previousPkt = True

                # Notify the channel about data sending 
                self.connection.send(str.encode('sending'))
                self.connection.recv(1024)

                # Send the packet and increase packet count
                self.connection.send(str.encode(packet.toBinaryString(46)))
                self.pktCount += 1

                # Print sent status
                print("Sender ",self.senderNo," sent packet no ",self.seqNo," to channel.")
            
                # Wait for propagation time
                time.sleep(propagation_time)

                # Get transmission status (send successfully/collision)
                transmission_status = self.connection.recv(1024).decode()

                # If collision ocuured, increase collision count
                if transmission_status == 'collision':
                    self.collisionCount += 1
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," collided in channel.")

                elif transmission_status == 'Sent successfully':
                    previousPkt = False
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," delivered successfully.")

                    # Read next data frame
                    data_frame = file.read(defaultDataPacketSize)

                # If all data has been read, break
                if len(data_frame) == 0: break

        # Close the data file
        file.close()

        # Send 'end transmission' message to channel
        self.connection.send(str.encode('end'))
        

    # Function to send data using non persistent method
    def sendDataNonPersistent(self):
        # Notify about the start of sending
        print("\n",self.senderNo," starts sending data using non-persistent\n")
        
        # open data file for reading
        file = open(self.fileName,'r')

        # Read data of size of frame from file
        data_frame = file.read(defaultDataPacketSize)
        
        # Initialize sequence number and other variables
        self.seqNo = 0
        self.pktCount = 0
        self.collisionCount = 0
        previousPkt = False

        # Loop until whole data is sent
        while data_frame:
            time.sleep(0.005)
            # Get the current status of the channel (busy/idle)
            self.connection.send(str.encode('status'))
            reply = self.connection.recv(1024)
            reply = reply.decode()

            # If channel is busy, sleep for random time then check again
            if reply == 'Busy':
                start = 1
                end = (self.totalSender)
                randomTime = random.randint(start,end)
                time.sleep(randomTime*propagation_time)
                continue

            # If channel is idle, send data
            else:
                if not previousPkt:
                    # Build packet using data, type and sequence number
                    packet = PacketManager.Packet(self.senderAddress, self.receiverAddress, 0, self.seqNo, data_frame)

                    # Increment sequence number and other parameters accordingly
                    self.seqNo += 1
                    previousPkt = True

                # Notify the channel about data sending 
                self.connection.send(str.encode('sending'))
                self.connection.recv(1024)

                # Send the packet and increase packet count
                self.connection.send(str.encode(packet.toBinaryString(46)))
                self.pktCount += 1

                # Print sent status
                print("Sender ",self.senderNo," sent packet no ",self.seqNo," to channel.")
            
                # Wait for propagation time
                time.sleep(propagation_time)

                # Get transmission status (send successfully/collision)
                transmission_status = self.connection.recv(1024).decode()

                # If collision ocuured, increase collision count
                if transmission_status == 'collision':
                    self.collisionCount += 1
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," collided in channel.")

                elif transmission_status == 'Sent successfully':
                    previousPkt = False
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," delivered successfully.")

                    # Read next data frame
                    data_frame = file.read(defaultDataPacketSize)

                # If all data has been read, break
                if len(data_frame) == 0: break

        # Close the data file
        file.close()

        # Send 'end transmission' message to channel
        self.connection.send(str.encode('end'))


    # Function to send data using non persistent method
    def sendData_P_Persistent(self):
        # Notify about the start of sending
        print("\n",self.senderNo," starts sending data\n")
        
        # open data file for reading
        file = open(self.fileName,'r')

        # Read data of size of frame from file
        data_frame = file.read(defaultDataPacketSize)
        
        # Initialize sequence number and other variables
        self.seqNo = 0
        self.pktCount = 0
        self.collisionCount = 0

        previousPkt = False
        threshold = (1/self.totalSender)

        # Loop until whole data is sent
        while data_frame:
            time.sleep(0.005)
            # Get the current status of the channel (busy/idle)
            self.connection.send(str.encode('status'))
            reply = self.connection.recv(1024)
            reply = reply.decode()

            # If channel is idle, send data
            if reply == 'Busy':
                # Wait for next time slot
                time.sleep(propagation_time)

            else:
                if not previousPkt:
                    # Build packet using data, type and sequence number
                    packet = PacketManager.Packet(self.senderAddress, self.receiverAddress, 0, self.seqNo, data_frame)

                    # Increment sequence number and other parameters accordingly
                    self.seqNo += 1
                    previousPkt = True

                p = random.random()
                while p >= threshold:
                    time.sleep(propagation_time)
                    #time.sleep(0.1)

                    # Get the current status of the channel (busy/idle)
                    self.connection.send(str.encode('status'))
                    reply = self.connection.recv(1024)
                    reply = reply.decode()

                    if reply == 'Busy':
                        break

                    p = random.random()

                if reply == 'Busy':
                    continue

                # Notify the channel about data sending 
                self.connection.send(str.encode('sending'))
                self.connection.recv(1024)

                
                # Send the packet and increase packet count
                self.connection.send(str.encode(packet.toBinaryString(46)))
                self.pktCount += 1

                # Print sent status
                print("Sender ",self.senderNo," sent packet no ",self.seqNo," to channel.")
            
                # Wait for propagation time
                time.sleep(propagation_time)

                # Get transmission status (send successfully/collision)
                transmission_status = self.connection.recv(1024).decode()

                # If collision ocuured, increase collision count
                if transmission_status == 'collision':
                    self.collisionCount += 1
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," collided in channel.")

                elif transmission_status == 'Sent successfully':
                    previousPkt = False
                    print("Sender ",self.senderNo,", packet no ",self.seqNo," delivered successfully.")

                    # Read next data frame
                    data_frame = file.read(defaultDataPacketSize)

                # If all data has been read, break
                if len(data_frame) == 0: break

        # Close the data file
        file.close()

        # Send 'end transmission' message to channel
        self.connection.send(str.encode('end'))


    # Function to control the whole transmission
    def startTransmission(self):
        # Initialize the socket
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Connect with the channel
        channel_ip = '127.0.0.2'
        channel_port = 1233
        channel_address = (channel_ip,channel_port)
        self.connection.connect(channel_address)

        # Receive sender address from channel
        self.senderAddress = int(self.connection.recv(1024).decode())

        # Notify channel that it's a sender
        self.connection.send(str.encode('sender'))

        # Get corresponding receiver address from channel
        self.receiverAddress = int(self.connection.recv(1024).decode())

        # record the strating time
        startTime=time.time()

        # Call the corresponding method
        if self.method == 0:
            self.sendDataOnePersistent()
        elif self.method == 1:
            self.sendDataNonPersistent()
        else:
            self.sendData_P_Persistent()


        # Close the connection
        self.connection.close()

        # Calculate total time taken and write analysis into file
        endTime=time.time()
        if(self.method == 1):
            endTime += (5*(self.totalSender-1))
        totalTime=(endTime-startTime)
        self.report = Analysis.Report(self.pktCount, self.collisionCount, totalTime)