import streamlit as st
import pandas as pd

# =========================
# SAYFA AYARI (MOBİL UYUMLU)
# =========================
st.set_page_config(
    page_title="Stok Takip",
    page_icon="📦",
    layout="centered"
)

# =========================
# ŞİFRE
# =========================
PASSWORD = "1234"  # Burayı değiştirebilirsin

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 Giriş")

    password_input = st.text_input("Şifre", type="password")

    if st.button("Giriş Yap"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Hatalı şifre")

    st.stop()

# =========================
# EXCEL VERİSİ (GITHUB RAW)
# =========================
@st.cache_data(ttl=300)
def load_data():
    url = "https://github.com/jetwindy/stok-sorgu/raw/main/STOK.xlsx"
    df = pd.read_excel(url, sheet_name="STOK")

    # Kolon isimlerini temizle
    df.columns = df.columns.str.strip()

    # Sayısal kolonları düzelt
    numeric_cols = ["ELSAN", "HES", "ERİKOĞLU", "EMSAN", "KAVİ", "EMTEL", "TOPLAM"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

# =========================
# SIDEBAR MENÜ (MOBİL İÇİN)
# =========================
menu = st.sidebar.radio(
    "📌 Menü",
    ["📊 Dashboard", "📦 Stok Sorgula"]
)

# =========================
# DASHBOARD
# =========================
if menu == "📊 Dashboard":

    st.title("📊 Genel Dashboard")

    toplam_stok = int(df["TOPLAM"].sum())
    st.metric("Genel Toplam Stok", toplam_stok)

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

    marka_df = pd.DataFrame(
        list(marka_toplam.items()),
        columns=["Marka", "Toplam"]
    )

    st.bar_chart(marka_df.set_index("Marka"), use_container_width=True)

# =========================
# STOK SORGULAMA
# =========================
elif menu == "📦 Stok Sorgula":

    st.title("📦 Stok Sorgulama")

    # TEL seçimi
    secili_tel = st.selectbox(
        "TEL Seç",
        sorted(df["TEL"].astype(str).unique())
    )

    # CİNS seçimi
    secili_cins = st.selectbox(
        "CİNS Seç",
        sorted(df[df["TEL"].astype(str) == secili_tel]["CİNS"].unique())
    )

    # Filtreleme
    sonuc = df[
        (df["TEL"].astype(str) == secili_tel) &
        (df["CİNS"] == secili_cins)
    ]

    if not sonuc.empty:

        st.divider()
        st.subheader("📋 Sonuç")

        satir = sonuc.iloc[0]

        st.write(f"**RAF NO:** {satir['RAF NO']}")
        st.write(f"**ELSAN:** {int(satir['ELSAN'])}")
        st.write(f"**HES:** {int(satir['HES'])}")
        st.write(f"**ERİKOĞLU:** {int(satir['ERİKOĞLU'])}")
        st.write(f"**EMSAN:** {int(satir['EMSAN'])}")
        st.write(f"**KAVİ:** {int(satir['KAVİ'])}")
        st.write(f"**EMTEL:** {int(satir['EMTEL'])}")
        st.write(f"**TOPLAM:** {int(satir['TOPLAM'])}")

    else:
        st.warning("Kayıt bulunamadı.")