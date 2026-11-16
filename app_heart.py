import streamlit as st
import numpy as np
import pandas as pd
import pickle
import datetime
with open('heart_model.pkl','rb') as file:
    loaded_model = pickle.load(file)
st.set_page_config(page_title ="Heart Disease Detector", page_icon ="heart", layout = "centered")
st.markdown("""
    <style>
    .stApp{background-color: #FFF5F5;}
    h1{color:#DC2626; text-align: center; font-weight: bold;}
    .stButton>button{
    backgrount-color: #DC2626; color:white;font-size: 18px;
    font-weight: bold; width: 100%; border-radius: 8px;}
    .stButton>button:hover{background-color:#891C1C;}
    </style>
    """,unsafe_allow_html= True)
st.title("Heart disease prediction app")
st.write("Please enter below medical details of patients")
st.markdown("---")
patient_name = st.text_input("Name of the patient:",value ="Rahul Sharma")
col1,col2 = st.columns(2)
with col1:
    age = st.number_input("Age:", min_value = 1 , max_value = 120 , value = 45)
    sex_label = st.selectbox("sex:", options = ["Male","Female"])
    sex = 1 if sex_label=="Male" else 0
    cp = st.slider("Chest Pain Type 0-3:", 0, 3 , 1)
    trestbps = st.number_input("Resting BP:",min_value = 50, max_value= 250, value = 120)
    chol = st.number_input("Cholesterol:", min_value = 100, max_value = 600, value = 200)
    fbs_label = st.selectbox("Fasting blood sugar > 120 mg/dl?:",options = ["No", "Yes"])
    fbs =1 if fbs_label =="Yes" else 0
with col2:
    restecg = st.slider("Resting ECG Result(0-2):", 0,2,0)
    thalach = st.number_input("Max Heart Rate:",min_value = 60, max_value = 250, value = 150)
    exang_label = st.selectbox("Is Chest Pain from exerciese?:", options =["No","Yes"])
    exang = 1 if exang_label=="Yes" else 0
    oldpeak = st.number_input("ST Depression (Oldpeak):",min_value =0.0, max_value = 10.0 , value = 1.0 , step = 0.1)
    slope = st.slider("Slope of ST segment(0-2):",0,2,1)
    ca = st.slider("Main drain number(Ca 0-4):",0,4,0)
    thal = st.slider("Thalisimia score(Thal 0-3):", 0 , 3,2)
st.markdown("---")
if st.button("Check health(Predict Status)"):
    input_data = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
    prediction = loaded_model.predict(input_data)
    if prediction[0] == 1:
        result_text = "High Probablity of Heart Disease(consult a Doctor)"
        st.error("Warning: According to model probablity of patient has heart diseas. please  consult to doctor")
    else:
        result_text = "Normal Status (Heart looks safe)"
        st.success("Good news: According to model hear is safe. patient is normal")
    st.markdown("----")
    st.subheader("Health Vitals Comparison (Patient Vs Normal Limit)")
    chart_data = pd.DataFrame({
        "Patient Value": [trestbps, chol, thalach],
        "Normal Reference": [120,200,150]
    }, index = ["Blood Pressure","Cholesterol","Max Heart Rate"])
    st.bar_chart(chart_data)
    current_date = datetime.date.today()
    report_content = f"""=========HEART HEALTH SCREENING REPORT==========
Date: {current_date}
Patient Name: {patient_name}
Age / Sex: {age} yrs / {sex_label}
------CLINICAL PARAMETERS--------
Resting Blood Pressure : {trestbps}
Cholesterol Level       : {chol} mg/dl
Max Heart Rate          : {thalach} bpm
Fasting Blood Sugar     : {fbs_label}
Chest Pain Type         : {cp}
Exercise Angina         : {exang_label}
-------AI MODEL PREDICTION---------
Status: {result_text}
Note: This is an AI -generated screening report for educational purposes.
Please consult a certified cardiologist for medical advice.
======================================================================"""
    st.download_button(
        label = "Download Patient Report(.txt)",
        data = report_content,
        file_name = f"{patient_name.replace(' ','_')}_Heart_Report.txt",
        mime = "text / plain"
    )
