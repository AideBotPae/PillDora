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

    def introd_medicine(self, query_parsed):
        with Database() as db:
            # execute SQL query using execute() method.
            # data = db.query()
            print(" Hace falta introducir información no sacar ")


    def check_medicine(self, medicine_name, quantity):
        with Database() as db:
            # execute SQL query using execute() method.
            data = db.query("SELECT id, national_code FROM aidebot.medicines where national_code={national_code}".format(id=self.user_id))
            if data[0][1] is not None:
                return True
            else:
                return False

    def check_medicine_schedule(self, medicine_name, frequency):
        with Database() as db:
            # execute SQL query using execute() method.
            data = db.query("SELECT id, frequency FROM aidebot.medicines where frequency={frequency}".format(id=self.user_id))
            if frequency != data[0][1]:
                print('Wrong Frequency')
                return False
            else:
                print('Correct Frequency')
                return True