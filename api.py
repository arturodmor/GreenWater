from fastapi import FastAPI, UploadFile, File
import os
import pandas as pd
from GreenWater.utils import Utils

app = FastAPI(title="GreenWater. Chemical predictor")
functions = Utils()

# ENDPOINT 1. Upload data.csv
@app.post("/upload")
async def upload_file(file:UploadFile = File(...)): # The method waits that user upload a file

    file_path = f"data/{file.filename}"
    with open(file_path,"wb") as f:
        f.write(file.file.read())
    return {"FILE_INFO":f"'{file.filename}' is stored in '{file_path}'"}


@app.post("/train-model")
async def train_model_endpoint():
    file_location = "data/data.csv"
    data = pd.read_csv(file_location)
    data = functions.data_processing(df=data)
    model = functions.train_model(df=data)
    return {"info": "Model trained and saved"}

