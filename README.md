# Bloc 5 - Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision

## getaround_streamlit

file for the streamlit dash board accessible at : https://getaround369.herokuapp.com/
contains:

- A Dockerfile
- the data as a csv file
- the app.py for the dashboard

## getaround_api

file for the api accessible at : https://getaroundapi369.herokuapp.com/
contains:

- a train.py to train the model
- reqquiements.txt file for the dockerfile
- a joblib file which saved the model
- two csv files to feed data to the model
- a Dockerfile
- a .py app for the api


here is an example querry to test the /predict endpoint:

import requests

payload = {
  "model_key": "Citroen",
  "mileage": 140411,
  "engine_power": 100,
  "fuel": "diesel",
  "paint_color": "black",
  "car_type": "convertible",
  "private_parking_available": True,
  "has_gps": True,
  "has_air_conditioning": False,
  "automatic_car": False,
  "has_getaround_connect": True,
  "has_speed_regulator": True,
  "winter_tires": True
}

response = requests.post("https://getaroundapi369.herokuapp.com/predict", json=payload)

response.text

this shloud return : '{"prediction":117.02883761383585}'
