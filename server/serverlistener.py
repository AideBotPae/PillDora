import socket
import json
from threading import Thread
from server.serverworker import ServerWorker


class MyThread(Thread):

    def __init__(self, connection):
        super().__init__()
        self.conn = connection
        self.server_worker = None

    def run(self):
        while True:
            query = self.conn.recv(2048)
            if query == b'Exit':
                break
            print(query)
            user_id = json.loads(query)['user_id']
            print(user_id)

            if self.server_worker is None:
                self.server_worker = ServerWorker(user_id)

            self.conn.send(bytes(self.server_worker.handler_query(query), "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 9001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("socket listening")

    while True:
        conn, addr = s.accept()
        MyThread(conn).start()
    #s.close()
