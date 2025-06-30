import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Load the model and data
try:
    if not os.path.exists('pipe3.pkl'):
        raise FileNotFoundError('pipe3.pkl not found in the app directory.')
    if not os.path.exists('df3.pkl'):
        raise FileNotFoundError('df3.pkl not found in the app directory.')
    pipe = pickle.load(open('pipe3.pkl', 'rb'))
    df = pickle.load(open('df3.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model or data: {e}\n\nIf you see a ModuleNotFoundError, make sure all required libraries and custom classes used in the model are installed and available.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="LappyTag - Laptop Price Predictor",
    page_icon="💻",
    layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f7fbfc;
    }
    .title-style {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #154360;
        font-size: 70px;
        font-weight: bold;
        text-shadow: 2px 2px #85c1e9;
        background-color: #e8f8f5;
        padding: 20px;
        border-radius: 10px;
    }
    .subtitle-style {
        text-align: center;
        font-family: 'Trebuchet MS', sans-serif;
        color: #117864;
        font-size: 26px;
        margin-top: 20px;
        margin-bottom: 30px;
        font-style: italic;
    }
    .footer {
        font-family: 'Arial', sans-serif;
        text-align: center;
        color: #34495e;
        font-size: 16px;
        margin-top: 20px;
    }
    .footer a {
        color: #1a5276;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True
)

# Header section
st.markdown('<h1 class="title-style">LappyTag 💻</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Your intelligent laptop price prediction system</p>', unsafe_allow_html=True)

# Form layout
with st.container():
    st.subheader("Select Laptop Features")
    col1, col2 = st.columns(2)

    with col1:
        company = st.selectbox('Brand', df['Company'].unique())
        type = st.selectbox('Type', df['TypeName'].unique())
        ram = st.selectbox('RAM (in GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
        weight = st.number_input('Weight of the Laptop (kg)', format="%.2f", min_value=0.1)

    with col2:
        touchscreen = st.radio('Touchscreen', ['No', 'Yes'], horizontal=True)
        ips = st.radio('IPS Display', ['No', 'Yes'], horizontal=True)
        screen_size = st.number_input("Screen Size (in inches):", min_value=10.0, format="%.1f")
        resolution = st.selectbox('Screen Resolution', ['1920x1080', '1366x768', '1600x900', '3840x2160',
                                                        '3200x1800', '2880x1800', '2560x1600', '2560x1440',
                                                        '2304x1440'])

    st.subheader("Select Hardware Specifications")
    col3, col4 = st.columns(2)

    with col3:
        cpu = st.selectbox('CPU', df['Cpu brand'].unique())
        hdd = st.selectbox('HDD (in GB)', [0, 128, 256, 512, 1024, 2048])

    with col4:
        ssd = st.selectbox('SSD (in GB)', [0, 8, 128, 256, 512, 1024])
        gpu_brand = st.selectbox('GPU Brand', df['Gpu brand'].unique())

    os = st.selectbox('Operating System', df['os'].unique())

# Prediction button
if st.button('Predict Price', key='predict_button'):
    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0
    X_res, Y_res = map(int, resolution.split('x'))
    ppi = ((X_res ** 2) + (Y_res ** 2)) ** 0.5 / screen_size

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
        'Gpu brand': gpu_brand,
        'os': os
    }

    query_df = pd.DataFrame([input_data])

    # Predicting the price
    predicted_price = np.exp(pipe.predict(query_df)[0])  # Assuming log price prediction

    st.success(f"💰 **The predicted price of this configuration is ₹{int(predicted_price):,}**")

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <p>Crafted with 💙 by Hardik Sharma</p>
        <p>
            <a href="https://github.com/hardiksharma0511" target="_blank">GitHub</a> | 
            <a href="https://www.linkedin.com/in/hardiksharma05" target="_blank">LinkedIn</a>
        </p>
    </div>
    """, unsafe_allow_html=True
)
