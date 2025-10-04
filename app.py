from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse,HTMLResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd
from schema.user_input import UserInput
from Model.predict import model, predict_output

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Bank Churn Prediction System"}

templates = Jinja2Templates(directory="templates")

@app.get("/home", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post('/predict')
def predict_premium(data: UserInput):

    user_input = {
        "Gender": data.Gender,
        "Balance": data.Balance,
        "NumOfProducts": data.NoOfProducts,
        "HasCrCard": data.HasCrCard,
        "IsActiveMember": data.IsActiveMember,
        "EstimatedSalary": data.EstimatedSalary,
        "BalanceSalaryRatio": data.BalanceSalaryRatio,
        "CreditAgeRatio": data.CreditAgeRatio,
        "HighBalanceCustomers": data.High_Bal_Customers,
        "CreditScoreSegregation": data.CreditScoreSegregation,
        "Age_Group": data.categorize_age,
        "LongTenure": data.long_tenure_label
    }

    prediction = predict_output(user_input)

    return JSONResponse(status_code=200, content={'Prediction': prediction})






