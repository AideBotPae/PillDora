from server.database import DBMethods
import server.cima as cima
import json
import datetime
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
        self.checker = DBMethods()
        self.logger = logging.getLogger('ServerWorker')

    def connectClient(self):
        # CONNECTION OF THE SERVER WORKER WITH THE MYSQL DATABASE
        self.checker = DBMethods()

    def handler_query(self, query):
        parsed_string = json.loads(query)
        instruction = parsed_string["function"]
        # CHECKING IF THERE IS ANY USER WITH A CERTAIN USER_ID
        if instruction == "CHECK USER":
            user_id = parsed_string["parameters"]["user_id"]
            print(user_id)
            user_correct = self.checker.check_user(user_id=user_id)
            response = self.bot_parser(user_id=user_id, function="CHECK USER") + ' "boolean": "' + str(
                user_correct) + '"}}'
            self.logger.info(response)
            return response
        # CHECKING IF THE USER IS INTRODUCING THE CORRECT PASSWORD
        elif instruction == "CHECK PASSWORD":
            user_id = parsed_string["user_id"]
            password = parsed_string["parameters"]["password"]
            pwd_correct = self.checker.check_password(user_id=user_id, password=password)
            response = self.bot_parser(user_id=user_id, function="CHECK PASSWORD") + ' "boolean": "' + str(
                pwd_correct) + '"}}'
            self.logger.info(response)
            return response
        # ADDING A NEW USER
        elif instruction == "NEW PASSWORD":
            new_user = parsed_string["user_id"]
            new_password = parsed_string["parameters"]["new_password"]
            user_added = self.checker.add_user(new_user=new_user, new_password=new_password)
            while not user_added:
                user_added = self.checker.add_user(new_user=new_user, new_password=new_password)
            response = self.bot_parser(user_id=new_user, function="NEW PASSWORD") + ' "boolean": "' + str(
                user_added) + '"}}'
            self.logger.info(response)
            return response
        # INTRODUCING NEW PRESCRIPTION
        elif instruction == "INTRODUCE PRESCRIPTION":
            user_id = parsed_string["user_id"]
            national_code = parsed_string["parameters"]["NAME"]
            is_there = self.checker.check_receipt(user_id=user_id, cn=national_code)
            if not is_there:
                self.checker.introd_receipt(user_id=user_id, query_parsed=parsed_string["parameters"],
                                            date=datetime.date.today().strftime("%Y-%m-%d"))
                response = self.bot_parser(user_id=user_id, function="INTRODUCE PRESCRIPTION") + """ "Code": "0"}}"""

                self.logger.info(response)
                return response
            elif not self.checker.check_medicine_frequency(user_id=user_id, cn=national_code,
                                                           freq=parsed_string["parameters"]["FREQUENCY"]):

                response = self.bot_parser(user_id=user_id,
                                           function="INTRODUCE PRESCRIPTION") + '"Code": "1" , "freq_database" : "' + str(
                    self.checker.get_medicine_frequency(user_id=user_id,
                                                        cn=national_code)) + '", "freq_introduced" : "' + str(
                    parsed_string["parameters"]["FREQUENCY"]) + '"}}'
                self.logger.info(response)
                return response
            else:
                response = self.bot_parser(user_id=user_id, function=
                "INTRODUCE PRESCRIPTION") + '"Code" : "2"}}'
                self.logger.info(response)
                return response

        # INTRODUCING NEW MEDICINE BOUGHT:
        elif instruction == "INTRODUCE MEDICINE":
            user_id = parsed_string["user_id"]
            national_code = parsed_string["parameters"]["NAME"]
            self.checker.intr_inventory(user_id=user_id, query_parsed=parsed_string["parameters"])
            response = self.bot_parser(user_id=user_id, function="INTRODUCE MEDICINE") + """ "Code": "0"}}"""
            self.logger.info(response)
            return response

        # THE USER WANTS TO PLAN A JOURNEY
        elif instruction == "JOURNEY":
            # WE OUTPUT A SERIES OF ACTIONS TO BE DONE FROM A LEAVING DATE TO THE DEPARTURE ONE
            [user_id, begin, end] = [parsed_string["user_id"], parsed_string["parameters"]["departure_date"],
                                     parsed_string["parameters"]["arrival_date"]]
            # IF THE BEGINNING DAT AND THE END DATE CONFLICTS, THE METHOD WILL RETURN A NULL CALENDAR OUTPUT
            calendar_output = self.checker.get_reminders(user_id=user_id, date=begin, to_date=end)
            if calendar_output is not None:
                journey_info = "Quantity of meds to take:\\n"
                for output in list(calendar_output.keys()):
                    journey_info += "\\t-> " + cima.get_med_name(str(output)) + " : " + str(calendar_output[output]) + "\\n"
            response = self.bot_parser(user_id=user_id,
                                       function="JOURNEY") + '"journey_info" : "' + journey_info + '"}}'
            self.logger.info(response)
            return response

        # THE USER WANTS INFORMATION ABOUT THE REMINDERS OF A SPECIFIC DATE
        elif instruction == "TASKS CALENDAR":
            # WE OUTPUT A SERIES OF ACTIONS TO BE DONE FOR A SPECIFIC DATE
            [user_id, date_selected] = [parsed_string["user_id"], parsed_string["parameters"]["date"]]
            calendar_output = self.checker.get_reminders(user_id=user_id, date=date_selected)
            if calendar_output is not None:
                journey_info = "Reminders:\\n"
                for output in calendar_output:
                    time=str(output[1]).split(',')[1] if len(str(output[1]).split(','))==2 else str(output[1])
                    journey_info += "\\t-> " + cima.get_med_name(str(output[0])) + " : " + time + "\\n"
            response = self.bot_parser(user_id, "TASKS CALENDAR") + '"tasks" : "' + journey_info + '"}}'
            self.logger.info(response)
            return response

        # THE USER WANTS TO DELETE A REMINDER
        elif instruction == "DELETE REMINDER":
            # WE CHECK IF A MEDICINE REMINDER IS THERE FIRST
            [user_id, cn] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            deleted = self.checker.delete_reminders(user_id=user_id, national_code=cn)
            response = self.bot_parser(user_id=user_id, function="DELETE REMINDER") + '"boolean" : "' + str(
                deleted) + '"}}'
            self.logger.info(response)
            return response

        # THE USER ASKS FOR THE CURRENT TREATMENT
        elif instruction == "CURRENT TREATMENT":
            user_id = parsed_string["parameters"]["user_id"]
            current_treatment = self.checker.get_currentTreatment(user_id=user_id)
            if current_treatment is not ():
                current_treatment_info = "Meds currently being taken :\\n"
                for output in current_treatment:
                    current_treatment_info += "\\t-> Taking " + cima.get_med_name(str(output[0])) + " until the date of " + str(output[1]).split()[0] + "\\n"
            else:
                current_treatment_info="False"
            response = self.bot_parser(user_id=user_id,
                                       function="CURRENT TREATMENT") + '"reminder_info" : "' + current_treatment_info + '"}}'
            self.logger.info(response)
            return response

        # THE USER ASKS FOR THE HISTORY OF PILLS TAKEN
        elif instruction == "HISTORY":
            user_id = parsed_string["parameters"]["user_id"]
            history = self.checker.get_history(user_id=user_id)
            if history is not ():
                history_info = "History of last meds :\\n"
                for output in history:
                    history_info += "\\t-> " + cima.get_med_name(str(output[0])) + " of " + str(output[1])
                    if output[2]:
                        history_info +=": taken\\n"
                    else:
                        history_info += ": not taken\\n"
            else:
                history_info="False"
            response = self.bot_parser(user_id=user_id,
                                       function="HISTORY") + '"history" : "' + history_info + '"}}'
            self.logger.info(response)
            return response

            # THE USER ASKS TO INTRODUCE HISTORY OF PILLS TAKEN
        elif instruction == "INTRODUCE HISTORY":
            user_id = parsed_string["parameters"]["user_id"]
            history = self.checker.intr_to_history(user_id=user_id, query_parsed=parsed_string["parameters"])
            response = self.bot_parser(user_id=user_id,
                                       function="INTRODUCE HISTORY") + '"boolean" : "' + history + '"}}'
            self.logger.info(response)
            return response

            # THE USER ASKS FOR THE HISTORY OF PILLS TAKEN
        elif instruction == "INVENTORY":
            user_id = parsed_string["parameters"]["user_id"]
            inventory = self.checker.get_inventory(user_id=user_id)
            if inventory is not ():
                inventory_info = "Your current inventory consists on:\\n"
                for output in inventory:
                    print(output)
                    inventory_info += "\\t-> There are " + str(output[1]) + " of " + cima.get_med_name(str(output[0])) + " which expire on " + datetime.datetime.strftime(output[2],
                                                                                         "%Y-%m-%d")
            else:
                inventory_info="False"
            response = self.bot_parser(user_id=user_id,
                                       function="INVENTORY") + '"inventory" : "' + inventory_info + '"}}'
            self.logger.info(response)
            return response

        # THE USER ASKS FOR THE REMINDERS FOR TODAY ON A SPECIFIC NATIONAL CODE
        elif instruction == "GET REMINDER":
            [user_id, national_code] = [parsed_string["user_id"], parsed_string["parameters"]["CN"]]
            reminder_info = self.checker.get_reminders(user_id=user_id, date=datetime.date.today().strftime("%Y-%m-%d"),
                                                       cn=national_code)
            # THIS MEANS THAT WE GOT INFORMATION ABOUT THIS MEDICINE, SO WE ARE PARSING IT
            if reminder_info != '"False"':
                reminder_info = '"CN":"' + str(reminder_info[0][0]) + '","frequency":"' + str(
                    reminder_info[0][1]) + '","end_date":"' + datetime.datetime.strftime(reminder_info[0][2],
                                                                                         "%Y-%m-%d") + '"'
            else:
                # THIS MEANS THAT WE GOT NO INFORMATION ABOUT THIS MEDICINE FOR THE REMINDERS OF TODAY AND WE SEND NONE.
                reminder_info = '"CN":' + reminder_info
            response = self.bot_parser(self.user_id,
                                       function="GET REMINDER") + reminder_info + '}}'
            self.logger.info(response)
            return response

        # IF WE SEND A WRONG QUERY, WE SEND THE INFORMATION LIKE THIS
        else:
            user_id = parsed_string["user_id"]
            response = self.bot_parser(user_id=user_id,
                                       function="ERROR QUERY") + '"content" : "The query ' + instruction + ' is not on the query database"}}'
            self.logger.info(response)
            return response

    # METHOD USED TO PARSE ALL THE INFORMATION SENT TO THE CLIENT.PY (JSON)
    def bot_parser(self, user_id, function):
        return """{"user_id": """ + str(user_id) + ', "function": "' + function + '", "parameters": {'

    # METHOD USED TO ACTUALIZE THE TABLE OF REMINDERS EVERY DAY! ((((YET TO BE DONE PROPERLY!!!!))))
    def actualize_daily_table(self, user_id=None):
        if user_id:
            today = datetime.date.today().strftime("%Y-%m-%d")
            reminder_info = self.checker.get_reminders(user_id, today)
            response = self.bot_parser(self.user_id, "DAILY REMINDER") + '"reminder_info" : "' + reminder_info + '"}}'
            self.logger.info(response)
            return response
        else:
            today = datetime.date.today().strftime("%Y-%m-%d")
            reminder_info = self.checker.get_reminders_all(today)
            response = self.bot_parser("ALL", "DAILY REMINDER") + '"reminder_info" : "' + reminder_info + '"}}'
            self.logger.info(response)
            return response
