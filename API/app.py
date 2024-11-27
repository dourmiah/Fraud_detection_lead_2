import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import joblib
import pandas as pd

app = FastAPI()

# Chargement du modèle
with open('randomforest_model.pkl', 'rb') as file:
    loaded_model = joblib.load(file)

# Chargement du pipeline de preprocessing
with open('preprocessor_model.pkl', 'rb') as file:
    loaded_preprocessor = pickle.load(file)

class PredictionFeatures(BaseModel):
    input: list
    


@app.post('/predict')
async def predict(predictionfeatures: PredictionFeatures):
    ### Predict if a transaction is a fraud
    input_data = predictionfeatures.input
    # input_features = [
    #     "trans_date_trans_time",
    #     "cc_num",
    #     "merchant",
    #     "category",
    #     "amt",
    #     "first",
    #     "last",
    #     "gender",
    #     "street",
    #     "city",
    #     "state",
    #     "zip",
    #     "lat",
    #     "long",
    #     "city_pop",
    #     "job",
    #     "dob",
    #     "trans_num",
    #     "unix_time",
    #     "merch_lat",
    #     "merch_long"
    # ]
    input_features = [
        "cc_num",
        "amt",
        "zip",
        "lat",
        "long",
        "city_pop",
        "unix_time",
        "merch_lat",
        "merch_long"
    ]
    
    df = pd.DataFrame(input_data, columns = input_features)
    data = loaded_preprocessor.transform(df)

    prediction = loaded_model.predict(data)


    response = {
        # "is_a_fraud ": "yes" if prediction[0] == "1" else "no"
        "is_a_fraud ": f"{prediction[0]}"
    }

    return response

@app.get('/docs')
async def get_docs():
    return {"doc_url": "/docs"}


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)