import joblib
import json
import pandas as pd
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

models=['LogisticRegression',
        'KNN']

model_logistic = joblib.load("model_logistic.joblib")
model_knn = joblib.load("model_knn.joblib")

# liste des tags utilisée pour affichage dans swagger
tags=[  {'name': 'home', 'description': 'basic functions'},
        {'name': 'predictions', 'description': 'Predictions with KNN and Logistic Regression'}
        ]


# liste des erreurs pour affichage dans swagger
errors = {200: {"description": "OK"},
          400: {"description": "Wrong argument type"},
          401: {"description": "Incorrect email or password"},
          404: {"description": "Model not available"}
          }


#Sécurisation de l'API
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_pwd'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# liste des users habilités à se connecter à l'application.
users = {"alice": {"type":"user",
                   "username": "alice",
                   "hashed_pwd": pwd_context.hash("wonderland")
                   },
         "bob": {"type":"user",
                 "username": "bob",
                 "hashed_pwd": pwd_context.hash("builder")
                 },
         "clementine": {"type":"user",
                        "username": "clementine",
                        "hashed_pwd": pwd_context.hash("mandarine")
                        },
         "axel": {"type":"admin",
                  "username": "axel",
                  "hashed_pwd": pwd_context.hash("axdeo")
                  },
         "karine": {"type":"admin",
                    "username": "karine",
                    "hashed_pwd": pwd_context.hash("kparra")
                    }
         }

# instanciation de l'API
app = FastAPI (title='API Churn', description='API requests prediction of churn',
               version = '1.0.1', openapi_tags=tags
               )


with open("features.json","r") as f:
    features = json.load(f)


class Customer(BaseModel):
    """
    Customer's datas : \n
    - gender : 1 = Male, 0 = Female \n
    - SeniorCitizen     : 1/0 \n
    - Partner           : 1 = Yes, 0 = No \n
    - Dependents        : 1 = Yes, 0 = No \n
    - Tenure (months) \n
    - PhoneService      : 1 = Yes, 0 = No \n
    - MultipleLines     : 1 = Yes, 0 = No, -1 = No phone service \n
    - InternetService   : 0 = No, 1 = DSL, 2 = Fiber optic \n
    - OnlineSecurity    : 1 = Yes, 0 = No, -1 = No internet service \n
    - OnlineBackup      : 1 = Yes, 0 = No, -1 = No internet service \n
    - DeviceProtection  : 1 = Yes, 0 = No, -1 = No internet service \n
    - TechSupport       : 1 = Yes, 0 = No, -1 = No internet service \n
    - StreamingTV       : 1 = Yes, 0 = No, -1 = No internet service \n
    - StreamingMovies   : 1 = Yes, 0 = No, -1 = No internet service \n
    - Contract          : 24 = Two year, 12 = One year, 1 = Month-to-month \n
    - PaperlessBilling  : 1 = Yes, 0 = No \n
    - PaymentMethod     : 1 = 'Electronic check', 2 = 'Mailed check', 3 = 'Bank transfer (automatic)', 4 = 'Credit card (automatic)' \n
    - MonthlyCharges($) \n
    - TotalCharges($) \n
    """
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
    """
    Gets the prediction for un customer and a model.
    Parameters :
    - customer : Customer object
    - model : model name, in 'KNN' and 'LogisticRegression'
    Returns :
    - prediction : 1 = the customer may unsubscribe, 0 = he may not
    - probability : probability that the model is right
    """
    # on formate les données sous forme de dataframe
    data = pd.DataFrame([customer.dict()])
    # on ordonne les features pour avoir le meme ordre que les données qui ont entrainées les modèle
    # cet ordre a été sauvegardé sans features.json
    data = data[features]

    if model == 'KNN':
        prediction = model_knn.predict(data)[0]
        probability = model_knn.predict_proba(data)
    elif model == 'LogisticRegression':
        prediction = model_logistic.predict(data)[0]
        probability = model_logistic.predict_proba(data)

    return  {'prediction' : int(prediction),
             'probability' : str(round(probability[0][0]*100,2)) + "%"
             }


# définitions des différentes routes

# Route / : Accueil.
@app.get('/', name='Welcome', tags=['home'], responses=errors)
def get_index():
    """
    Returns greetings
    """
    return {'greetings':"Welcome in the API churn's prediction - you must have an account to interogate the API"}


# Route /models : Renvoie les modèles étudiés et disponibles
@app.get('/models', name ='Models', tags=['predictions'])
def get_models():
    """
    Returns all the models that you can request
    """
    return {'models':models
            }


# Route /status : Vérifier que l'API est bien fonctionnelle.
@app.get('/status', name="Connexion test", tags=['home'], responses=errors)
def get_status( username: str = Depends(get_current_user)):
    """
    Tests if the API is available \n
    Tests if the user has the proper authorizations to access the API : only administrators can use it
    """
    if users[username]['type']== "admin" :
        return {'API Status':'API is running normally'}
    else :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you don't have the authorization here, you must be admin")


@app.post('/models/{model_name}/prediction', tags=['predictions'], responses=errors)
def post_model_prediction( c: Customer, model_name: str , username: str = Depends(get_current_user)):
    """
    Tests if the user has the proper authorizations to access the API \n
    Gets prediction for un customer and a model. \n
    Parameters : \n
    - customer : Customer object \n
    - model : model name, in 'KNN' and 'LogisticRegression' \n
    Returns : \n
    - prediction : 1 = the customer may unsubscribe, 0 = he may not \n
    - probability : probability that the model is right \n
    """
    try:
        if model_name not in models:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='This model is not available, see "/models" for  more informations')
        elif  not users[username]['type']== "admin" and not not users[username]['type']== "user" :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="you don't have the authorization here")
        else:
            return get_predictions(c,model_name)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Unknown Index')
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Bad Type')
