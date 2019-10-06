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
        if instruction == "CHECK USER":
            user_correct = self.checker.check_user()
            return user_correct
        # Checking if the user is introducing a correct password (we pass
        elif instruction == "CHECK PASSWORD":
            [user_id, password] = parsed_string[1:3]
            pwd_correct = self.checker.check_password(user_id, password)
            return pwd_correct
        # Add a new user
        elif instruction == "NEW PASSWORD":
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
        elif instruction == "JOURNEY":
            # We output a series of actions to be done from a date to another one.
            [user_id, begin, end] = parsed_string[1:4]
            # If the beginning date and the end date create conflicts, the method will return a null calendar output
            calendar_output = self.checker.get_journey(user_id, begin, end)
            return calendar_output
        elif instruction == "TASKS CALENDAR":
            # We output a series of actions to be done from a date.
            [user_id, date] = parsed_string[1:3]
            calendar_tasks = self.checker.get_tasks(user_id, date)
            return calendar_tasks
        elif instruction == "DELETE REMINDER":
            # We check if the medicine introduced is there or not.
            [user_id, medicine_name, cn] = parsed_string[1:4]
            is_there = self.checker.check_medicine(medicine_name)
            if not is_there:
                # If it is not there, we send a False statement.
                return False
            else:
                info = self.checker.get_info_from_med(medicine_name, cn)
                self.checker.delete_information(medicine_name, cn)
                return info
        elif instruction == "HISTORY":
            user_id = parsed_string[1]
            history = self.checker.get_history(user_id)
            return history
        elif instruction == "GET INFO":
            [user_id, cn] = parsed_string[1:3]
            reminder = self.checker.get_medicine(user_id, cn)
            return reminder
        else:
            return "ERROR"


