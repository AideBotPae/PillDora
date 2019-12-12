import socket
import json
from threading import Thread
from serverworker import ServerWorker


class MyThread(Thread):

    def __init__(self, connection):
        super().__init__()
        self.conn = connection
        self.server_worker = None

    def run(self):
        while True:
            query = str(self.conn.recv(2048), "utf-8")[2:]
            print(query, type(query))
            if "Exit" in query:
                self.conn.send(bytes("end", "utf-8"))
                return
            user_id = json.loads(query)['user_id']
            #print(user_id)

            if self.server_worker is None:
                self.server_worker = ServerWorker(user_id)

            self.conn.send(bytes(self.server_worker.handler_query(query), "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 12346
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("socket listening")

    while True:
        conn, addr = s.accept()
        MyThread(conn).start()
