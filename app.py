import streamlit as st
import pandas as pd
import datetime
import time

# ==============================
# 📦 SAYFA AYARI
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

# 30 dakika timeout
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

                with open("log.txt", "a") as f:
                    f.write(f"{datetime.datetime.now()} - {kullanici} giriş yaptı\n")

                st.rerun()
            else:
                st.error("Şifre yanlış")
        else:
            st.error("Kullanıcı bulunamadı")

    st.stop()

# Süre yenile
st.session_state.son_aktif = time.time()

# ==============================
# 📋 SIDEBAR
# ==============================

st.sidebar.success(f"Kullanıcı: {st.session_state.kullanici}")
st.sidebar.info(f"Rol: {st.session_state.rol}")

if st.sidebar.button("Çıkış Yap"):
    st.session_state.giris = False
    st.rerun()

# Admin panel
if st.session_state.rol == "admin":
    st.sidebar.markdown("---")
    st.sidebar.title("Admin Paneli")

    if st.sidebar.button("Logları Gör"):
        try:
            with open("log.txt", "r") as f:
                st.text(f.read())
        except:
            st.warning("Henüz log yok.")

# ==============================
# 📊 VERİ YÜKLEME (GITHUB EXCEL)
# ==============================

st.set_page_config(page_title="Stok Sistemi", layout="wide")

df = pd.read_excel("STOK.xlsx", sheet_name="STOK")
df.columns = df.columns.str.strip()

df = load_data()

# String dönüşüm
df["TEL"] = df["TEL"].astype(str)
df["CİNS"] = df["CİNS"].astype(str)

# ==============================
# 📦 STOK SORGULAMA
# ==============================

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

# ==============================
# 📋 SONUÇ KART
# ==============================

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