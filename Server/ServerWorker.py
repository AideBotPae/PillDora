from Server.database import DatabaseConnector, ClientChecker

class ServerWorker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.localhost = "localhost"
        self.port = 8080
        self.database = None

    def connectClient(self):
        # Connexió amb el Socket del Client

        #Connexió amb la DB del Servidor
        self.database = DatabaseConnector.connect

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


    def sendInfo(self, info):
        print("Fa falta programar")

    def readInfo(self):
        print("Fa falta programar")
        return 0


    def closeWorker(self):
        # Fa falta tancar les connexions amb el socket
        self.database.close()

