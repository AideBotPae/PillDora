from Server.database import DatabaseConnector, ClientChecker
import json

class ServerWorker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.localhost = "localhost"
        self.port = 8080
        self.database = None
        self.checker = None



    def connectClient(self):
        # Connexió amb el Socket del Client (1)

        #Connexió amb la DB del Servidor
        self.database = DatabaseConnector.connect
        self.checker = ClientChecker(self.user_id, self.database)

    def closeWorker(self):
        # Fa falta tancar les connexions amb el socket
        self.database.close()

    def sendInfo(self, info):
        print("Fa falta programar")

    def readInfo(self):
        print("Fa falta programar")
        # lectura = socket.read()
        # handler_query(lectura)

    def handler_query(self, query):
        parsed_string = json.load(query)
        instruction = parsed_string[0]

        if instruction == "check_usr":
            user_correct = self.checker.check_user()
            self.sendInfo(user_correct)
        elif instruction == "check_pwd":
            pwd_correct = self.checker.check_password()
            self.sendInfo(pwd_correct)
        elif instruction == "add_user":
            self.checker.add_user(parsed_string[1])
        elif instruction == ""





        }

    def check_user_name(self):
        checker = ClientChecker(self.user_id, self.database)
        user_correct = checker.check_user()
        if user_correct:
            self.sendInfo(bool)
            pwd = self.readInfo()
            password_correct = checker.check_password(pwd)
            while not password_correct:
                password_correct = checker.check_password()
        else:
            self.sendInfo("pwd")
            pwd = self.readInfo()
            checker.add_user(pwd)







