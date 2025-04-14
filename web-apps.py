import streamlit as st
import requests
import pandas as pd
from model_ai import classify_image

UBIDOTS_TOKEN = "BBUS-itVkw0RhfDRPK6GiVnfgbiLsOhdWOn"
DEVICE_LABEL = "smart-trash"
VARIABLE_LABEL = "trash_level"

st.title("🗑️ Dashboard Tempat Sampah Pintar")

# Fetch dari Ubidots
def get_data():
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{VARIABLE_LABEL}/values"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    r = requests.get(url, headers=headers)
    results = r.json()['results']
    timestamps = [pd.to_datetime(x['timestamp'], unit='ms') for x in results]
    values = [x['value'] for x in results]
    return pd.DataFrame({'Waktu': timestamps, 'Level Sampah': values})

df = get_data()
st.line_chart(df.set_index("Waktu"))

latest = df["Level Sampah"].iloc[0]
st.metric("Level Sampah Saat Ini", f"{latest:.1f}%")

if latest > 80:
    st.warning("⚠️ Tempat sampah hampir penuh!")

# Upload gambar untuk klasifikasi AI
uploaded = st.file_uploader("Upload foto sampah untuk klasifikasi AI", type=["jpg", "png"])
if uploaded:
    from PIL import Image
    img = Image.open(uploaded)
    st.image(img, caption="Gambar sampah", use_column_width=True)
    
    result = classify_image(uploaded)
    st.success(f"Hasil Klasifikasi AI: *{result}*")