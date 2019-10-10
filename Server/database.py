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
            data = db.query("SELECT password FROM aidebot.users where id={id}".format(id=user_id))

            if password != data[0]:
                print('Wrong password')
                return False
            else:
                print('Correct password')
                return True

    def introd_receipt(self, query_parsed, user_id, date):
        with Database() as db:
            db.execute('''INSERT INTO aidebot.receipts (user_id,national_code, frequency, quantity, begin_date, end_date)
                        values ({id},{cn},{frequency},'{quantity}','{init}','{end}')'''.format(
                id=user_id, cn=query_parsed['NAME'], frequency=query_parsed['FREQUENCY'],
                quantity=query_parsed['QUANTITY'],
                init=date,
                end=query_parsed['END_DATE']
            ))

            # Comprobar que se ha introducido bien

    def check_receipt(self, cn, user_id):
        with Database() as db:
            data = db.query('''SELECT count(*) FROM aidebot.receipts WHERE user_id={id} and national_code={med}
            '''.format(id=user_id, med=cn))
            if data[0] == 0:
                return False
            else:
                return True

    def get_medicine_frequency(self, user_id, cn):
        with Database() as db:
            data = db.query('''SELECT frequency 
            FROM aidebot.receipts
            WHERE user_id={id} and national_code={cn}
            '''.format(id=user_id, cn=cn))
            return data

    def check_medicine_frequency(self, user_id, cn, freq):
        with Database() as db:
            data = db.query('''SELECT frequency FROM aidebot.receipts WHERE user_id={id} and national_code={cn}
            '''.format(id=user_id, cn=cn))

            if data[0] == freq:
                return True
            else:
                return False

    ''' 
    TODO
    '''
    def get_inventory(self, user_id, begin, end):
        with Database() as db:
            data = db.query(''' SELECT national_code, frequency, init_date, end_date, expiracy_date
             FROM aidebot.inventory 
             WHERE user_id={id} and init_date>='{begin}' and init_date<='{end}'
            '''.format(begin=begin, end=end, id=user_id
                       ))
            return data

    def create_reminders(self):
        with Database() as db:
            return False

    def get_reminders(self, user_id, date, to_date=None):
        with Database() as db:
            if to_date:
                data = db.query(''' SELECT national_code, date
                FROM aidebot.reminders 
                WHERE date>='{date}' and date<='{to_date}' and user_id={id}
                '''.format(date=date, to_date=to_date, id=user_id))
                return data
            else:
                data = db.query('''SELECT national_code, date
                FROM aidebot.reminders 
                WHERE date ='{date}' and user_id={id}
                '''.format(date=date, id=user_id))
                return data

    def delete_reminders(self, user_id, national_code):
        with Database() as db:

            db.execute('''DELETE FROM aidebot.inventory WHERE user_id={id} and national_code={cn}
            '''.format(id=user_id, cn=national_code))
            db.execute('''DELETE FROM aidebot.reminders WHERE user_id={id} and national_code={cn}
            '''.format(id=user_id, cn=national_code))
            #Comprobar si se ha hecho bien
            return True

    def get_history(self, user_id):
        with Database() as db:
            data = db.query('''
            ''')

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
