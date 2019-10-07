from Server.database import ClientChecker
import json
from datetime import date


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
        instruction = parsed_string["function"]

        # Checking if there is any user with this user_id
        if instruction == "CHECK USER":
            user_id = parsed_string["parameters"]["user_id"]
            user_correct = self.checker.check_user(user_id=user_id)
            return user_correct
        # Checking if the user is introducing a correct password (we pass
        elif instruction == "CHECK PASSWORD":
            user_id = parsed_string["user_id"]
            password = parsed_string["parameters"]["password"]
            pwd_correct = self.checker.check_password(user_id, password)
            return pwd_correct
        # Add a new user
        elif instruction == "NEW PASSWORD":
            [new_user, new_password] = parsed_string[1:3]
            user_added = self.checker.add_user(new_user, new_password)
            return user_added
        # Introduce medicine
        elif instruction == "INTRODUCE MEDICINE":
            medicine_name = parsed_string["parameters"]["name"]
            is_there = self.checker.check_medicine(medicine_name)
            # We are checking if the medicine is already on the database
            if not is_there:
                # If we are here, it means that the medicine wasn't on the database, so we input all the data
                self.checker.introd_medicine(parsed_string["parameters"])
                return "Code 0"
            elif self.checker.check_medicine_schedule(medicine_name, parsed_string["parameters"]["FREQUENCY"]):
                # If we are here, the medicine is already on the database, we check first if the frequencies concur,
                # if not PROBLEM!
                return "Code 1"
            else:
                # If we are here, the medicine is already on the database, and the times match, so we add the
                # quantity only
                quantity = parsed_string["parameters"]["QUANTITY"]
                self.checker.increase_medicine(medicine_name, quantity)
                return "Code 2, added " + quantity + " pills of " + medicine_name
        elif instruction == "JOURNEY":
            # We output a series of actions to be done from a date to another one.
            [user_id, begin, end] = [parsed_string["user_id"], parsed_string["parameters"]["departure_date"],
                                     parsed_string["parameters"]["arrival_date"]]
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
            [user_id, cn] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            deleted = self.checker.delete_information(user_id, cn)
            return deleted
        elif instruction == "HISTORY":
            user_id = parsed_string["parameters"]["user_id"]
            history = self.checker.get_history(user_id)
            return history
        elif instruction == "GET REMINDER":
            [user_id, national_code] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            reminder_info = self.checker.get_medicine(user_id, national_code)
            return reminder_info
        else:
            return "ERROR"



    def create_reminders(self, user_id, parsed_string):
        frequency = parsed_string["parameters"]["frequency"]
        today = date.today()
        begin = today.strftime("%d/%m/%Y")
        end = parsed_string["parameters"]["END_DATE"]

        if datetime.date.today().strftime('%A') == 'Wednesday':
            print("Pick up the kids!")

