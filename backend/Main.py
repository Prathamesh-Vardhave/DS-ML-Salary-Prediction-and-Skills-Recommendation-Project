from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from feature_engineering import process_user_input
from recommendation import recommend_skills

#create app
app=FastAPI()

#loading model but only once
model_path=os.path.join("..","Model","xgb_tunned_salary_model.pkl")
model=joblib.load(model_path)

print("Model Loaded Sucessfully")

#Input schema

class UserInput(BaseModel):
    Job_Role:str
    primary_city:str
    experience:float
    skills:list[str]

#root test route
@app.get("/")

def home():
    return {"message":"salary prediction api running"}

#predict route
@app.post("/predict")
def predict_salary(user: UserInput):

    data = user.dict()

    # Feature Engineering
    input_df = process_user_input(data)

    # Salary Prediction
    prediction = model.predict(input_df)[0]

    # Skill Recommendation
    exp_bucket = input_df["exp_bucket"].iloc[0]

    recommended = recommend_skills(
        job_role=data["Job_Role"],
        exp_bucket=exp_bucket,
        user_skills=data["skills"],
        top_n=10
    )

    return {
        "predicted_salary": round(float(prediction), 2),
        "recommended_skills": recommended
    }

