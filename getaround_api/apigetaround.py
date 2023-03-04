# Importing libraries

import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from joblib import load
import os


import boto3
import pickle



description = """
ML for getaround
"""

# Declare API metadata
tags_metadata = [
    {
        "name": "Introduction Endpoint",
        "description": "Simple endpoint to try out!",
    },

    {
        "name": "Machine Learning Endpoint",
        "description": "getaround pricing api"
    }
]

# Declare instance of API
app = FastAPI(
    title="getaround pricing api",
    description=description,
    version="0.1",
    contact={
        "name": "getaround pricing api",
        #"url": "none",
    },
    openapi_tags=tags_metadata
)

# Declare formating of queries to the API
class PredictionFeatures(BaseModel):
    model_key : str
    mileage: int
    engine_power: int
    fuel: str
    paint_color : str
    car_type: str
    private_parking_available :bool
    has_gps: bool
    has_air_conditioning : bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

# Declare intro endpoint
@app.get("/", tags=["Introduction Endpoint"])
async def index():

    message = 'This is the API default endpoint. To get more information about the API, go to "/docs".'
    return message


# Delcare predict endpoint using formating query
@app.post("/predict", tags=["Machine Learning Endpoint"])
async def predict(features: PredictionFeatures):    
    """
    getaround pricing estimator.
    """ 
    # Read query as Pd dataframe
    df = pd.DataFrame(dict(features), index=[0])
    # Load model
    loaded_model = load('getaround.joblib')
    # Run prediction using model
    prediction = loaded_model.predict(df)
    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

# Run api
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)