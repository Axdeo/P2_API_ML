import joblib
import json

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

# todo lib au dessus à rajouter dans requirement.txt puis dans le dockerfile
# todo : rajouter la documentation et la gestion des exceptions
models=['LogisticRegression',
                  'KNN',
                  'SVR'
                  ]

model_logistic = joblib.load("model_logistic.joblib")
model_knn = joblib.load("model_knn.joblib")
model_linear = joblib.load("model_linear.joblib")

# liste des tags utilisée pour swagger
tags=[  {'name': 'home', 'description': 'basic functions'},
        {'name': 'predictions', 'description': 'Predictions with KNN, Logistic Regression and Linear SVC models'},
        {'name':'performances', 'description':'models performances requests'}
     ]


# instanciation de l'API
app = FastAPI (title='API Churn', description='API requests prediction of churn',
               version = '1.0.1', openapi_tags=tags
               )

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


def get_predictions(customer , model): 
    # on formate les données sous forme de dataframe
    data = pd.DataFrame([customer.dict()])
    # on ordonne les features pour avoir le meme ordre que les données qui ont entrainées les modèle
    # cet ordre a été sauvegardé sans features.json
    data = data[features]

    if model == 'KNN':
      prediction = model_knn.predict(data)[0]
      probability = model_knn.predict_proba(data)
    elif model == 'SVR':
      # note karine : pour SVR il va falloir enrigistrer le scaler dans un joblig et scaler les données
      prediction = model_linear.predict(data)[0]
      probability = model_linear.predict_proba(data)  # KO pour LinearSVC, la methode n'existe pas. trouver la methode correspondante
    elif model == 'LogisticRegression':
      prediction = model_logistic.predict(data)[0]
      probability = model_logistic.predict_proba(data)
      
    return  {'prediction' : int(prediction),
             'probability' : str(round(probability[0][0]*100,2)) + "%"
             }      

def get_performances(model): 
  #TODO: recup via les joblib des perfs
  pass

# définitions des différentes routes
# TODO : rajouter l'authentification sur toutes les routes

# Route / : Accueil.
@app.get('/', name='Welcome', tags=['home'])
def get_index():
   """return greetings
   """
   return {'greetings':"Welcome in the API churn's prediction - you must have an account to interogate the API"}

# Route /status : Vérifier que l'API est bien fonctionnelle.
@app.get('/status', name="Connexion test", tags=['home'])
def get_status():
    # TODO : authentification
    return 1
  
# Route /models : Renvoi les modèles étudiés et disponibles
@app.get('/models', name ='Models')
def get_models():
    """ return all the models that you can request"""
    return {'models':models
            }
# note karine : transformé de get en post (on ne peut pas envoyer un body à un get)
@app.post('/models/{model_name}/prediction', tags=['predictions'])
def post_model_prediction( c: Customer, model_name: str ):
    if model_name not in models:
        raise HTTPException(status_code=404,
                            detail='This model is not available, see "/models" for  more informations')
    else:
        return get_predictions(c,model_name)

# note karine : transformé de get en post (on ne peut pas envoyer un body à un get)
@app.post('/models/{model_name}/performances', tags=['performances'])
def post_model_performance(model_name: str):
    if model_name not in models:
        raise HTTPException(status_code=404,
                            detail='This model is not available, see "/models" for  more informations')
    else:
        return get_performances(model_name)
    
    


