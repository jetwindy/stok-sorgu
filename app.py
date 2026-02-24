import streamlit as st
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt

# ==============================
# 📱 SAYFA AYARI
# ==============================

st.set_page_config(
    page_title="Stok Sistemi",
    page_icon="📦",
    layout="centered"
)

# ==============================
# 🔐 SESSION
# ==============================

if "giris" not in st.session_state:
    st.session_state.giris = False
    st.session_state.kullanici = ""
    st.session_state.rol = ""
    st.session_state.son_aktif = time.time()

# Timeout
if st.session_state.giris:
    if time.time() - st.session_state.son_aktif > 1800:
        st.session_state.giris = False
        st.warning("Oturum süresi doldu.")
        st.stop()

# ==============================
# 🔐 LOGIN
# ==============================

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

                st.rerun()
            else:
                st.error("Şifre yanlış")
        else:
            st.error("Kullanıcı bulunamadı")

    st.stop()

st.session_state.son_aktif = time.time()

# ==============================
# 📊 VERİ YÜKLEME (GITHUB)
# ==============================

@st.cache_data(ttl=60)
def load_data():
    url = "https://raw.githubusercontent.com/jetwindy/stok-sorgu/main/STOK.xlsx"
    df = pd.read_excel(url, sheet_name="STOK")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

df["TEL"] = df["TEL"].astype(str)
df["CİNS"] = df["CİNS"].astype(str)

# ==============================
# 📱 MOBİL MENÜ
# ==============================

menu = st.radio(
    "",
    ["📊 Dashboard", "📦 Stok Sorgula"],
    horizontal=True
)

# ==============================
# 📊 DASHBOARD
# ==============================

if menu == "📊 Dashboard":

    st.title("📊 Genel Dashboard")

    # Toplam stok
    toplam_stok = pd.to_numeric(df["TOPLAM"], errors="coerce").sum()

    st.metric("Genel Toplam Stok", int(toplam_stok))

    st.divider()

    st.subheader("🏷 Marka Dağılımı")

    marka_sutunlari = ["ELSAN", "HES", "ERİKOĞLU", "EMSAN", "KAVİ", "EMTEL"]

    marka_toplam = {}

    for marka in marka_sutunlari:
        marka_toplam[marka] = pd.to_numeric(df[marka], errors="coerce").sum()

    fig, ax = plt.subplots()
    ax.pie(marka_toplam.values(), labels=marka_toplam.keys(), autopct="%1.1f%%")
    ax.axis("equal")

    st.pyplot(fig)

# ==============================
# 📦 STOK SORGULAMA
# ==============================

if menu == "📦 Stok Sorgula":

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