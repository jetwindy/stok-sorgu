import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stok Sistemi", layout="wide")

df = pd.read_excel("STOK.xlsx", sheet_name="STOK")
df.columns = df.columns.str.strip()

st.title("📦 Stok Sorgulama")

secili_tel = st.radio("TEL Seç", sorted(df["TEL"].unique()))
filtered_cins = df[df["TEL"] == secili_tel]["CİNS"].unique()
secili_cins = st.radio("CİNS Seç", sorted(filtered_cins))

sonuc = df[(df["TEL"] == secili_tel) & (df["CİNS"] == secili_cins)]

if not sonuc.empty:
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