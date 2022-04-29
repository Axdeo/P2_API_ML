# P2_API_ML
ML predictions of churn API - Formation project P2 DataScientest

## OBJECTIF:
L'objectif de ce projet est de déployer un modèle de Machine Learning. 

Attention, en production, les modèles ne devront pas être relancés.

### Création d’un modèle de Machine learning
* Audit + Exploration des données
* Visualisation
* Entraînement et évaluation de modèles de machine learning

### L'API
On va dans un premier construire une API avec Flask ou FastAPI.

Cette API devra permettre d'interroger les différents modèles. 

Routes disponibles :
* / : Message welcome
* /status : Test de connexion
* /models : Liste des noms des différents modeles disponibles
* /models/{model_name}/prediction : Prediction à partir d'un des modèles référencés au point précédent
Les utilisateurs pourront aussi interroger l'API pour accéder aux performances de l'algorithme sur les jeux de tests.

Enfin il faut permettre aux utilisateurs d'utiliser une identification basique. (On pourra utiliser le header Authentication et encoder username:password en base 64).

On pourra utiliser la liste d'utilisateurs/mots de passe suivante:
  - alice: wonderland
  - bob: builder
  - clementine: mandarine
  - ...

### Le container
Il s'agira ici de créer un container Docker pour déployer facilement l'API. 

n portera une attention particulière aux librairies Python à installer ainsi qu'à leurs différentes versions.  

TODO : préciser les versions dans requirements.txt


Commandes pour construire le container docker dans le répertoire racine :
* docker build -t api_churn .


Commandes pour lancer l'API en local :
* docker container run -p 8000:8000 api_churn
* swagger disponible sur : http://127.0.0.1:8000/docs
* API disponible sur : http://127.0.0.1:8000/


Commandes pour ajouter l'API sur github :
* docker login --username krineparra --password ...
* docker tag api_churn krineparra/api_churn
* docker image push krineparra/api_churn:latest
* penser à redémarrer le deploiement kubernetes s'il tourne déjà pour prendre en compte les modifications de l'API


### Les tests
Une série de tests devra être créée pour tester l'API conteneurisée. 

On pourra pour cela créer un fichier docker-compose.yml en s'inspirant de ce qui a été fait dans l'évaluation de Docker.

### Kubernetes
On pourra enfin créer un fichier de déploiement ainsi qu'un Service et un Ingress avec Kubernetes pour permettre le déploiement de l'API sur au moins 3 Pods.

Commandes pour construire le deploiement k8s :
* minikube addons enable ingress
* kubectl create -f deployment.yml
* kubectl create -f service.yml
* kubectl create -f ingress.yml
* API disponible sur : http://127.0.0.1:8000/docs

### Les Livrables
Les attendus sont un fichier pdf contenant des précisions sur les fichiers, sur les différentes étapes ainsi que sur les choix effectués. 

On devra aussi rendre un repo Github sur lequel seront les fichiers suivants:
* fichier source de l'API
* Dockerfile de l'API
* dans un dossier l'ensemble des fichiers utilisés pour créer les tests
* les fichiers de déploiements de Kubernetes
* tout autre fichier ayant été utilisé pour faire ce projet.