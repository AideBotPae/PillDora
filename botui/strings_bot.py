# !/usr/bin/env
# -*- coding: utf-8 -*-


#OJO MARKUPS
INTR_PRESCRIPTION_MSSGS = {
    'eng': ["What is the medicine's name (CN)?\nYou can also send me a photo of the package!",
                           "How many pills do you have to take each time?",
                           "How often do you take your pill (in hours)?",
                           "Which day does treatment end?"],
    'esp': ['¿Cuál es el nombre del medicamento? (CN)\nPuedes enviarme una foto del paquete, si lo prefieres!',
            '¿Cúantas pastillas ingieres en cada toma?',
            '¿Cada cuánto tiempo tomas la pastilla?(en horas)',
            '¿Que día acaba el tratamiento?']
}

INTR_MEDICINE_MSSGS ={
    'eng' :["What is the medicine's name (CN)?\nYou can also send me a photo of the package!",
            "How many pills are contained in the box?",
            "When does the medicine expire?"],
    'esp' :['¿Cuál es el nombre del medicamento? (CN)\nPuedes enviarme una foto del paquete, si lo prefieres!',
            '¿Cúantas pastillas contiene cada caja?',
            '¿Qué día caduca el medicamento?']
}

reply_keyboard ={

'eng' : [
    [u'New Prescription \U0001F4C3', u'New Medicine \U0001F48A'],
    [u'Current Treatments \U0001F3E5', u'Delete reminder \U0001F514'],
    [u'History \U0001F4D6', u'Inventory \U00002696', u'Information \U0001F4AC'],
    [u'Journey \U0000270D', u'Calendar \U0001F4C6',  u'Exit \U0001F6AA']] ,
'esp':[ [u'Nueva receta \U0001F4C3', u'Nuevo medicamento \U0001F48A'],
    [u'Tratamientos actuales \U0001F3E5', u'Eliminar recordatorio \U0001F514'],
    [u'Historial \U0001F4D6', u'Inventorio \U00002696', u'Información \U0001F4AC'],
    [u'Viaje \U0000270D', u'Calendario \U0001F4C6',  u'Salir \U0001F6AA']]
}

yes_no_reply_keyboard = {
  'eng':  [['YES', 'NO']],
    'esp': [['SÍ', 'NO']]
}

taken_pill_keyboard = {'eng': [['TAKEN','POSTPONE']],
                       'esp' : [['TOMADA', 'POSPONER']]}

loc_button = {
    'eng': 'KeyboardButton(text="Send Location", request_location=True)',
    'esp': 'KeyboardButton(text="Enviar ubicación", request_location=True)'
}

location_keyboard = {
    'eng': [[loc_button['eng'], "Don't Send Location"]],
    'esp': [[loc_button['esp'], "No enviar ubicación"]]

}

#Usar eval() o to_do '', ALOMEJOR HAY QUE INCLUIR MENSAJE DONDE PREGUNTAR POR IDIOMA AQUI
STR_START_WELCOME =  {
    'eng': "'Welcome ' + name + ' ! My name is AideBot'",
    'esp': "'Bienvenido '+ name+ ' ! Mi nombre es AideBot'"
}

STR_START_ENTERPASSWORD = {
    'eng': "Enter your password in order to get Assistance: ",
    'esp': "Introduce tu contraseña para que pueda ayudarte:"
}

STR_START_CREATEUSER = {
    'eng' : "Welcome to the HealthCare Assistant AideBot!\nEnter new password for creating your account:",
    'esp': "Bienvenido a Aidebot, tu asistente médico\nIntroduce una nueva contraseña para crear tu cuenta:"
}


STR_INTR_PWD_WRONGPASS = {
    'eng': "Wrong Password. Enter correct password again:",
    'esp': "Contraseña incorrecta. Introduce la contraseña de nuevo"
}

STR_INTR_PWD_WELCOME = {
'eng': "'Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?',reply_markup=markup",
'esp': "'Bienvenido ' self.get_name(update.message.from_user) + '. ¿Cómo te puedo ayudar?',reply_markup=markup"
}


