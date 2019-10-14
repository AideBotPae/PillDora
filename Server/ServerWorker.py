from Server.database import DBMethods
import json
from datetime import date
import logging


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
        self.logger = logging.getLogger('AideBot')

    def connectClient(self):
        # Connexió amb la DB del Servidor
        self.checker = DBMethods(self.user_id)

    def handler_query(self, query):
        parsed_string = json.loads(query)
        instruction = parsed_string["function"]
        print(parsed_string)
        # Checking if there is any user with this user_id
        if instruction == "CHECK USER":
            user_id = parsed_string["parameters"]["user_id"]
            print(user_id)
            user_correct = self.checker.check_user(user_id=user_id)
            response = self.bot_parser(user_id=user_id, function="CHECK USER") + "[boolean: " + str(
                user_correct) + "] }"
            self.logger.info(response)
            return response
        # Checking if the user is introducing a correct password (we pass
        elif instruction == "CHECK PASSWORD":
            user_id = parsed_string["user_id"]
            password = parsed_string["parameters"]["password"]
            pwd_correct = self.checker.check_password(user_id=user_id, password=password)
            response = self.bot_parser(user_id=user_id, function="CHECK PASSWORD") + "[boolean: " + str(
                pwd_correct) + "] }"
            self.logger.info(response)
            return response
        # Add a new user
        elif instruction == "NEW PASSWORD":
            [new_user, new_password] = parsed_string[1:3]
            user_added = self.checker.add_user(new_user=new_user, new_password=new_password)
            while not user_added:
                user_added = self.checker.add_user(new_user=new_user, new_password=new_password)
            response = self.bot_parser(user_id=new_user, function="NEW PASSWORD") + "[boolean: " + str(
                user_added) + "] }"
            self.logger.info(response)
            return response
        # Introduce medicine
        elif instruction == "INTRODUCE MEDICINE":
            user_id = parsed_string["parameters"]["name"]
            national_code = parsed_string["parameters"]["cn"]
            is_there = self.checker.check_receipt(user_id=user_id, cn=national_code)
            # We are checking if the medicine is already on the database
            if not is_there:
                # If we are here, it means that the medicine wasn't on the database, so we input all the data
                self.checker.introd_medicine(user_id=user_id, query_parsed=parsed_string["parameters"])
                response = self.bot_parser(user_id=user_id, function="INTRODUCE MEDICINE") + "[code : 0] }"
                self.actualize_daily_table(user_id)
                self.logger.info(response)
                return response
            elif not self.checker.check_medicine_frequency(user_id=user_id, cn=national_code,
                                                           freq=parsed_string["parameters"]["FREQUENCY"]):
                # If we are here, the medicine is already on the database, we check first if the frequencies concur,
                # if not PROBLEM!
                response = self.bot_parser(user_id=user_id,
                                           function="INTRODUCE MEDICINE") + "[code : 1], " + " [freq_database : " + str(
                    self.checker.get_medicine_frequency(user_id=user_id,
                                                        cn=national_code)) + ' [freq_introduced : ' + str(
                    parsed_string["parameters"]["FREQUENCY"]) + "] }"
                self.logger.info(response)
                return response

            else:
                # If we are here, the medicine is already on the database, and the times match, so we add the
                # quantity only
                # AQUI EN EL FUTURO TOCAREMOS EL INVENTARIO
                response = self.bot_parser(user_id=user_id, function=
                "INTRODUCE MEDICINE") + "[code : 2] }"
                self.logger.info(response)
                return response

        elif instruction == "JOURNEY":
            # We output a series of actions to be done from a date to another one.
            [user_id, begin, end] = [parsed_string["user_id"], parsed_string["parameters"]["departure_date"],
                                     parsed_string["parameters"]["arrival_date"]]
            # If the beginning date and the end date create conflicts, the method will return a null calendar output
            calendar_output = self.checker.get_reminders(user_id=user_id, date=begin, to_date=end)
            # Right now, the journey will have the national code, on the future, we will use the medicine name!
            response = self.bot_parser(user_id=user_id,
                                       function="JOURNEY") + "[journey_info : " + calendar_output + "] }"
            self.logger.info(response)
            return response

        elif instruction == "TASKS CALENDAR":
            # We output a series of actions to be done from a date.
            [user_id, date_selected] = parsed_string[1:3]
            calendar_tasks = self.checker.get_reminders(user_id=user_id, date=date_selected)
            response = self.bot_parser(user_id, "TASKS CALENDAR") + "[tasks : " + calendar_tasks + "] }"
            self.logger.info(response)
            return response
        elif instruction == "DELETE REMINDER":
            # We check if the medicine introduced is there or not.
            [user_id, cn] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            deleted = self.checker.delete_information(user_id=user_id, national_code=cn)
            response = self.bot_parser(user_id=user_id, function="DELETE REMINDER") + "[boolean : " + str(
                deleted) + "] }"
            self.logger.info(response)
            return response
        elif instruction == "HISTORY":
            user_id = parsed_string["parameters"]["user_id"]
            history = self.checker.get_history(user_id=user_id)
            response = self.bot_parser(user_id=user_id, function="HISTORY") + "[reminder_info : " + history + "] }"
            self.logger.info(response)
            return response
        elif instruction == "GET REMINDER":
            [user_id, national_code] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            reminder_info = self.checker.get_reminders(user_id=user_id, date=date.today(), cn=national_code)
            response = self.bot_parser(self.user_id,
                                       function="GET REMINDER") + "[reminder_info : " + reminder_info + "] }"
            self.logger.info(response)
            return response
        else:
            user_id = parsed_string["parameters"]["user_id"]
            response = self.bot_parser(user_id=user_id,
                                       function="ERROR QUERY") + "[content : The query" + instruction + " is not on the query database] }"
            self.logger.info(response)
            return response

    def bot_parser(self, user_id, function):
        return """{"user_id": """ + str(user_id) + """ function": """ + function + """, "parameters": """

    def actualize_daily_table(self, user_id=None):
        if user_id:
            today = date.today()
            reminder_info = self.checker.get_reminders(user_id, today)
            response = self.bot_parser(self.user_id, "DAILY REMINDER") + "[reminder_info : " + reminder_info + "] }"
            self.logger.info(response)
            return response
        else:
            today = date.today()
            reminder_info = self.checker.get_reminders_all(today)
            response = self.bot_parser("ALL", "DAILY REMINDER") + "[reminder_info : " + reminder_info + "] }"
            self.logger.info(response)
            return response

    def json_query_comprovar(self, query):
        query_1 ="""{
                "glossary": {
                    "title": "example glossary",
                    "GlossDiv": {
                        "title": "S",
                        "GlossList": {
                            "GlossEntry": {
                                "ID": "SGML",
                                "SortAs": "SGML",
                                "GlossTerm": "Standard Generalized Markup Language",
                                "Acronym": "SGML",
                                "Abbrev": "ISO 8879:1986",
                                "GlossDef": {
                                    "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                    "GlossSeeAlso": ["GML", "XML"]
                                },
                                "GlossSee": "markup"
                            }
                        }
                    }
                }
        }"""
        query_jsoned = json.dumps()