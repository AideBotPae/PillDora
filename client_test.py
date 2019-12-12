import json
import socket
import sys

HOST, PORT = "localhost", 12346
#data = " ".join(sys.argv[1:])

queries = [{"user_id":  323299533, "function": "INVENTORY", "parameters": {}}, {"user_id":  323299533, "function": "HISTORY", "parameters": {"date": "2019-12-08"}},
           {"user_id":  323299533, "function": "TASKS CALENDAR", "parameters": {"date": "2019-12-08"}}, {"user_id":  323299533, "function": "JOURNEY", "parameters": {"departure_date": "2019-12-10", "arrival_date": "2019-12-30"}},
           {"user_id":  323299533, "function": "INTRODUCE MEDICINE", "parameters": {"QUANTITY": "2", "NAME": "664029", "EXP_DATE": "2022-01-10"}},
           {"user_id":  821061948, "function": "INTRODUCE PRESCRIPTION", "parameters": {"END_DATE": "2019-12-19", "QUANTITY": "56", "FREQUENCY": "2", "NAME": "664029"}}, 'Exit']

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

   # Connect to server and send data
    sock.connect((HOST, PORT))
    f = open("queries.txt", "w+")

    for query in queries:

        query = json.dumps(query)
        sock.sendall(bytes(query, "utf-8"))

        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        f.write(f"{received}\n")

        print("Sent:     {}".format(query))
        print("Received: {}".format(received))

    f.close()
