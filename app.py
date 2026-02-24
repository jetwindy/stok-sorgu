import streamlit as st
import pandas as pd
import datetime
import time


if "giris" not in st.session_state:
    st.session_state.giris = False
    st.session_state.kullanici = ""
    st.session_state.rol = ""
    st.session_state.son_aktif = time.time()


if st.session_state.giris:
    if time.time() - st.session_state.son_aktif > 1800:
        st.session_state.giris = False
        st.warning("Oturum süresi doldu. Tekrar giriş yapın.")
        st.stop()


if not st.session_state.giris:

    st.title("🔐 Stok Sistemi Giriş")

    kullanici = st.text_input("Kullanıcı Adı")
    sifre = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):

        if kullanici in st.secrets["users"]:
            if st.secrets["users"][kullanici] == sifre:
                st.session_state.giris = True
                st.session_state.kullanici = kullanici
                st.session_state.rol = st.secrets["roles"][kullanici]
                st.session_state.son_aktif = time.time()

                # LOG KAYDI
                with open("log.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()} - {kullanici} giriş yaptı\n")

                st.rerun()
            else:
                st.error("Şifre yanlış")
        else:
            st.error("Kullanıcı bulunamadı")

    st.stop()


st.session_state.son_aktif = time.time()


st.sidebar.success(f"Kullanıcı: {st.session_state.kullanici}")
st.sidebar.info(f"Rol: {st.session_state.rol}")

if st.sidebar.button("Çıkış Yap"):
    st.session_state.giris = False
    st.rerun()

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