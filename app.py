import streamlit as st
import pandas as pd

st.set_page_config(page_title="Stok Sistemi", layout="wide")

df = pd.read_excel("STOK.xlsx", sheet_name="STOK")
df.columns = df.columns.str.strip()

df["TEL"] = df["TEL"].astype(str).str.strip()
df["CİNS"] = df["CİNS"].astype(str).str.strip()

df = df.dropna(subset=["TEL", "CİNS"])
df.columns = df.columns.str.strip()

st.title("📦 Stok Sorgulama")

col1, col2 = st.columns(2)

with col1:
    secili_tel = st.selectbox(
        "TEL",
        sorted(df["TEL"].unique())
    )

filtreli_df = df[df["TEL"] == secili_tel]

with col2:
    secili_cins = st.selectbox(
        "CİNS",
        sorted(filtreli_df["CİNS"].unique())
    )

sonuc = df[(df["TEL"] == secili_tel) & (df["CİNS"] == secili_cins)]

if not sonuc.empty:

    veri = sonuc.iloc[0]

    st.markdown("### 📋 Stok Detayı")

    st.markdown(f"""
    <div style="
        background-color:#f9f9f9;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 2px 10px rgba(0,0,0,0.1);
        font-size:16px;
    ">
        <b>RAF NO:</b> {veri["RAF NO"]} <br><br>
        <b>ELSAN:</b> {veri["ELSAN"]} <br>
        <b>HES:</b> {veri["HES"]} <br>
        <b>ERİKOĞLU:</b> {veri["ERİKOĞLU"]} <br>
        <b>EMSAN:</b> {veri["EMSAN"]} <br>
        <b>KAVİ:</b> {veri["KAVİ"]} <br>
        <b>EMTEL:</b> {veri["EMTEL"]} <br><br>
        <hr>
        <h3>TOPLAM: {veri["TOPLAM"]}</h3>
    </div>
    """, unsafe_allow_html=True)

    try:
        if int(veri["TOPLAM"]) < 10:
            st.error("⚠ Kritik Stok Seviyesi!")
    except:
        pass

else:
    st.warning("Kayıt bulunamadı.")