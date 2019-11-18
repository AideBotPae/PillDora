import json
import socket
import sys

HOST, PORT = "localhost", 9001
#data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    query = {
        'user_id': 1234,
        'function': 'CHECK USER',
        'parameters': {'user_id': 'Pol'}
    }
    query = json.dumps(query)
    sock.sendall(bytes(query, "utf-8"))

    # Receive data from the server and shut down
    received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(query))
print("Received: {}".format(received))