import pymysql


class DatabaseConnector:
    @property
    def connect(self):
        # Open database connection
        return pymysql.connect("localhost", "paesav", "12345678", "aidebot")


class ClientChecker:

    def __init__(self, user_id, database):
        self.user_id = user_id
        self.password = ''
        self.user_exists = True
        self.db = database
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

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
    database = DatabaseConnector.connect
    checker = ClientChecker(user_id=1, database=database)
    exists = checker.check_user()
    if exists:
        checker.check_password('hola')
        checker.check_password('prueba')
    else:
        print("Va como el culo, no detecta el unico id :(")
    checker_2 = ClientChecker(user_id=2, database=database)
    exists_2 = checker_2.check_user()
    if exists_2:
        print("Maaaaal, no existe :(((")
    else:
        checker_2.add_user('prueba_checker_method')


