import joblib
import json

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

# todo lib au dessus à rajouter dans requirement.txt puis dans le dockerfile

model_logistic = joblib.load("model_logistic.joblib")
model_knn = joblib.load("model_knn.joblib")
model_linear = joblib.load("model_linear.joblib")

# liste des tags utilisée pour swagger
tags=[  {'name': 'home', 'description': 'basic functions'},
        {'name': 'predictions', 'description': 'Predictions with KNN, Logistic Regression and Linear SVC models'}]

# instanciation de l'API
api = FastAPI(title = "API Churn",
              openapi_tags = tags)

# liste des users habilités à se connecter à l'application.
users = {"alice": "wonderland",
         "bob": "builder",
         "clementine": "mandarine"}

# TODO définition du modele de données à transférer à l'API (NB : utiliser un POST pour pouvoir l'envoyer dans le body
with open("features.json","r") as f:
    features = json.load(f)

class Customer(BaseModel):
    # todo cf features : meme champs. Est-ce qu'on supprime des champs pour alléger l'API?
    gender : int = 0
    SeniorCitizen : int = 0
    Partner : int = 0
    Dependents : int = 0
    tenure : int = 0
    PhoneService : int = 0
    MultipleLines : int = 0
    OnlineSecurity : int = 0
    OnlineBackup : int = 0
    DeviceProtection : int = 0
    TechSupport : int = 0
    StreamingTV : int = 0
    StreamingMovies : int = 0
    Contract : int = 0
    PaperlessBilling : int = 0
    MonthlyCharges : float = 0
    TotalCharges : float = 0
    PaymentMethod_Bank_transfer : int = 0
    PaymentMethod_Credit_card : int = 0
    PaymentMethod_Electronic_check : int = 0
    PaymentMethod_Mailed_check : int = 0
    InternetService_DSL : int = 0
    InternetService_Fiber_optic : int = 0
    InternetService_No : int = 0

# définitions des différentes routes
# TODO : rajouter l'authentification sur toutes les routes
# Route /status : Vérifier que l'API est bien fonctionnelle.
@api.get('/status', name="Connexion test", tags=['home'])
def get_status():
    # TODO : authentification
    return 1

# Route /prediction/KNN : Prediction avec le modele KNN. Renvoyer la prediction et la probabilité (cf masterclass)
@api.post('/prediction/knn', name='KNN Prediction', tags = ['predictions'])
def post_prediction_knn(customer : Customer):

    print(features)

    # on formate les données sous forme de dataframe
    data = pd.DataFrame([customer.dict()])
    # on ordonne les features pour avoir le meme ordre que les données qui ont entrainées les modèle
    # cet ordre a été sauvegardé sans features.json
    data = data[features]

    prediction = model_knn.predict(data)[0]
    probability = model_knn.predict_proba(data)
    return  {'prediction' : int(prediction),
             'probability' : str(round(probability[0][0]*100,2)) + "%"
             }


# Route /prediction/logistic : Prediction avec le modele Logistic Regression
@api.post('/prediction/logictic', name='Logistic Regression Prediction', tags = ['predictions'])
def post_prediction_logistic(customer : Customer):
    # todo sur la base de knn quand il sera finalisé
    return


# Route /prediction/logistic : Prediction avec le modele Logistic Regression
@api.post('/prediction/svc', name='Linear SVC Prediction', tags = ['predictions'])
def post_prediction_svc(customer : Customer):
    # todo sur la base de knn quand il sera finalisé
    return

