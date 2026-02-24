import streamlit as st
import streamlit as st

if "giris" not in st.session_state:
    st.session_state.giris = False
    st.session_state.kullanici = ""

if not st.session_state.giris:

    st.title("Stok Sistemi Giriş")

    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):

        if kullanici in st.secrets["users"]:
            if st.secrets["users"][kullanici] == sifre:
                st.session_state.giris = True
                st.session_state.kullanici = kullanici
                st.rerun()
            else:
                st.error("Şifre yanlış")
        else:
            st.error("Kullanıcı bulunamadı")

    st.stop()
import pandas as pd

st.set_page_config(page_title="Stok Sistemi", layout="wide")

df = pd.read_excel("STOK.xlsx", sheet_name="STOK")
df.columns = df.columns.str.strip()

df["TEL"] = df["TEL"].astype(str).str.strip()
df["CİNS"] = df["CİNS"].astype(str).str.strip()

df = df.dropna(subset=["TEL", "CİNS"])
df.columns = df.columns.str.strip()

st.title("📦 Stok Sorgulama")

secili_tel = st.selectbox("TEL Seç", sorted(df["TEL"].unique()))
filtered_cins = df[df["TEL"] == secili_tel]["CİNS"].unique()
secili_cins = st.selectbox("CİNS Seç", sorted(filtered_cins))

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