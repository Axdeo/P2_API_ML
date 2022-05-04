# P2_API_ML
ML predictions of churn API - Formation project P2 DataScientest


## OBJECTIF:
L'objectif de ce projet est de déployer un modèle de Machine Learning.
Ce repo Github contient les fichiers suivants:
* le fichier source de l'API : main.py
* le Dockerfile de l'API et le fichier requirements.txt associé
* l'ensemble des fichiers utilisés pour créer les tests
* les fichiers de déploiements de Kubernetes dans le repertoire kubernetes
* le fichier machine_learning.py contenant le code pour entrainer et stocker les modeles KNN et regression logistique
* les fichiers model_knn.joblib et model_logistic.joblib contenant les modeles entrainés, pour réutilisation dans main.py
* le fichier features.json contenant l'ensemble des features des données utilisées pour entrainer les modèles, pour réutilisation dans main.py

### Création d’un modèle de Machine learning
Cf notebook Projet churn_mar22bcde_KParra_AdeOliveira livré pour le projet 1
* Audit + Exploration des données 
* Visualisation 
* Entraînement et évaluation de modèles de machine learning 


### L'API
L'API est construite avec FastAPI dans le fichier main.py.
Cette API permet d'interroger 2 modèles : KNN et Regression Logistique. 

Routes disponibles :
* / : Message welcome
* /status : Test de connexion. Accessibles pour les administrateurs
* /models : Liste des noms des différents modèles disponibles
* /models/{model_name}/prediction : Prediction à partir d'un des modèles référencés au point précédent, et performance de l'algorithme sur les jeux de tests.

Une identification basique est utilisée. La liste d'utilisateurs/mots de passe:
  - alice: wonderland
  - bob: builder
  - clementine: mandarine


### Le container
Un container Docker a été créé pour déployer facilement l'API. 

Les librairies Python à installer ainsi que leurs différentes versions sont détaillées dans le fichier requirements.txt.  

Commandes pour construire le container docker dans le répertoire racine :
* docker build -t api_churn .


Commandes pour lancer l'API en local :
* docker container run -p 8000:8000 api_churn
* swagger disponible sur : http://127.0.0.1:8000/docs
* API disponible sur : http://127.0.0.1:8000/


Commandes pour ajouter l'API sur dockerhub :
* docker login --username krineparra --password ...
* docker tag api_churn krineparra/api_churn
* docker image push krineparra/api_churn:latest
* penser à redémarrer le deploiement kubernetes s'il tourne déjà pour prendre en compte les modifications de l'API


### Les tests
Une série de tests a été créée pour tester l'API conteneurisée. 
On a pour cela créé un fichier docker-compose.yml


### Kubernetes
Pour permettre le déploiement de l'API sur 3 Pods, ont été créés : 
* Un fichier de déploiement 
* un Service 
* un Ingress 

Commandes pour construire le deploiement k8s :
* minikube start
* minikube addons enable ingress
* minikube dashboard --url=true
* VM : kubectl proxy --address='0.0.0.0' --disable-filter=true
* kubectl create -f deployment.yml
* kubectl create -f service.yml
* kubectl create -f ingress.yml
* VM : ouvrir un tunnel : ssh -i "data_enginering_machine.pem" ubuntu@(ip de la machine) -fNL 8000:192.168.49.2:80
* API disponible sur : http://127.0.0.1:8000/docs
* VM : Dashboard k8s disponible sur : http://(ip de la VM):8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/


### Livrable
Un fichier pdf contient les précisions sur les fichiers, les différentes étapes ainsi que sur les choix effectués. 

