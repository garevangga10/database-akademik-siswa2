import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px
import time

# =========================================
# CONFIG PAGE
# =========================================
st.set_page_config(page_title="AHA Academic System", layout="wide")

# =========================================
# PREMIUM UI STYLE
# =========================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #020617, #0f172a, #111827, #0a0f2c);
    background-size: 400% 400%;
    animation: gradientMove 20s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.welcome-container {
    text-align: center;
    margin-top: 20px;
}

.welcome-text {
    font-size: 30px;
    font-weight: 900;
    background: linear-gradient(90deg,#22d3ee,#3b82f6,#a855f7,#22d3ee);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 6s linear infinite;
}

@keyframes shimmer {
    0% {background-position: 0%;}
    100% {background-position: 200%;}
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,255,0.2);
}

.metric-card h2 {
    color: #22d3ee;
    font-size: 32px;
}

div.stButton > button {
    background: linear-gradient(90deg,#3b82f6,#22d3ee);
    border-radius: 12px;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    box-shadow: 0 0 20px #22d3ee;
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# =========================================
# CONNECT SUPABASE (STABLE)
# =========================================
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    supabase = create_client(url, key)
    CONNECTED = True
except:
    CONNECTED = False

# =========================================
# LOGIN SYSTEM
# =========================================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-text">✨ WELCOME TO AHA WEBSITE ✨</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🔐 LOGIN DATABASE AKADEMIK")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.rerun()
        elif username == "siswa" and password == "siswa123":
            st.session_state.login = True
            st.session_state.role = "siswa"
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()

# =========================================
# LOAD DATA (SAFE VERSION)
# =========================================
def load_data():
    if not CONNECTED:
        return pd.DataFrame()

    try:
        res = supabase.table("siswa").select("*").execute()
        data = res.data
        if data:
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

df = load_data()

# =========================================
# MAIN DASHBOARD
# =========================================
st.markdown("""
<div class="welcome-container">
    <div class="welcome-text">📊 DATABASE AKADEMIK SISWA</div>
</div>
""", unsafe_allow_html=True)

if not CONNECTED:
    st.error("Supabase tidak terhubung.")
    st.stop()

if df.empty:
    st.warning("Database kosong atau gagal dimuat.")
    st.stop()

# Pastikan kolom ada
if "nilai" in df.columns:
    df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")
else:
    st.error("Kolom 'nilai' tidak ditemukan di database.")
    st.stop()

# =========================================
# METRICS
# =========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric-card'><h2>{len(df)}</h2><p>Total</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric-card'><h2>{(df['status']=='Lulus').sum()}</h2><p>Lulus</p></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='metric-card'><h2>{(df['status']=='Tidak Lulus').sum()}</h2><p>Tidak Lulus</p></div>", unsafe_allow_html=True)

st.divider()

# =========================================
# TABLE
# =========================================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

st.divider()

# =========================================
# ADMIN PANEL
# =========================================
if st.session_state.role == "admin":

    st.subheader("➕ Tambah Data")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("Simpan"):
        try:
            supabase.table("siswa").insert({"nama": nama, "nilai": nilai}).execute()
            st.success("Data ditambahkan")
            time.sleep(1)
            st.rerun()
        except:
            st.error("Gagal menambahkan data.")

    st.divider()

    st.subheader("🗑️ Hapus Data")

    pilih = st.selectbox("Pilih ID", df["id"])

    if st.button("Hapus"):
        try:
            supabase.table("siswa").delete().eq("id", pilih).execute()
            st.warning("Data dihapus")
            time.sleep(1)
            st.rerun()
        except:
            st.error("Gagal menghapus data.")

# =========================================
# INTERACTIVE CHART
# =========================================
st.divider()
st.subheader("📈 Grafik Interaktif")

fig = px.bar(df, x="nama", y="nilai", color="status", text="nilai")
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.divider()

if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
