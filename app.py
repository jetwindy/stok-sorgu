import streamlit as st
import pandas as pd

df = pd.read_excel("stok.xlsx", sheet_name="STOK")
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