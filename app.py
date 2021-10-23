from flask import Flask, request, render_template 
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.base import BaseEstimator, TransformerMixin
import sklearn.externals 
import joblib
import datetime
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

class CategoricalEncoding(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
        
    def fit(self,x,y=None):
        return self
            
    def transform(self, X):
        app.logger.info('<------Encoding Categorical variables------>')
        X_ = X.copy()
        X_['sex_male'] = np.where(X_['sex']=='male',1,0)
        X_['smoker_yes'] = np.where(X_['smoker']=='yes',1,0)
        X_['region_northwest'] = np.where(X_['region']=='northwest',1,0)
        X_['region_southwest'] = np.where(X_['region']=='southwest',1,0)
        X_['region_northeast'] = np.where(X_['region']=='northeast',1,0)
        X_.drop(['sex', 'smoker', 'region'], 1, inplace=True)
        return X_
    
class OutlierTreatment(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
        
    def fit(self,x,y=None):
        return self
            
    def transform(self,X):
        app.logger.info('<------Treating Outliers------>')
        X_ = X.copy()
        tenth_percentile = np.percentile(X_['bmi'], 10)
        ninetieth_percentile = np.percentile(X_['bmi'], 90)
        X_['bmi'] = np.where(X_['bmi']<tenth_percentile, tenth_percentile, X_['bmi'])   
        X_['bmi'] = np.where(X_['bmi']>ninetieth_percentile, ninetieth_percentile, X_['bmi'])   
        return X_

@app.route("/")
def home():
    app.logger.info('<------Loading home page------>')
    return render_template("home.html")

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    app.logger.info('<------Using model to predict the premium------>')
    if request.method == "POST":

        # Age
        age = int(request.form["Age"])
        
        # Gender
        gender = request.form["Gender"]
        
        # BMI
        BMI = float(request.form["bmi"])
        
        # Number of children
        children = int(request.form["Children"])
        
        # Smoker
        smoker = request.form["Smoker"]
        
        # Region
        region = request.form["Region"]

    #     ['age', 'sex','bmi', 'children', 'smoker', 'region']
        data = pd.DataFrame([[age, gender, BMI, children, smoker, region]], columns= ['age', 'sex','bmi', 'children', 'smoker', 'region'])
        prediction=model.predict(data)

        output=np.round(np.exp(prediction[0]),2)
        app.logger.info('<------Returning predicted output------>')
        return render_template('home.html',prediction="Your estimated health insurance premium is {} $".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    model = joblib.load('insurance_premium_perdiction.pkl')
    app.run(debug=True)
