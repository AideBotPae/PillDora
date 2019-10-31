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


#Usar eval() o to_do '', ALOMEJOR HAY QUE INCLUIR MENSAJE DONDE PREGUNTAR POR IDIOMA AQUI
STR_START_WELCOME =  {
    'eng': "Welcome " + name + " ! My name is AideBot",
    'esp': "Bienvenido "+ name+ " ! Mi nombre es AideBot"
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
'eng': 'Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?',reply_markup=markup,
'esp': 'Bienvenido ' self.get_name(update.message.from_user) + '. ¿Cómo te puedo ayudar?',reply_markup=markup
}


STR_NEW_USER_VALIDPASS= {
    'eng': 'Valid Password',
    'esp': 'Contraseña válida'
}

STR_NEW_USER_WELCOME = {
    'eng': "'Welcome ' + self.get_name(update.message.from_user) + '. How can I help you?', reply_markup = markup",
    'esp': "'Bienvenido '+self.get_name(update.message.from_user) + '. ¿Cómo te puedo ayudar?', reply_markup = markup"
}

STR_NEW