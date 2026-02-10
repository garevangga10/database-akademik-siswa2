import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Database Akademik Siswa MAS Al-Hamidiyah",
    page_icon="📚",
    layout="wide"
)

# =========================
# STYLE ESTETIK + ANIMASI
# =========================
st.markdown("""
<style>
@keyframes slide {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.running-text {
    font-size: 34px;
    font-weight: 900;
    white-space: nowrap;
    color: #38bdf8;
    animation: slide 14s linear infinite;
}
.line {
    height: 6px;
    border-radius: 10px;
    background: linear-gradient(90deg, #22c55e, #3b82f6, #a855f7);
    margin: 15px 0 25px 0;
}
.card {
    padding: 18px;
    border-radius: 18px;
    background: #0f172a;
    text-align: center;
    box-shadow: 0 0 18px rgba(56,189,248,0.4);
}
.card h3 {
    color: #60a5fa;
}
.card p {
    font-size: 30px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# KONEKSI GOOGLE SHEETS (SECRETS)
# =========================
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPE
)

client = gspread.authorize(creds)

# GANTI DENGAN SHEET ID KAMU
SHEET_ID = "1-vRO7H8T2yZjlObE-t-BApmaYrreR6qc_LvrC2smeWg"

sheet = client.open_by_key(SHEET_ID).sheet1

# =========================
# FUNGSI DATA
# =========================
def load_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def save_data(df):
    sheet.clear()
    sheet.update([df.columns.tolist()] + df.values.tolist())

# =========================
# LOAD DATA
# =========================
df = load_data()

if df.empty:
    df = pd.DataFrame(columns=["Nama", "Nilai"])

df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📚 MENU")
menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📋 Data Siswa", "✏️ CRUD Data", "📊 Grafik"]
)

st.sidebar.divider()
ambang = st.sidebar.slider("🎯 Ambang Kelulusan", 0, 100, 75)

df["Status"] = df["Nilai"].apply(
    lambda x: "Lulus" if x >= ambang else "Tidak Lulus"
)

# =========================
# METRIK
# =========================
total = len(df)
lulus = (df["Status"] == "Lulus").sum()
tidak = (df["Status"] == "Tidak Lulus").sum()
rata = df["Nilai"].mean() if total > 0 else 0

# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":
    st.markdown(
        "<div class='running-text'>📚 DATABASE AKADEMIK SISWA MAS AL-HAMIDIYAH 📚</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><h3>Total Siswa</h3><p>{total}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><h3>Lulus</h3><p>{lulus}</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><h3>Tidak Lulus</h3><p>{tidak}</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><h3>Rata-rata</h3><p>{rata:.1f}</p></div>", unsafe_allow_html=True)

    st.success("✅ Data tersimpan permanen di Google Sheets")

# =========================
# DATA SISWA
# =========================
elif menu == "📋 Data Siswa":
    st.title("📋 Data Siswa")
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

# =========================
# CRUD DATA
# =========================
elif menu == "✏️ CRUD Data":
    st.title("✏️ Tambah / Edit / Hapus Data")
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)

    st.subheader("➕ Tambah Data")
    nama = st.text_input("Nama Siswa")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("💾 Simpan Data"):
        if nama.strip() == "":
            st.warning("Nama tidak boleh kosong")
        else:
            df.loc[len(df)] = [nama, nilai]
            save_data(df)
            st.success("Data berhasil ditambahkan")
            st.rerun()

    st.divider()

    if total > 0:
        st.subheader("✏️ Edit / 🗑️ Hapus Data")
        pilih = st.selectbox("Pilih Siswa", df["Nama"].tolist())
        data = df[df["Nama"] == pilih].iloc[0]

        nilai_edit = st.number_input(
            "Edit Nilai",
            0, 100,
            int(data["Nilai"])
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Update"):
                df.loc[df["Nama"] == pilih, "Nilai"] = nilai_edit
                save_data(df)
                st.success("Data diperbarui")
                st.rerun()

        with col2:
            if st.button("🗑️ Hapus"):
                df = df[df["Nama"] != pilih]
                save_data(df)
                st.warning("Data dihapus")
                st.rerun()

# =========================
# GRAFIK
# =========================
elif menu == "📊 Grafik":
    st.title("📊 Visualisasi Data")
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)

    g1, g2 = st.columns(2)

    with g1:
        fig, ax = plt.subplots()
        ax.bar(df["Nama"], df["Nilai"], color="#3b82f6")
        ax.axhline(ambang, color="red", linestyle="--", label="Ambang")
        ax.legend()
        st.pyplot(fig)

    with g2:
        fig2, ax2 = plt.subplots()
        ax2.pie(
            [lulus, tidak],
            labels=["Lulus", "Tidak Lulus"],
            colors=["#22c55e", "#ef4444"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax2.axis("equal")
        st.pyplot(fig2)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("✨ Database Akademik Siswa MAS Al-Hamidiyah | Streamlit + Google Sheets")

