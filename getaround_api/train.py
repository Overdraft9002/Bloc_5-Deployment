# Import librairies
import os
import pandas as pd
import numpy as np
import time

from joblib import dump
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score

# Import dataset
df = pd.read_csv('/Users/ymilo/Desktop/Jedha/getaround/get_around_pricing_project.csv')
df.model_key = df.model_key.map({'Citroën': 'Citroen'})
del df['Unnamed: 0']

# Train test split
target_name = "rental_price_per_day"
features = df.drop(target_name, axis = 1)

X = features
Y = df[target_name]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.01, random_state=0)

# Declare numeric and categorical features
numeric_features = ['mileage', 'engine_power']
categorical_features = ['model_key', 'fuel', 'paint_color', 'car_type', 'private_parking_available', 'has_gps', 'has_air_conditioning','automatic_car','has_getaround_connect','has_speed_regulator','winter_tires',]

# Declare transformer and Pipelines
numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('encoder', OneHotEncoder(drop='first'))])
preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# Declare Model
model = Pipeline(steps=[
    ('features_preprocessing', preprocessor),
    ("Regressor",LinearRegression())
])

# Fit model
model.fit(X_train, Y_train)
prediction = model.predict(X_train)
    
print("...Done!")

# Save model
print("Saving model...")
dump(model, "getaround.joblib")
print(f"Model has been saved here: {os.getcwd()}")