from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
import pickle
import pandas as pd


#create an pydantic model to take user_input
class UserInput(BaseModel):

    CreditScore: Annotated[int, Field(..., gt=0, lt=901, description='Credit_Score of the user')]
    Gender: Annotated[Literal['Male', 'Female'], Field(..., description='Gender of the user')]
    Age: Annotated[int, Field(..., gt=18, lt=100, description='Age of the user')]
    Tenure: Annotated[int, Field(..., gt=0, description='Tenure of user')]
    Balance: Annotated[float, Field(..., description='user bank balance')]
    NoOfProducts: Annotated[int, Field(..., description='No of user products')]
    HasCrCard: Annotated[int, Field(...,description="1 if user has a credit card, 0 otherwise",ge=0, le=1,examples=[0, 1])]
    IsActiveMember: Annotated[int, Field(...,description="1 if user is an active member, 0 otherwise",ge=0, le=1,examples=[0, 1])]
    EstimatedSalary: Annotated[float, Field(..., description='user estimated salary')]

    

    @computed_field
    @property
    def BalanceSalaryRatio(self) -> float:
        return self.Balance/self.EstimatedSalary

    @computed_field
    @property
    def CreditAgeRatio(self) -> float:
        return self.CreditScore/self.Age

    @computed_field
    @property
    def High_Bal_Customers(self)->str:
        if self.Balance>=97198.54:
            return "High"
        else:
            return "Low"

    @computed_field
    @property
    def CreditScoreSegregation(self)->str:
        if self.CreditScore>=700:
            return "High"
        elif self.CreditScore>600 and self.CreditScore<700:
            return "Medium"
        else:
            return "Low"
    
    @computed_field
    @property
    def categorize_age(self)->str:
        if self.Age < 30:
            return "Young"
        elif self.Age < 45:
            return "Adult"
        elif self.Age < 60:
            return "Middle_Aged"
        else:
            return "Older"
        
    @computed_field
    @property
    def long_tenure_label(self)->str:
        if self.Tenure >= 5:
            return "Long"
        else:
            return "Short"
    