import pymysql


class ClientChecker:

    def __init__(self, user_id, passsword):
        self.user_id = user_id
        self.password = passsword

    def run(self):
        # Open database connection
        db = pymysql.connect("localhost", "paesav", "12345678", "aidebot")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        # execute SQL query using execute() method.
        cursor.execute("SELECT id, password FROM aidebot.users where id={id}".format(id=self.user_id))

        # Fetch a single row using fetchone() method.
        data = cursor.fetchall()

        print("Data ")
        print(data)

        # disconnect from server
        db.close()


if __name__ == "__main__":
    checker = ClientChecker(user_id=1, passsword=12)
    checker.run()
