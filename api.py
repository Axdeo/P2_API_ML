# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 18:19:53 2022

@author: axeld
"""

from fastapi import FastAPI ,HTTPException 
from joblib import load
from pydantic import BaseModel
from typing import Optional
import asyncio


models=['LinearRegression',
                  'KNN',
                  'SVR'
                  ]

api = FastAPI ( title='API Churn' , description='API requests prediction of churn',
               version = '1.0.1', openapi_tags=[{'name':'predictions', 'description':'prediction requests'},
                                                {'name':'performances', 'description':'models performances requests'}
                                                ]
               )

class user_features(BaseModel):
    #à remplir
    return

@api.get('/',name='Welcome')
def get_index():
   """return greetings
   """
   return {'greetings':"Welcome in the API churn's prediction - you must have an account to interogate the API"}

@api.get('/models', name = 'Models')
def get_models():
    """ return all the models that you can request"""
    return {'models':models
            }

@api.get('models/{model_name}/performances', tags=['performances'])
def get_model_performance(m = model_name):
    #à remplir
    # test et ajout HTTPException si model_name pas dans models
    return
    
@api.get('models/{model_name}/prediction', tags=['predictions'])
def get_model_prediction( user = user_features, m = model_name):
    #à remplir
    # test et ajout HTTPException si model_name pas dans models
    return