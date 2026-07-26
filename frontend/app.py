import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Forecast Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for property features
Product_id = st.text_input("Product ID")
Product_Weight = st.number_input("Product_Weight (in units)", min_value=0.0, step=0.1)
Product_Sugar_Content = st.selectbox("Product_Sugar_Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area (in sq.m)", min_value=0.0, step=0.001)
Product_Type = st.selectbox("Product_Type", ["Frozen Foods", "Dairy", "Canned", "Baking Goods", "Health and Hygiene",
        "Snack Foods", "Meat", "Household", "Hard Drinks", "Fruits and Vegetables",
        "Breads", "Breakfast", "Soft Drinks", "Starchy Foods", "Seafood", "Others"])
Product_MRP = st.number_input("Product MRP (₹)", min_value=0.0, step=0.5)
Store_Id = st.text_input("Store ID")
Store_Establishment_Year = st.number_input("Store Establishment Year",min_value=1900,max_value=2030,step=1)
Store_Size = st.selectbox("Store Size",["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type",["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox( "Store Type",["Supermarket Type1","Supermarket Type2","Departmental Store","Food Mart"])

import datetime
current_year = datetime.datetime.now().year
Store_Age = current_year - Store_Establishment_Year
Store_Age = st.write(f"Store Age: {Store_Age} years")


# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_id': Product_id,
    'Product_Weight': Product_Weight,
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_Type': Product_Type,
    'Product_MRP': Product_MRP,
    'Store_Id': Store_Id,
    'Store_Establishment_Year': Store_Establishment_Year,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Store_Age': Store_Age
    }])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted sales forecast (in dollars)']
        st.success(f"Predicted sales forecast (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
