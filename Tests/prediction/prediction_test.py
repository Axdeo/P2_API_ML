# -*- coding: utf-8 -*-
import os
import requests

# définition de l'adresse de l'API
api_address = 'api_churn_container' #variable environnement IP du container de l'api
# port de l'API
api_port = 8000

client_churn = {
  "gender": 1,
  "SeniorCitizen": 1,
  "Partner": 0,
  "Dependents": 0,
  "tenure": 2,
  "PhoneService": 0,
  "MultipleLines": 0,
  "OnlineSecurity": 0,
  "OnlineBackup": 0,
  "DeviceProtection": 1,
  "TechSupport": 0,
  "StreamingTV": 1,
  "StreamingMovies": 1,
  "Contract": 1,
  "PaperlessBilling": 1,
  "MonthlyCharges": 150,
  "TotalCharges": 500,
  "PaymentMethod_Bank_transfer": 0,
  "PaymentMethod_Credit_card": 0,
  "PaymentMethod_Electronic_check": 0,
  "PaymentMethod_Mailed_check": 1,
  "InternetService_DSL": 1,
  "InternetService_Fiber_optic": 0,
  "InternetService_No": 0
}


client_nochurn = {
  "gender": 1,
  "SeniorCitizen": 0,
  "Partner": 1,
  "Dependents": 0,
  "tenure": 60,
  "PhoneService": 1,
  "MultipleLines": 0,
  "OnlineSecurity": 0,
  "OnlineBackup": 0,
  "DeviceProtection": 0,
  "TechSupport": 0,
  "StreamingTV": 1,
  "StreamingMovies": 1,
  "Contract": 24,
  "PaperlessBilling": 1,
  "MonthlyCharges": 40,
  "TotalCharges": 2400,
  "PaymentMethod_Bank_transfer": 0,
  "PaymentMethod_Credit_card": 0,
  "PaymentMethod_Electronic_check": 0,
  "PaymentMethod_Mailed_check": 1,
  "InternetService_DSL": 1,
  "InternetService_Fiber_optic": 0,
  "InternetService_No": 0
}



# requêtes
r_knn_c = requests.post(
    url='http://{address}:{port}/models/KNN/prediction'.format(address=api_address, port=api_port),
    auth=('karine','kparra'),
    json=client_churn
)

r_knn_nc = requests.post(
    url='http://{address}:{port}/models/KNN/prediction'.format(address=api_address, port=api_port),
    auth=('karine','kparra'),
    json=client_nochurn
)

r_log_c = requests.post(
    url='http://{address}:{port}/models/LogisticRegression/prediction'.format(address=api_address, port=api_port),
    auth=('karine','kparra'),
    json=client_churn
)

r_log_nc = requests.post(
    url='http://{address}:{port}/models/LogisticRegression/prediction'.format(address=api_address, port=api_port),
    auth=('karine','kparra'),
    json=client_nochurn
)

output = '''
============================
    Algorithms tests
============================

      =============
          KNN
      =============
      
request done at "models/KNN/prediction"
| username="karine"
| password="kparra"


    | client no churn

    expected status result = 200
    actual status result = {status_code_knn_nc}
    
    expected algorithm result : 0
    actual algorithm result : {result_knn_nc}


    | client churn

    expected status result = 200
    actual status result = {status_code_knn_c}
    
    expected algorithm result : 1
    actual algorithm result : {result_knn_c}
    
    

      =============
        LOG REG
      =============
      
request done at "models/LogisticRegression/prediction"
| username="karine"
| password="kparra"


    | client no churn

    expected status result = 200
    actual status result = {status_code_log_nc}
    
    expected algorithm result : 0
    actual algorithm result : {result_log_nc}


    | client churn

    expected status result = 200
    actual status result = {status_code_log_c}
    
    expected algorithm result : 1
    actual algorithm result : {result_log_c}

==>  {test_status}

'''

# statut de la requête
status_code_knn_c = r_knn_c.status_code
status_code_knn_nc = r_knn_nc.status_code
status_code_log_c = r_log_c.status_code
status_code_log_nc = r_log_nc.status_code

print(r_knn_c.json())
result_knn_c = r_knn_c.json()['prediction']
result_knn_nc = r_knn_nc.json()['prediction']
result_log_c = r_log_c.json()['prediction']
result_log_nc = r_log_nc.json()['prediction']


# affichage des résultats
if status_code_knn_c == 200 and status_code_knn_nc == 200 and status_code_log_c == 200 \
and status_code_log_nc == 200  and result_knn_c == 1 and result_knn_nc == 0 \
and result_log_c == 1 and result_log_nc == 0:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(test_status=test_status, status_code_knn_c=status_code_knn_c, status_code_knn_nc=status_code_knn_nc,\
                    status_code_log_c=status_code_log_c, status_code_log_nc = status_code_log_nc,\
                    result_knn_c=result_knn_c, result_knn_nc=result_knn_nc,\
                    result_log_c=result_log_c, result_log_nc=result_log_nc))


# impression dans un fichier
if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a') as file:
        file.write(output.format(test_status=test_status, status_code_knn_c=status_code_knn_c, status_code_knn_nc=status_code_knn_nc,\
                    status_code_log_c=status_code_log_c, status_code_log_nc = status_code_log_nc,\
                    result_knn_c=result_knn_c, result_knn_nc=result_knn_nc,\
                    result_log_c=result_log_c, result_log_nc=result_log_nc))
