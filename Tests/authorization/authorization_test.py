# -*- coding: utf-8 -*-

import os
import requests

# définition de l'adresse de l'API
api_address = 'api_Churn_container' #variable environnement IP du container de l'api
# port de l'API
api_port = 8000

# requête
karine_r = requests.get(
    url='http://{address}:{port}/status'.format(address=api_address, port=api_port),
    auth=('karine','kparra')
)

clem_r = requests.get(
    url='http://{address}:{port}/status'.format(address=api_address, port=api_port),
    auth=('clementine','mandarine')
)




output = '''
============================
    Autorization test
============================

        ===========
           KARINE
        ===========
        
request done at "/status"
| username="karine"
| password="kparra"

  expected status result = 200
  actual status result = {karine_status_code} 
    
        ===========
         CLEMENTINE
        ===========
        
request done at "/status"
| username="clementine"
| password="mandarine"

  expected status result = 401
  actual status result = {clem_status_code}
    

==>  {test_status}

'''

# statut de la requête
karine_status_code = karine_r.status_code
clem_status_code = clem_r.status_code


# affichage des résultats
if karine_status_code == 200 and clem_status_code == 401 : 
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(karine_status_code = karine_status_code, clem_status_code = clem_status_code,
                    test_status=test_status))

# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a') as file:
        file.write(output.format(karine_status_code = karine_status_code, clem_status_code = clem_status_code,\
                            test_status=test_status))