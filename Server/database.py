import pymysql


class DatabaseConnectionCredentials:

    @property
    def credentials(self):
        return {'ip': 'localhost', 'user': 'paesav', 'password': '12345678', 'database': 'aidebot'}


class Database(DatabaseConnectionCredentials):
    def __init__(self):
        self._conn = pymysql.connect(self.credentials['ip'], self.credentials['user'], self.credentials['password'],
                                     self.credentials['database'])
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql_query):
        self.cursor.execute(sql_query)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql_query):
        self.cursor.execute(sql_query)
        return self.fetchall()


class ClientChecker:

    def __init__(self, user_id):
        self.user_id = user_id

    def check_user(self):
        with Database() as db:
            data = db.query("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

            if not data:
                print("User isn't registered\n")
                return False
            else:
                print("User registered\n")
                return True

    def add_user(self, password):
        with Database as db:
            db.execute(
                "INSERT INTO aidebot.users (id, password) VALUES ({id},{pwd})".format(id=self.user_id,
                                                                                      pwd=password))

    def check_password(self, password):

        with Database as db:
            # execute SQL query using execute() method.
            data = db.query("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

            if password != data[0][1]:
                print('Wrong password')
                return False
            else:
                print('Correct password')
                return True


if __name__ == "__main__":
    checker = ClientChecker(user_id=1)
    exists = checker.check_user()
    if exists:
        checker.check_password('hola')
        checker.check_password('prueba')
    else:
        print("Va como el culo, no detecta el unico id :(")
    checker_2 = ClientChecker(user_id=2)
    exists_2 = checker_2.check_user()
    if exists_2:
        print("Maaaaal, no existe :(((")
    else:
        checker_2.add_user('prueba_checker_method')

