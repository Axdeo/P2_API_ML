import joblib
from sklearn.linear_model import LogisticRegression
import json
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

def load_data():
    """
    Charge, nettoie et formate le jeu de données churn.csv
    """
    # Les données sont chargées dans un dataframe:
    data = pd.read_csv('https://assets-datascientest.s3-eu-west-1.amazonaws.com/de/total/churn.csv')

    # Transformation des variables qualitatives : PaymentMethod et InternetService, via get_dummies
    data = pd.get_dummies(data=data, prefix="PaymentMethod", columns=['PaymentMethod'], drop_first=False)
    data = pd.get_dummies(data=data, prefix="InternetService", columns=['InternetService'], drop_first=False)

    # Transformation des autres variables
    data['gender'] = data['gender'].replace(['Male', 'Female'], [1,0]) # transformation binaire pour la feature 'gender'
    data = data.replace('No internet service',-1) # pour toutes les sous features optionnelles de la feature 'InternetService' => -1 si pas de souscription 'InternetService'
    data = data.replace('No phone service',-1) # pour toutes les sous features optionnelles de la feature 'PhoneService' => -1 si pas de souscription 'PhoneService'
    data = data.replace(['Yes','No'],[1,0]) #transformation binaire pour tous les 'yes'/'no' du dataset
    data['Contract'] = data['Contract'].replace(['Two year', 'One year', 'Month-to-month'],[24,12,1]).astype('int')

    # Nettoyage des valeurs vides :
    data.TotalCharges = data.TotalCharges.replace(" ",0).astype('float')

    # Renommage des variables avec des espaces dans les noms (pour pouvoir utiliser les memes noms dans l'API)
    data = data.rename(columns = {"PaymentMethod_Bank transfer (automatic)": "PaymentMethod_Bank_transfer",
                                  "PaymentMethod_Credit card (automatic)":"PaymentMethod_Credit_card",
                                  "PaymentMethod_Mailed check":"PaymentMethod_Mailed_check",
                                  "PaymentMethod_Electronic check":"PaymentMethod_Electronic_check",
                                  "InternetService_Fiber optic": "InternetService_Fiber_optic"})

    #colonne 'customerID' devient l'index du dataset
    data = data.set_index('customerID')
    return data

def save_models():
    """
    Instancie plusieurs modèles :
    - LogisticRegression
    - LinearSVC
    - KNN
    Entraine ces modèles
    Sauvegarde les modèles dans joblib
    Sauvegarde les features dans un fichier json
    """
    data = load_data()
    # séparation des données pour apprentissage :
    X = data.drop(columns = 'Churn')
    y = data.Churn

    # Instanciation, entrainement et sauvegarde dans un joblib de différents modèles :
    # - Logistic Regression
    model_logistic = LogisticRegression( solver ='liblinear')
    model_logistic.fit(X,y)
    with open('model_logistic.joblib', 'wb') as f:
        joblib.dump(model_logistic, f)

    # - LinearSVC :
    scaler = StandardScaler()
    Xs = scaler.fit(X).transform(X)
    model_linear = LinearSVC(random_state=0)
    model_linear.fit(Xs,y)
    with open('model_linear.joblib', 'wb') as f:
        joblib.dump(model_linear, f)

    # - KNN :
    model_knn = KNeighborsClassifier(17)
    model_knn.fit(X,y)
    with open('model_knn.joblib', 'wb') as f:
        joblib.dump(model_knn, f)

    # sauvagarde des features
    with open('features.json', 'w') as f:
        feature_names = X.columns.to_list()
        json.dump(feature_names,f, indent =4)

    return

if __name__ == "__main__":
    save_models()