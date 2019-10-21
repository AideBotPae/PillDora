from Server.database import DBMethods
import json
import datetime
import logging
import requests


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
        # INTRODUCING A NEW MEDICINE
        elif instruction == "INTRODUCE RECEIPT":
            user_id = parsed_string["user_id"]
            national_code = parsed_string["parameters"]["NAME"]
            is_there = self.checker.check_receipt(user_id=user_id, cn=national_code)
            # CHECKING IF THE MEDICINE IS ALREADY ON THE DATABASE
            if not is_there:
                # IF WE ARE HERE, IT MEANS THAT THE MEDICINE WASN'T ON THE DATABASE, SO WE INPUT ALL THE DATA
                self.checker.introd_receipt(user_id=user_id, query_parsed=parsed_string["parameters"],
                                            date=datetime.date.today().strftime("%Y-%m-%d"))
                response = self.bot_parser(user_id=user_id, function="INTRODUCE MEDICINE") + """ "Code": "0"}}"""
                #     WE ALSO ACTUALIZE THE REMINDERS OF THAT DAY IN CASE WE HAVE TO TAKE ANY PILL OF THAT MEDICINE
                # self.actualize_daily_table(user_id)
                #     THIS SHOWS INFORMATION ON THE TERMINAL THAT RUNS THIS CLIENT
                #     IT IS USED TO SHOW THE INFORMATION THAT WE ARE SENDING
                self.logger.info(response)
                return response
            elif not self.checker.check_medicine_frequency(user_id=user_id, cn=national_code,
                                                           freq=parsed_string["parameters"]["FREQUENCY"]):
                # IF WE ARE HERE, THE MEDICINE IS ALREADY ON THE DATABASE, WE CHECK FIRST IF THE FREQUENCIES CONCUR,
                # IF THEY NOT, IT IS A PROBLEM!
                response = self.bot_parser(user_id=user_id,
                                           function="INTRODUCE MEDICINE") + '"Code": "1" , "freq_database" : "' + str(
                    self.checker.get_medicine_frequency(user_id=user_id,
                                                        cn=national_code)) + '", "freq_introduced" : "' + str(
                    parsed_string["parameters"]["FREQUENCY"]) + '"}}'
                self.logger.info(response)
                return response

            else:
                # IF WE ARE HERE, THE MEDICINE IS ALREADY ON THE DATABASE AND THE FREQUENCIES MATCH, SO WE INCREASE
                # THE QUANTITY OF PILLS THAT WE HAVE TO TAKE
                # (((((((AQUI EN EL FUTURO TOCAREMOS EL INVENTARIO)))))))
                response = self.bot_parser(user_id=user_id, function=
                "INTRODUCE MEDICINE") + '"Code" : "2"}}'
                self.logger.info(response)
                return response
        # THE USER WANTS TO PLAN A JOURNEY
        elif instruction == "INTRODUCE MEDICINE":
            user_id = parsed_string["user_id"]
            cn = parsed_string["parameters"]["NAME"]
            medicine_name = self.resolve_name(cn)
            measure = self.resolve_measure(cn)
            introduced = self.checker.intr_inventory(user_id=user_id, query_parsed=parsed_string["parameters"],
                                            medicine_name=medicine_name, measure=measure)
            response = self.bot_parser(user_id=user_id, function="INTRODUCE RECEIPT") + '"boolean" : '+str(introduced)+'}}'
            return response

        elif instruction == "HISTORY":
            user_id = parsed_string["user_id"]
            data = self.checker.get_history(self, user_id=user_id)
            response = self.bot_parser(user_id=user_id, function="INTRODUCE RECEIPT") + '"history" : ' + data + '}}'
            return response
        elif instruction == "JOURNEY":
            # WE OUTPUT A SERIES OF ACTIONS TO BE DONE FROM A LEAVING DATE TO THE DEPARTURE ONE
            [user_id, begin, end] = [parsed_string["user_id"], parsed_string["parameters"]["departure_date"],
                                     parsed_string["parameters"]["arrival_date"]]
            # IF THE BEGINNING DAT AND THE END DATE CONFLICTS, THE METHOD WILL RETURN A NULL CALENDAR OUTPUT
            calendar_output = self.checker.get_reminders(user_id=user_id, date=begin, to_date=end)
            if calendar_output is not None:
                journey_info = "Quantity of meds to take:\\n"
                for output in list(calendar_output.keys()):
                    journey_info += "\\t-> " + str(output) + " : " + str(calendar_output[output]) + "\\n"
            #   (((RIGHT NOW, THE MEDICINES ON THE JOURNEY WILL HAVE A NATIONAL CODE, ON THE FUTURE THEY WILL
            #                               GO BY THE MEDICINE NAME)))
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
                    journey_info += "\\t-> " + str(output[0]) + " : " + str(output[1]) + "\\n"
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
        # THE USER ASKS FOR THE HISTORY OF PILLS TAKEN
        elif instruction == "CURRENT TREATMENT":
            user_id = parsed_string["parameters"]["user_id"]
            history = self.checker.get_current_treatments(user_id=user_id)
            if history is not None:
                history_info = "History of all Meds currently being taken :\\n"
                for output in history:
                    history_info += "\\t-> Taking  " + str(output[0]) + " until the date of " + str(output[1]) + "\\n"
            response = self.bot_parser(user_id=user_id,
                                       function="HISTORY") + '"reminder_info" : "' + history_info + '"}}'
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
        elif instruction == "SHOW INFO ABOUT":
            user_id = parsed_string["user_id"]
            cn = parsed_string["parameters"]["NAME"]
            information = self.resolve_medicine_info(cn)
            response = self.bot_parser(user_id=user_id, function="INTRODUCE RECEIPT") + '"information" : ' + information + '}}'
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

    def resolve_medicine_info(self, cn):
        str_requested =  requests.get( url = "https://cima.aemps.es/cima/rest/medicamento?cn= "+ cn)
        parsed_string = json.loads(str_requested)
        data = parsed_string[""]
        return data

    def resolve_name(self, cn):
        str_requested = requests.get(url="https://cima.aemps.es/cima/rest/medicamento?cn= " + cn)
        parsed_string = json.loads(str_requested)
        data = parsed_string[""]
        return data


    def resolve_measure(self, cn):
        str_requested = requests.get(url="https://cima.aemps.es/cima/rest/medicamento?cn= " + cn)
        parsed_string = json.loads(str_requested)
        data = parsed_string["potato"]
        return data