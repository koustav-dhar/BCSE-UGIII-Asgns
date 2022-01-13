import socket
import threading
import time

# Define sender and receiver connection list
sender_list = []
receiver_list = []

# Define receiver address list
receiver_address = []

# Define vulnerable time
vulnerable_time = 0.5

# Define propagation time
propagation_time = 0.1

# Define sender count
sender_count = 0

# Define variable to indicate collision
collision = False

# Define variable to indicate channel is busy
is_busy = False

# Define the lock object
my_lock=threading.Lock()

# Function to handle channel actions for data passing
def channel(receiver, packet):
    # Try to get the lock for accessing global variables
    my_lock.acquire()

    global is_busy
    global collision

    # If channel is idle, make it busy
    # Else set the collision flag true
    if not is_busy:
        is_busy = True
    else:
        collision = True
        my_lock.release()
        return "collision"

    # Unlock
    my_lock.release()
    
    # Sleep for vulnerable time to detect if collision happened
    time.sleep(propagation_time)

    # If collision didn't happened send tne packet to receiver
    msg = ''
    if not collision:
        receiver.send(packet)
        msg = 'Sent successfully'
    else:
        msg = "collision"

    # Try to get the lock for accessing global variables
    my_lock.acquire()

    # Set the global variables properly
    is_busy = False
    collision = False

    # Unlock
    my_lock.release()

    return msg


# Function for run method of client thread
def sender(connection, receiver):
    # Define data
    data="start"

    global is_busy

    # Loop until data transmission ends
    while data!="close":

        # Wait and receive sender sent data
        data =connection.recv(1024)
        data = data.decode()

        # If sender asks for status (busy/idle) send it
        if data == 'status':
            if is_busy:
                connection.send(str.encode('Busy'))
            else:
                connection.send(str.encode('Idle'))
        
        # If sender is sending data call 'channel' function for handling
        # Return the transmission status (sent successfully/collision) to sender thereafter
        elif data == 'sending':
            connection.send(str.encode('ok'))
            packet = connection.recv(1024)
            reply = channel(receiver,packet)
            connection.send(str.encode(reply))

        # If data transmission ends, notify receiver
        elif data == 'end':
            receiver.send(str.encode(data))

    # Close the connection and corresponding receiver
    connection.close()
    receiver.close()

    # Remove list entries
    sender_list.remove(connection)
    receiver_list.remove(receiver)

    # Decrease sender count
    global sender_count
    sender_count -= 1


# Function to specify server functionality
def server():
    # Defien server IP address
    server_ip='127.0.0.2'
    # Define server port address
    server_port=1233
    # Define total server address
    server_address=(server_ip,server_port)

    # Initialize server
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # Bind server to the address
    server.bind(server_address)

    # Define maximum waiting client requests
    server.listen(5)

    # Notify that server started
    print("Server started")

    # Initialize sender count
    global sender_count

    # Put server on listen mode and accept client requests
    while True:
        # Accept client request
        new_connection,address=server.accept()
        
        # Notify client's joining
        print(address,' joined')

        # Receive client name from client and send port-number to it
        new_connection.send(str.encode(str(address[1])))
        name=new_connection.recv(1024)
        name=name.decode()

        # Update sender and receiver list 
        # If it's receiver add receiver connection and address into list
        if name == 'receiver':
            receiver_list.append(new_connection)
            receiver_address.append(address)

        # If it's sender add sender conection into list
        # Send corresponding receiver address to sender
        # Start sender thread providing the receiver connection
        elif name == 'sender':
            sender_list.append(new_connection)
            new_connection.send(str.encode(str(receiver_address[sender_count][1])))

            # Define and start new client thread
            new_thread=threading.Thread(target=sender,args=(new_connection,receiver_list[sender_count]))
            new_thread.start()

            sender_count += 1


# Main function
if __name__=='__main__':
    server()