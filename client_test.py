import json
import socket
import sys

HOST, PORT = "localhost", 9001
#data = " ".join(sys.argv[1:])

queries = [{"user_id": 1, "function": "INVENTORY", "parameters": {}}, {"user_id": 1,"function": "HISTORY", "parameters": {"date": "08/12/2019"}},
           {"user_id": 1,"function": "TASKS CALENDAR","parameters": {"date": "08/12/2019"}}, {"user_id": 1, "function":"JOURNEY","parameters": {"departure_date": "10/12/2019","arrival_date": "31/12/2019"}},
           {"user_id": 1,"function": "INTRODUCE MEDICINE","parameters": {"quantity": "2","CN": "664029.6","expiration_date": "10/01/2022"}},
           {"user_id": 1,"function": "INTRODUCE PRESCRIPTION","parameters": {"end_date": "31/12/2019","quantity": "56","freq": "2","CN": "664029.6"}}]

responses = []
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    for query in queries:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        query = json.dumps(query)
        sock.sendall(bytes(query, "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        responses.append(received)

        print("Sent:     {}".format(query))
        print("Received: {}".format(received))

print(responses)