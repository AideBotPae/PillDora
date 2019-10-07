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


class DBMethods:

    def check_user(self, user_id):
        with Database() as db:
            data = db.query("SELECT id FROM aidebot.users where id={id}".format(id=user_id))

            if not data:
                print("User isn't registered\n")
                return False
            else:
                print("User registered\n")
                return True

    def add_user(self, user_id, password):
        with Database() as db:
            db.execute(
                "INSERT INTO aidebot.users (id, password) VALUES ({id},'{pwd}')".format(id=user_id,
                                                                                        pwd=password))
            data = db.query("SELECT id FROM aidebot.users where id={id}".format(id=user_id))

            if not data:
                print("User not added\n")
                return False
            else:
                print('User added\n')
                return True

    def check_password(self, user_id, password):

        with Database() as db:
            # execute SQL query using execute() method.
            data = db.query("SELECT id, password FROM aidebot.users where id={id}".format(id=user_id))

            if password != data[0][1]:
                print('Wrong password')
                return False
            else:
                print('Correct password')
                return True

    def introd_medicine(self, query_parsed):
        print(query_parsed)

    def check_medicine(self, medicine_name):
        print(medicine_name)

    def check_medicine_schedule(self, medicine_name, begin, end):
        print(medicine_name, begin, end)

    def increase_medicine(self, medicine_name, quantity):
        return False

    def get_journey(self, user_id, begin, end):
        return False

    def get_tasks(self, user_id, date):
        return False

    def delete_information(self, user_id, national_code):
        return False

    def get_history(self, user_id):
        return False

    def get_inventory(self, user_id, national_code=None):
        return False

    def daily_table(self, user_id, national_code):
        return False


if __name__ == "__main__":
    checker = DBMethods()
    exists = checker.check_user()
    if exists:
        checker.check_password('hola')
        checker.check_password('prueba')
    else:
        print("Va como el culo, no detecta el unico id :(")
    checker_2 = DBMethods()
    exists_2 = checker_2.check_user()
    if exists_2:
        print("Maaaaal, no existe :(((")
    else:
        checker_2.add_user('prueba_checker_method')
