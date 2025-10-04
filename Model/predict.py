import pickle
import pandas as pd

# import the ml model
with open('Model/model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_output(user_input: dict):
    input_df = pd.DataFrame([user_input])

    output = model.predict(input_df)[0]
    return output