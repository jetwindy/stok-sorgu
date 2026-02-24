import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stok Sistemi", layout="wide")

# Google Sheets canlı bağlantı
url = "https://docs.google.com/spreadsheets/d/189eP59G3ECgvXypR8UQ_BULqMSdZrLav/export?format=csv&gid=1105255650"

df = pd.read_csv(url)
df.columns = df.columns.str.strip()

st.title("📦 Stok Sorgulama")

secili_tel = st.selectbox("TEL Seç", sorted(df["TEL"].unique()))
filtered_cins = df[df["TEL"] == secili_tel]["CİNS"].unique()
secili_cins = st.selectbox("CİNS Seç", sorted(filtered_cins))

sonuc = df[(df["TEL"] == secili_tel) & (df["CİNS"] == secili_cins)]

if not sonuc.empty:
    st.success("Sonuç bulundu ✅")
    st.dataframe(
        sonuc[[
            "RAF NO",
            "ELSAN",
            "HES",
            "ERİKOĞLU",
            "EMSAN",
            "KAVİ",
            "EMTEL",
            "TOPLAM"
        ]]
    )