import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes
import os

# =========================
# SAYFA AYARI
# =========================
st.set_page_config(page_title="Stok Yönetim", page_icon="📦", layout="centered")

# =========================
# KULLANICILAR
# =========================
USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "ufuk": {"password": "1998", "role": "user"},
    "burak": {"password": "2000", "role": "user"},
    "ali": {"password": "2005", "role": "user"},
    "recep": {"password": "1976", "role": "user"},
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None

# =========================
# LOGIN
# =========================
if not st.session_state.authenticated:
    st.title("🔐 Kullanıcı Girişi")

    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.session_state.role = USERS[username]["role"]
            st.rerun()
        else:
            st.error("Hatalı giriş")

    st.stop()

# =========================
# VERİ YÜKLE
# =========================
@st.cache_data(ttl=300)
def load_data():
    url = "https://github.com/jetwindy/stok-sorgu/raw/main/STOK.xlsx"
    df = pd.read_excel(url, sheet_name="STOK")
    df.columns = df.columns.str.strip()

    numeric_cols = ["ELSAN", "HES", "ERİKOĞLU", "EMSAN", "KAVİ", "EMTEL", "TOPLAM"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# =========================
# LOG DOSYASI
# =========================
LOG_FILE = "log.csv"

def log_kaydet(islem, detay):
    log_df = pd.DataFrame([{
        "Tarih": datetime.now(),
        "Kullanıcı": st.session_state.user,
        "İşlem": islem,
        "Detay": detay
    }])

    if os.path.exists(LOG_FILE):
        eski = pd.read_csv(LOG_FILE)
        yeni = pd.concat([eski, log_df], ignore_index=True)
        yeni.to_csv(LOG_FILE, index=False)
    else:
        log_df.to_csv(LOG_FILE, index=False)

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📌 Menü",
    ["📦 Stok Sorgula", "📊 Dashboard", "📁 Log Kayıtları"] +
    (["🛠 Admin Panel"] if st.session_state.role == "admin" else [])
)

st.sidebar.write(f"👤 {st.session_state.user}")
if st.sidebar.button("Çıkış Yap"):
    st.session_state.authenticated = False
    st.rerun()

# =========================
# DASHBOARD
# =========================
if menu == "📊 Dashboard":

    st.title("📊 Genel Dashboard")

    st.metric("Genel Toplam Stok", int(df["TOPLAM"].sum()))

    st.divider()
    st.subheader("🏷 Marka Dağılımı")

    marka_toplam = {
        "ELSAN": df["ELSAN"].sum(),
        "HES": df["HES"].sum(),
        "ERİKOĞLU": df["ERİKOĞLU"].sum(),
        "EMSAN": df["EMSAN"].sum(),
        "KAVİ": df["KAVİ"].sum(),
        "EMTEL": df["EMTEL"].sum(),
    }

    chart_df = pd.DataFrame(
        list(marka_toplam.items()),
        columns=["Marka", "Toplam"]
    )

    st.pyplot(
        chart_df.set_index("Marka").plot.pie(
            y="Toplam",
            autopct='%1.1f%%',
            figsize=(5,5)
        ).figure
    )

# =========================
# STOK SORGULA
# =========================
elif menu == "📦 Stok Sorgula":

    st.title("📦 Stok Sorgulama")

    tel = st.selectbox("TEL", sorted(df["TEL"].astype(str).unique()))
    cins = st.selectbox(
        "CİNS",
        sorted(df[df["TEL"].astype(str) == tel]["CİNS"].unique())
    )

    sonuc = df[
        (df["TEL"].astype(str) == tel) &
        (df["CİNS"] == cins)
    ]

    if not sonuc.empty:

        satir = sonuc.iloc[0]

        st.markdown("### 📋 Sonuç Kartı")
        st.dataframe(sonuc, use_container_width=True)

        log_kaydet("Sorgulama", f"{tel} - {cins}")

        # PDF Export
        if st.button("📄 PDF İndir"):

            file_path = "stok_rapor.pdf"
            doc = SimpleDocTemplate(file_path, pagesize=pagesizes.A4)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph("Stok Raporu", styles["Heading1"]))
            elements.append(Spacer(1, 12))

            data = [list(sonuc.columns)] + sonuc.values.tolist()
            table = Table(data)
            table.setStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ])

            elements.append(table)
            doc.build(elements)

            with open(file_path, "rb") as f:
                st.download_button(
                    "PDF Dosyasını İndir",
                    f,
                    file_name="stok_rapor.pdf"
                )

    else:
        st.warning("Kayıt bulunamadı")

# =========================
# LOG
# =========================
elif menu == "📁 Log Kayıtları":

    st.title("📁 Günlük İşlem Kayıtları")

    if os.path.exists(LOG_FILE):
        log_df = pd.read_csv(LOG_FILE)
        st.dataframe(log_df, use_container_width=True)
    else:
        st.info("Henüz kayıt yok")

# =========================
# ADMIN PANEL
# =========================
elif menu == "🛠 Admin Panel":

    st.title("🛠 Admin Panel")

    st.write("Toplam Kullanıcı:", len(USERS))

    st.write("### Kullanıcılar")
    st.json(USERS)