STR_NEW_USER_VALIDPASS= {
    'eng': 'Alright. Now you are ready! How can I help you?',
    'esp': 'Perfecto, ya estamos listos! ¿Cómo te puedo ayudar?, reply_markup=markup'
}
STR_NEW_USER_NOTVALIDPASS = {
    'eng': "Not a Valid Password. Enter Password with 6 to 12 characters and minimum 3 of these types of characters: uppercase, lowercase, number and $, # or @",
    'esp': "No es una contraseña válida. Introduce una contraseña de 6 a 12 carácteres que contengo al menos 3 de estos tipos: minúsuclas, mayúsculas, numeros y $, # o @"
}

# STR_NEW_USER_WELCOME = {
#     'eng': "'Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?', reply_markup = markup",
#     'esp': "'Bienvenido '+self.get_name(update.message.from_user) + '. ¿Cómo te puedo ayudar?', reply_markup = markup"
# }

STR_MANAGE_RESPONSE_ALREADYPRESCRIPT1 = {
'eng' : "There is already a prescription of same med that has not expire yet. Different frequencies.\nIn order to introduce this new prescription, please first delete the other reminder.",
'esp' : "Ya existe una receta del mismo medicamento que aun no ha acabado. Frecuencias diferentes. \n Para introducir esta nueva receta, elimina la otra con la opcion eliminar recordatorio. "

}

STR_MANAGE_RESPONSE_ALREADYPRESCRIPT2 = {
'eng' : "Medicine already in the database with same frequencies. NO PROBLEM",
'esp' : "Ya existe una receta del mismo medicamento con la misma frecuencia. NINGÚN PROBLEMA"

}

STR_MANAGE_RESPONSE_EMPTYINVENTORY = {
    'eng': "In your inventory we do not have any of this medicine. Please 'Introduce Medicine' after getting the med",
    'esp': "En el inventorio no tenemos este medicamento. Por favor, usa la opcion 'Introduce Medicine' cuando la hayas probado "
}

STR_MANAGE_RESPONSE_FULLNIVENTORY = {
    'eng': "In your inventory there is enough of this medicine for this whole treatment. No need to buy it.",
    'esp': "En el inventorio hay suficientes pastillas para todo el tratamiento. No hace falta comprar "
}

STR_MANAGE_RESPONSE_BUYINVENTORY = {
    'eng': "In your inventory there is some of this medicine but not enough for the whole treatment. Need to buy it.",
    'esp': "En el inventorio queda algo, pero no suficiente para todo el tratamiento. Hay que comprar. "
}

STR_MANAGE_RESPONSE_DELETEREMINDER = {
    'eng' : "Medicine introduced did not exist in your current Treatment.",
    'esp' : "El medicamento introducido no aperace en tus Tratamientos Actuales"
}

STR_MANAGE_RESPONSE_JOURNEY = {
    'eng': "'Medicines to take during journey:\n' + response['parameters']['journey_info']",
    'esp': "'Medicamentos a llevar durante el viaje:\n + response['parameters']['journey_info']"
}

STR_MANAGERESPONSE_TAKEPILL1 = {
    'eng': "chat_id=user_id, text='Pills taken correctly introduced in the history'",
    'esp': "chat_id=user_id, text= 'Pastillas introducidas correctamente en el historial"
}

STR_MANAGE_RESPONSE_TAKEPILL0 = {
    'eng': "chat_id=user_id, text='Pills taken correctly introduced in the history. However, there is no record of these pills in the inventory. Please introduce them'",
    'esp': "chat_id=user_id, text='Pastillas tomadas introduciadas correctamente en el historial. Sin embargo, no hay registro de estas en el inventorio. Porfavor introducelas usando la función Introducir Medicamento'"
}

STR_MANAGE_RESPONSE_END = {
    'eng': "'Is there any other way I can help you?', reply_markup=markup",
    'esp': "'¿Puedo ayudarte de alguna otra manera?', reply_markup= markup"
}


STR_SEND_NEW_PRESCRIPTION_ERROR = {
    'eng': "An error has occurred, please repeat the photo or manually introduce the CN.",
    'esp': "Ha ocurrido un error, por favor repite la foto o introduce el CN manualmente."

}

