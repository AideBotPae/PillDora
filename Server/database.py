import pymysql


class DatabaseConnectionCredentials:

    @property
    def credentials(self):
        return {'ip': 'localhost', 'user': 'paesav', 'password': '12345678', 'database': 'aidebot'}


class ClientChecker:

    def __init__(self, user_id, credentials):
        self.user_id = user_id
        self.credentials = credentials
        self.user_exists = True

    def check_user(self):
        # Open database connection
        database = pymysql.connect(self.credentials['ip'], self.credentials['user'], self.credentials['password'],
                                   self.credentials['database'])
        cursor = database.cursor()

        cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))
        data = cursor.fetchall()
        database.close()
        if not data:
            print("User isn't registered\n")
            self.user_exists = False
            return False
        else:
            print("User registered\n")
            return True

    def add_user(self, password):
        database = pymysql.connect(self.credentials['ip'], self.credentials['user'], self.credentials['password'],
                                   self.credentials['database'])
        cursor = database.cursor()
        if not self.user_exists:
            cursor.execute(
                "INSERT INTO aidebot.users (id, password) VALUES ({id},{pwd})".format(id=self.user_id, pwd=password))
        database.close()

    def check_password(self, password):
        database = pymysql.connect(self.credentials['ip'], self.credentials['user'], self.credentials['password'],
                                   self.credentials['database'])
        cursor = database.cursor()

        # execute SQL query using execute() method.
        cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

        # Fetch all rows using fetchone() method.
        data = cursor.fetchall()

        database.close()
        if password != data[0][1]:
            print('Wrong password')
            return False
        else:
            print('Correct password')
            return True


if __name__ == "__main__":
    checker = ClientChecker(user_id=1, credentials=DatabaseConnectionCredentials.credentials)
    exists = checker.check_user()
    if exists:
        checker.check_password('hola')
        checker.check_password('prueba')
    else:
        print("Va como el culo, no detecta el unico id :(")
    checker_2 = ClientChecker(user_id=2, credentials=DatabaseConnectionCredentials.credentials)
    exists_2 = checker_2.check_user()
    if exists_2:
        print("Maaaaal, no existe :(((")
    else:
        checker_2.add_user('prueba_checker_method')
