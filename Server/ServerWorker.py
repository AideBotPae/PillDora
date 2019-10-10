from Server.database import ClientChecker
import json
from datetime import date
import time


class Reminder(object):
    def __init__(self, user_id, medicine, hour_of_pill):
        self.user_id = user_id
        self.cn = medicine["NATIONAL_CODE"]
        self.hour = hour_of_pill


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
            while not user_added:
                user_added = self.checker.add_user(new_user, new_password)

        # Introduce medicine
        elif instruction == "INTRODUCE MEDICINE":
            user_id = parsed_string["parameters"]["name"]
            medicine_name = parsed_string["parameters"]["name"]
            is_there = self.checker.check_medicine(user_id, medicine_name)
            # We are checking if the medicine is already on the database
            if not is_there:
                # If we are here, it means that the medicine wasn't on the database, so we input all the data
                self.checker.introd_medicine(user_id, parsed_string["parameters"])
                return "Code 0"
            elif not self.checker.check_medicine_schedule(user_id, medicine_name, parsed_string["parameters"]["FREQUENCY"]):
                # If we are here, the medicine is already on the database, we check first if the frequencies concur,
                # if not PROBLEM!
                return "Code 1"
            else:
                # If we are here, the medicine is already on the database, and the times match, so we add the
                # quantity only
                return "Code 3"
        elif instruction == "JOURNEY":
            # We output a series of actions to be done from a date to another one.
            [user_id, begin, end] = [parsed_string["user_id"], parsed_string["parameters"]["departure_date"],
                                     parsed_string["parameters"]["arrival_date"]]
            # If the beginning date and the end date create conflicts, the method will return a null calendar output
            calendar_output = self.checker.get_journey(user_id, begin, end)
            # Right now, the journey will have the national code, on the future, we will use the medicine name!
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
        number_of_hours = 24 / frequency
        reminders = list()
        for i in range(number_of_hours):
            reminder = Reminder(user_id, parsed_string, (i+1)*frequency)
            reminders.append(reminder)
        return reminders




    def actualize_daily_table(self, user_id):
        json_medicines = self.checker.get_inventory(user_id)
        medicines = json.load(json_medicines)
        for medicine in medicines:
            begin_date = medicine["BEGIN_DATE"]
            end_date = medicine["END_DATE"]
            today = date.today()
            cn = medicine["NATIONAL_CODE"]
            if today > begin_date:
                is_there = self.checker.daily_table(user_id, cn)
                if not is_there:
                    reminders = self.create_reminders(user_id, medicine)
                    modified = self.checker.add_daily_table(user_id, reminders)
                if today > end_date:
                    modified = self.checker.delete_from_daily_table(user_id, cn)

        daily_table = self.checker.get_daily_table(user_id)
        self.notify_telegram(daily_table)
        return modified







