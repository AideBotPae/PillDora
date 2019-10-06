from Server.database import ClientChecker
import json


class ServerWorker:

    def __init__(self, user_id):
        self.user_id = user_id
        self.localhost = "localhost"
        self.port = 8080
        self.checker = None

    def connectClient(self):
        # Connexió amb la DB del Servidor
        self.checker = ClientChecker(self.user_id)

    def handler_query(self, query):
        parsed_string = json.load(query)
        instruction = parsed_string[0]

        # Checking if there is any user with this user_id
        if instruction == "check_usr":
            user_correct = self.checker.check_user()
            return user_correct
        # Checking if the user is introducing a correct password (we pass
        elif instruction == "check_pwd":
            [user_id, password] = parsed_string[1:3]
            pwd_correct = self.checker.check_password(user_id, password)
            return pwd_correct
        # Add a new user
        elif instruction == "add_user":
            [new_user, new_password] = parsed_string[1:3]
            user_added = self.checker.add_user(new_user, new_password)
            return user_added
        # Introduce medicine
        elif instruction == "intr_medicine":
            medicine_name = parsed_string[1]
            is_there = self.checker.check_medicine(medicine_name)

            # We are checking if the medicine is already on the database
            if not is_there:
                # If we are here, it means that the medicine wasn't on the database, so we input all the data
                self.checker.introd_medicine(parsed_string[1:])
                return "Code 0"
            elif self.checker.check_medicine_schedule(medicine_name, parsed_string[3]):
                # If we are here, the medicine is already on the database, we check first if the times concur,
                # if not PROBLEM!
                return "Code 1"
            else:
                # If we are here, the medicine is already on the database, and the times match, so we add the
                # quantity only
                quantity = parsed_string[2]
                self.checker.increase_medicine(medicine_name, quantity)
                return "Code 2, added " + quantity + " pills of " + medicine_name
        elif instruction == "check_med":
            med_checked = False

            return med_checked
        elif instruction == "check_reminder":
            reminder_checked = False

            return reminder_checked
        elif instruction == "calendar_choose":
            calendar_output = False

            return calendar_output
        elif instruction == "calendar_tasks":
            calendar_tasks = False

            return calendar_tasks
        elif instruction == "get_cn":
            cn = False

            return cn
        else:
            return "ERROR"

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
