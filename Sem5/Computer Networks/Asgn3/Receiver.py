import socket
import PacketManager

# Define Receiver class to handle data receiving 
class Receiver:
    # Function to initialize obect
    def __init__(self, receiverNo:int, file:str):
        # Get the client/receiver connection and other informations (name, data file name)
        self.connection         = 0
        self.file_name          = file
        self.receiverAddress    = 0
        self.receiverNo         = receiverNo
  

    # Function for receiving data
    def receive(self):

        # Wait for data and receive
        data=self.connection.recv(576).decode()

        total_data=''

        # If data-receiving hasn't ended yet 
        while data!='end':
            # Build packet from binary data string
            packet = PacketManager.Packet.build(data)
            
            # If packet has no error
            if not packet.hasError():
                # print("NO ERROR FOUND")
                data = packet.getData()
                # print(data)
                total_data += data
                print("Receiver ",self.receiverNo," received packet successfully")

            # Discard erroneous packet
            else:
                print("Packet has error")

            # Wait and receive next packet
            data=self.connection.recv(576).decode()

        if total_data != '':
            # print(total_data)
            file = open(self.file_name,'a')
            file.write(total_data)
            file.close()


    # Function to connect receiver with channel and start receiving
    def startReceive(self):
        # Print starting of receiver
        print("Receiver ",self.receiverNo," started")

        # Initialize the socket
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Connect with the channel
        channel_ip = '127.0.0.2'
        channel_port = 1233
        channel_address = (channel_ip,channel_port)
        self.connection.connect(channel_address)

        # Receive receiver address from channel
        self.senderAddress = int(self.connection.recv(1024).decode())

        # Notify channel that it's a sender
        self.connection.send(str.encode('receiver'))

        # Start receiving
        self.receive()

        # Close the connection
        self.connection.close()