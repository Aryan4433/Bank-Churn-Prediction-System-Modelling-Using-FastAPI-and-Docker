import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict" 

st.title("Bank Churn Predictor")
st.markdown("Enter your details below:")

# Input fields
CreditScore = st.number_input("CreditScore", min_value=1, max_value=900)
Gender = st.selectbox("Gender", options=["Male", "Female"])
Age = st.number_input("Age", min_value=19, max_value=99, step=1)
Tenure = st.number_input("Tenure", min_value=1, step=1)
Balance = st.number_input("Balance", min_value=0.0, format="%.2f")
NoOfProducts = st.number_input("NoOfProducts", min_value=1, step=1)
HasCrCard = st.selectbox("HasCrCard", options=[0, 1])
IsActiveMember = st.selectbox("IsActiveMember", options=[0, 1])
EstimatedSalary = st.number_input("EstimatedSalary", min_value=0.0, format="%.2f")


if st.button("Predict Churn Category"):
    input_data = {
        "CreditScore": CreditScore,
        "Gender": Gender,
        "Age": Age,
        "Tenure": Tenure,
        "Balance": Balance,
        "NoOfProducts": NoOfProducts,
        "HasCrCard": HasCrCard,
        "IsActiveMember": IsActiveMember,
        "EstimatedSalary": EstimatedSalary
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200:
            # Case 1: If API returns {"Prediction": "Churned"}
            if "Prediction" in result:
                prediction = result["Prediction"]
                st.success(f"Predicted Churn Category: **{prediction}**")

            # Case 2: If API returns {"response": {...}}
            elif "response" in result:
                prediction = result["response"]
                st.success(f"Predicted Churn Category: **{prediction['prediction']}**")
                st.write("🔍 Confidence:", prediction.get("confidence"))
                st.write("📊 Class Probabilities:")
                st.json(prediction.get("class_probabilities"))

            else:
                st.warning("⚠️ Unexpected response format from API")
                st.json(result)

        else:
            st.error(f"API Error: {response.status_code}")
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")


