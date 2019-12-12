
def newmedicine_tostring( quantity, expiration_date, cn, medicine_name, language):
	retu = 'ERROR'
	if language =='esp':
		retu= 'Has introducido un nuevo medicamento: '+medicine_name+'cuyo CN es '+cn+'. La cantidad de comprimidos es de '+quantity+' y se caduca el dia '+expiration_date+ '.'
	else:
		retu = 'You have introduced a new medicine: '+medicine+'its NC is '+cn+'. There are '+quantity+' pills, its expiration date is '+expiration_date

	return retu


def prescription_tostring( cn, quantity, frequency, end_date, medicine_name, language):
	retu = 'ERROR'
	if language =='esp':
		retu= 'Has introducido una nuevo tratamiento de '+medicine_name+'cuyo CN es '+cn+'. Tomas '+quantity+' pastillas cada '+frequency+ ' horas. El tratamiento acaba el día.'+end_date+'.'
	else:
		retu= 'You have introduced a new '+medicine_name+' treatmne,t its NC is '+cn+'. You must take '+quantity+' pills every '+frequency+ ' hours. The treatment ends the '+end_date+'.'
	return retu

def calendat_tostring(date, dicc):
	retu = 'ERROR'
	if language =='esp':
		retu = 'Para el día '+date+' debes tomar los siguientes medicamentos :\n'
		for med, hours in dicc.items():
			retu+= med+': '
			for hour in hours:
				retu += hour+ ','

	else:
		retu = 'On the '+date+' you must take the following medicnes :\n'
		for med, hours in dicc.items():
			retu+= med+': '
			for hour in hours:
				retu += hour+ ','
		
	return retu

def journey_tostring(departure, arrival, dicc):
	retu = 'ERROR'
	if language =='esp':
		retu = 'Para tu viaje que empieza el día '+depature+ ' y acaba el día '+arrival+', necesitarás los siguientes medicamentos: '
		for med, quantity in dicc.items():
			quantity+ 'pastillas de' + medicine +'\n'

	else:
		retu = 'For your journey that starts on the '+depature+ ' and ends the '+arrival+', you will need ther following medicines: '
		for med, quantity in dicc.items():
			quantity+ 'pills of' + medicine +'\n'
	return retu	