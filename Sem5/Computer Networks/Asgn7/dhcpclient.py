import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
DHCPport = 65100        # The port used by the server

# Create a UDP Socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Client Started...")

address = (HOST, DHCPport)

print("Requesting for temporary IP from DHCP Server...")
client.sendto(str.encode("Request IP"), address)
ip, server = client.recvfrom(1024)
print("Temporary IP Allocated! [" + ip.decode() + "]")

while True:
    print("Press q to quit, anything else to stay online.")
    choice = input()
    if choice == "q" or choice == "Q":
        break

print("Terminating...")
client.sendto(ip, address)
