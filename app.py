import streamlit as st
import pickle
import numpy as np
import pandas as pd

# import the model
pipe = pickle.load(open('pipe3.pkl', 'rb'))
df = pickle.load(open('df3.pkl', 'rb'))

st.title("Laptop Predictor")

# brand
company = st.selectbox('Brand', df['Company'].unique())

# type of laptop
type = st.selectbox('Type', df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])

# weight
weight = st.number_input('Weight of the Laptop')

# Touchscreen
touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])

# IPS
ips = st.selectbox('IPS', ['No', 'Yes'])

# screen size
screen_size = st.number_input("Enter screen size (in inches):", min_value=0.1)

# resolution
resolution = st.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160', '3200x1800',
                                                '2880x1800', '2560x1600', '2560x1440', '2304x1440'])

# Calculate PPI before using it in query
X_res = int(resolution.split('x')[0])
Y_res = int(resolution.split('x')[1])
ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

# cpu
cpu = st.selectbox('CPU', df['Cpu brand'].unique())

hdd = st.selectbox('HDD(in GB)', [0, 128, 256, 512, 1024, 2048])

ssd = st.selectbox('SSD(in GB)', [0, 8, 128, 256, 512, 1024])

# GPU Brand only
gpu_brand = st.selectbox('GPU Brand', df['Gpu brand'].unique())  # Only ask for GPU brand

# OS
os = st.selectbox('OS', df['os'].unique())

if st.button('Predict Price'):
    # Convert touchscreen and ips to binary
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    # Create a dictionary with column names matching the training data
    input_data = {
        'Company': company,
        'TypeName': type,
        'Ram': ram,
        'Weight': weight,
        'Touchscreen': touchscreen,
        'Ips': ips,
        'ppi': ppi,
        'Cpu brand': cpu,
        'HDD': hdd,
        'SSD': ssd,
        'Gpu brand': gpu_brand,  # Only use 'Gpu brand'
        'os': os
    }

    # Convert the dictionary to a DataFrame
    query_df = pd.DataFrame([input_data])

    # Predict price using the pipeline
    predicted_price = np.exp(pipe.predict(query_df)[0])  # Assuming your model predicts the log price

    # Display the predicted price
    st.title("The predicted price of this configuration is " + str(int(predicted_price)))
