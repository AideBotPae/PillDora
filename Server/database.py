import pymysql


class DatabaseConnector:
    # Open database connection
    database = pymysql.connect("localhost", "paesav", "12345678", "aidebot")

    @property
    def database(self):
        return self.database

    @property
    def cursor(self):
        return self.database.cursor()


class ClientChecker:

    def __init__(self, user_id, databaseconnector):
        self.user_id = user_id
        self.password = ''
        self.user_exists = True
        self.db = databaseconnector.database
        # prepare a cursor object using cursor() method
        self.cursor = databaseconnector.cursor

    def check_user(self):
        self.cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))
        data = self.cursor.fetchall()

        if not data:
            print("User isn't registered\n")
            self.user_exists = False
            return False
        else:
            print("User registered\n")
            return True

    def add_user(self, password):
        if not self.user_exists:
            self.password = password
            self.cursor.execute(
                "INSERT INTO aidebot.users (id, password) VALUES ({id},{pwd})".format(id=self.id, pwd=self.password))

    def check_password(self, password):
        self.password = password
        # execute SQL query using execute() method.
        self.cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

        # Fetch all rows using fetchone() method.
        data = self.cursor.fetchall()

        if self.password != data[0][1]:
            print('Wrong password')
            return False
        else:
            print('Correct password')
            return True


if __name__ == "__main__":
    checker = ClientChecker(user_id=1, databaseconnector=DatabaseConnector)
    exists = checker.check_user()
    if exists:
        checker.check_password('hola')
        checker.check_password('prueba')
    else:
        print("Va como el culo, no detecta el unico id :(")
    checker_2 = ClientChecker(user_id=2, databaseconnector=DatabaseConnector)
    exists_2 = checker_2.check_user()
    if exists_2:
        print("Maaaaal, no existe :(((")
    else:
        checker_2.add_user('prueba_checker_method')