STR_SEND_NEW_PRESCRIPTION_ISCORRECT = {
    'eng': "chat_id=user_id, text='Is the medicine correctly introduced? ', reply_markup=yes_no_markup",
    'esp': "chat_id=user_id, text='¿Está introducida correctamente?, reply_markup=yes_no_markup"
}


STR_SHOW_PRESCRIPTION_MEDSTR = {
    'eng': "'You have to take *' + self.get_prescription(user_id)['QUANTITY'] + '* pills of medicine *' + cima.get_med_name(self.get_prescription(user_id)['NAME']).split(' ')[0] + '* each *' + self.get_prescription(user_id)['FREQUENCY'] + '* hours'",
    'esp': "'Debes tomar *' + self.get_prescription(user_id)['QUANTITY'] + '* pastillas del medicamento *' + cima.get_med_name(self.get_prescription(user_id)['NAME']).split(' ')[0] + '* cada *' + self.get_prescription(user_id)['FREQUENCY'] + '* horas'"
}

STR_SHOW_PRESCRIPTION_CHRONIC = {
    'eng': " *chronically*!",
    'esp': " *crónicamente*!"
}

STR_SHOW_PRESCRIPTION_UNTIL = {
    'eng': "'until the end date of *'+ date_str+'* !'",
    'esp': "'hasta el día *' + date_str+'* !'"
}

STR_SEND_NEW_MEDICINE_ERROR =  {
    'eng': "An error has occurred, please repeat the photo or manually introduce the CN.",
    'esp': "Ha ocurrido un error, por favor repite la foto o introduce el CN manualmente."

}

STR_SEND_NEW_MEDICINE_ISCORRECT = {
    'eng': "chat_id=user_id, text='Is the medicine correctly introduced? ', reply_markup=yes_no_markup",
    'esp': "chat_id=user_id, text='¿Está introducida correctamente?, reply_markup=yes_no_markup"
}

STR_SHOW_MEDICINE_INITIALSTRING = {
    'eng': "'Introducing *' + self.get_medicine(user_id)['QUANTITY'] + '* pills of medicine *' + cima.get_med_name(self.get_medicine(user_id)['NAME']).split(' ')[0] + '* which '",
    'esp': "'Introduciendo *' + self.get_medicine(user_id)['QUANTITY'] + '* pastillas del medicamento *' + cima.get_med_name(self.get_medicine(user_id)['NAME']).split(' ')[0] + '* que '"
}

STR_SHOW_MEDICINE_NOCADUCA = {
    'eng': "*never expire*!",
    'esp':"*no caducan nunca*!"
}

STR_SHOW_MEDICINE_ELDIA={
    'eng': "' expire on day *'+ date_str + '* !'",
    'esp': "' caducan el día *'+ date_str + '* !'"
}

STR_SEND_NEW_PILL_ERROR = STR_SEND_NEW_MEDICINE_ERROR

STR_SEND_NEW_PILL_ISTAKENCORRECTLY = {
    'eng': "chat_id=user_id, text='Is the pill taken correctly introduced? ', reply_markup=yes_no_markup".
    'esp': "chat_id=user_id, text='¿Se ha introducido correctamente la pastilla tomada? ', reply_markup=yes_no_markup"
}

STR_SHOW_PILL= {
    'eng': "'You are taking *' + self.get_pill(user_id)['QUANTITY'] + '* pills of medicine *' + cima.get_med_name(self.get_pill(user_id)['NAME']).split(' ')[0] + '* !'",
    'esp': "'Estás tomando *' + self.get_pill(user_id)['QUANTITY'] + '* pastillas de *' + cima.get_med_name(self.get_pill(user_id)['NAME']).split(' ')[0] + '* !'"
}

STR_CHECK_PILL = {
'eng': "chat_id=user_id,text='Please introduce photo of the pills you proceed to take. If you can not do so, click on NO',reply_markup=yes_no_markup",
'esp': "chat_id=user_id,text='Por favor, introduce una foto de las pastillas que te vas a tomar. Si no puedes realizarla ahora, apreta NO',reply_markup=yes_no_markup"
}

STR_SHOW_INFOABOUT_ERROR = STR_SEND_NEW_MEDICINE_ERROR


STR_SHOW_INFOABOUT_HELPEND= STR_MANAGE_RESPONSE_END