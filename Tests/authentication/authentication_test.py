# -*- coding: utf-8 -*-
import os
import requests

# définition de l'adresse de l'API
api_address = 'api_churn_container' #variable environnement IP du container de l'api
# port de l'API
api_port = 8000

# requête
axel_r = requests.get(

    url='http://{address}:{port}/status'.format(address=api_address, port=api_port),
    auth=('axel','axdeo')
)

karine_r = requests.get(
    url='http://{address}:{port}/status'.format(address=api_address, port=api_port),
    auth=('karine','kparra')
)

roger_r = requests.get(
    url='http://{address}:{port}/status'.format(address=api_address, port=api_port),
    auth=('roger','banane')
)


output = '''
============================
    Authentication test
============================

        ===========
           KARINE
        ===========
        
request done at "/permissions"
| username="karine"
| password="kparra"

expected status result = 200
actual status result = {karine_status_code}

        ===========
           AXEL
        ===========
        
request done at "/permissions"
| username="axel"
| password="axdeo"

expected status result = 200
actual status result = {axel_status_code}
    
        ===========
           ROGER
        ===========
        
request done at "/permissions"
| username="roger"
| password="banane"

expected status result = 401
actual status result = {roger_status_code}

==>  {test_status}

'''

# statut de la requête
karine_status_code = karine_r.status_code
axel_status_code = axel_r.status_code
roger_status_code = roger_r.status_code

# affichage des résultats
if karine_status_code == 200 and axel_status_code == 200 and roger_status_code == 401:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(karine_status_code = karine_status_code, axel_status_code = axel_status_code,\
                    roger_status_code=roger_status_code,\
                    test_status=test_status))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a') as file:
        print("dans la boucle d'ecriture fichier log\n")
        file.write(output.format(karine_status_code = karine_status_code, axel_status_code = axel_status_code,\
                    roger_status_code=roger_status_code,\
                    test_status=test_status))
