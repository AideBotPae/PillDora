import requests


r = requests.get(url = "https://cima.aemps.es/cima/rest/medicamento?cn=719556")
data= r.json()
print(data['presentaciones'][0]['nombre'])
