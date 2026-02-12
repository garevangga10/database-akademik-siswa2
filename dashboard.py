import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

# ===================================
# PAGE CONFIG
# ===================================
st.set_page_config(
    page_title="Database Akademik Siswa",
    layout="wide",
    page_icon="🎓"
)

# ===================================
# SUPABASE CONNECTION
# ===================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===================================
# LOGIN SYSTEM
# ===================================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "siswa": {"password": "siswa123", "role": "siswa"}
}

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("## 🔐 LOGIN DATABASE AKADEMIK")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.login = True
            st.session_state.role = users[username]["role"]
            st.rerun()
        else:
            st.error("Login salah")

    st.stop()

# ===================================
# LOAD DATA (SAFE VERSION)
# ===================================
def load_data():
    try:
        # GANTI INI SESUAI NAMA TABEL KAMU
        res = supabase.table("siswa").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error("Gagal memuat data:")
        st.write(e)
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Database kosong atau gagal dimuat.")
    st.stop()

# Pastikan kolom sesuai
if "nilai" not in df.columns:
    st.error("Kolom 'nilai' tidak ditemukan di database.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===================================
# HEADER
# ===================================
st.title("🎓 DATABASE AKADEMIK SISWA")
st.divider()

# ===================================
# METRICS
# ===================================
c1,c2,c3 = st.columns(3)

c1.metric("Total", len(df))
c2.metric("Lulus", (df['status']=='Lulus').sum())
c3.metric("Tidak Lulus", (df['status']=='Tidak Lulus').sum())

st.divider()

# ===================================
# TABLE
# ===================================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===================================
# ADMIN PANEL
# ===================================
if st.session_state.role == "admin":

    st.subheader("➕ Tambah Data")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("Simpan"):
        supabase.table("siswa").insert({"nama": nama, "nilai": nilai}).execute()
        st.success("Data ditambahkan")
        time.sleep(1)
        st.rerun()

    st.subheader("🗑️ Hapus Data")

    pilih = st.selectbox("Pilih ID", df["id"])

    if st.button("Hapus"):
        supabase.table("siswa").delete().eq("id", pilih).execute()
        st.warning("Data dihapus")
        time.sleep(1)
        st.rerun()

# ===================================
# GRAPH
# ===================================
st.subheader("📊 Grafik Interaktif")

fig = px.bar(df, x="nama", y="nilai", color="status")
st.plotly_chart(fig, use_container_width=True)

if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
