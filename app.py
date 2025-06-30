import streamlit as st
import pandas as pd
import numpy as np
import pickle

# === Load model & fitur ===
@st.cache_resource
def load_model():
    with open("random_forest_model.pkl", "rb") as f:
        model, feature_names = pickle.load(f)
    return model, feature_names

model, feature_names = load_model()

# === Header Dashboard ===
st.set_page_config(page_title="Prediksi Harga Sewa", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stApp { padding: 2rem; }
        .title { font-size: 2.5rem; font-weight: bold; color: #444; }
        .subtitle { font-size: 1.2rem; color: #777; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🏘️ Dashboard Prediksi Harga Sewa Properti</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Masukkan detail properti untuk memprediksi estimasi sewa per bulan</div><br>', unsafe_allow_html=True)

# === Split Layout ===
col1, col2 = st.columns(2)

with col1:
    area = st.number_input("📐 Luas Bangunan (ft²)", 100, 10000, 900)
    beds = st.selectbox("🛏️ Jumlah Kamar Tidur", [1, 2, 3, 4, 5])
    bathrooms = st.selectbox("🚿 Jumlah Kamar Mandi", [1, 2, 3, 4])
    balconies = st.selectbox("🌇 Jumlah Balkon", [0, 1, 2, 3])

with col2:
    area_rate = st.number_input("💸 Area Rate (₹/ft²)", 1, 500, 50)
    furnishing = st.selectbox("🪑 Tipe Furnishing", ['Unfurnished', 'Semi-Furnished', 'Furnished'])
    furnishing_val = {'Unfurnished': 0, 'Semi-Furnished': 1, 'Furnished': 2}[furnishing]

    city_list = [col.split('_')[1] for col in feature_names if col.startswith('city_')]
    locality_list = [col.split('_')[1] for col in feature_names if col.startswith('locality_')]
    selected_city = st.selectbox("🏙️ Kota", sorted(city_list))
    selected_locality = st.selectbox("📍 Locality", sorted(locality_list))

# === Buat Input DataFrame ===
input_df = pd.DataFrame(columns=feature_names)
input_df.loc[0] = [0] * len(feature_names)

# Set nilai input
input_df.at[0, 'area'] = area
input_df.at[0, 'beds'] = beds
input_df.at[0, 'bathrooms'] = bathrooms
input_df.at[0, 'balconies'] = balconies
input_df.at[0, 'furnishing'] = furnishing_val
input_df.at[0, 'area_rate'] = area_rate

city_col = f'city_{selected_city}'
locality_col = f'locality_{selected_locality}'
if city_col in input_df.columns:
    input_df.at[0, city_col] = 1
if locality_col in input_df.columns:
    input_df.at[0, locality_col] = 1

# === Tombol Prediksi ===
predict_btn = st.button("🔍 Prediksi Harga Sewa")

if predict_btn:
    prediction = model.predict(input_df)[0]
    
    st.markdown("---")
    st.markdown("### 💰 Hasil Prediksi")
    
    colA, colB, colC = st.columns([1, 3, 1])
    with colB:
        st.markdown(f"""
        <div style="padding: 2rem; background-color: #dff0d8; border-radius: 12px; text-align: center;">
            <h2 style="color: #3c763d;">₹ {prediction:,.0f} / bulan</h2>
            <p style="color: #3c763d;">Estimasi harga sewa properti berdasarkan input Anda</p>
        </div>
        """, unsafe_allow_html=True)
