import pymysql


class DatabaseConnector:
    @property
    def connect(self):
        # Open database connection
        return pymysql.connect("localhost", "paesav", "12345678", "aidebot")


class ClientChecker(DatabaseConnector):

    def __init__(self, user_id, passsword):
        self.user_id = user_id
        self.password = passsword
        self.user_exists = True
        self.db = self.connect

        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()

    def check_user(self):
        self.cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))
        data = self.cursor.fetchall()

        if not data:
            print("User isn't registered\n")
        return False

    def add_user(self):
        if not check_user:


    def check_password(self):
        # execute SQL query using execute() method.
        self.cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

        # Fetch all rows using fetchone() method.
        data = self.cursor.fetchall()

        if self.password != data[0][1]:
            print('Wrong password')


if __name__ == "__main__":
    checker = ClientChecker(user_id=1, passsword=12)
    checker.check_password()
