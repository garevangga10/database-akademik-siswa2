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
# SUPER UI STYLE
# ===================================
st.markdown("""
<style>

/* ===== WELCOME CONTAINER ===== */
.welcome-container {
    position: relative;
    width: 100%;
    height: 80px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ===== MOVING TEXT ===== */
.welcome-text {
    position: absolute;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 4px;
    white-space: nowrap;
    background: linear-gradient(90deg, #22d3ee, #3b82f6, #a855f7, #22d3ee);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: 
        slideMove 12s linear infinite,
        shimmer 4s ease-in-out infinite,
        glowPulse 2s ease-in-out infinite alternate;
}

/* ===== SLIDE LEFT TO RIGHT ===== */
@keyframes slideMove {
    0% { transform: translateX(-60%); }
    100% { transform: translateX(60%); }
}

/* ===== SHIMMER EFFECT ===== */
@keyframes shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}

/* ===== GLOW EFFECT ===== */
@keyframes glowPulse {
    from { text-shadow: 0 0 10px #22d3ee; }
    to { text-shadow: 0 0 35px #3b82f6; }
}

/* ===== SPARKLE ===== */
.sparkle {
    position: absolute;
    width: 6px;
    height: 6px;
    background: white;
    border-radius: 50%;
    animation: sparkleAnim 3s infinite ease-in-out;
    opacity: 0.8;
}

.sparkle:nth-child(1) { top: 10px; left: 20%; animation-delay: 0s; }
.sparkle:nth-child(2) { top: 50px; left: 40%; animation-delay: 1s; }
.sparkle:nth-child(3) { top: 20px; left: 70%; animation-delay: 2s; }

@keyframes sparkleAnim {
    0% { transform: scale(0.5); opacity: 0; }
    50% { transform: scale(1.5); opacity: 1; }
    100% { transform: scale(0.5); opacity: 0; }
}


/* ANIMATED BACKGROUND */
body {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #0ea5e9, #1e293b);
    background-size: 400% 400%;
    animation: gradientMove 15s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* GLASS EFFECT */
.glass {
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.07);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 0 40px rgba(0,255,255,0.2);
}

/* TITLE */
.main-title {
    font-size: 45px;
    font-weight: 900;
    text-align: center;
    color: #38bdf8;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {text-shadow: 0 0 10px #38bdf8;}
    to {text-shadow: 0 0 30px #22d3ee;}
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    color:white;
    border-radius:15px;
    padding:10px 25px;
    border:none;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.05);
    box-shadow:0 0 20px #38bdf8;
}

/* CARD */
.card {
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.08);
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow: 0 0 30px rgba(0,255,255,0.15);
    transition:0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 50px rgba(0,255,255,0.4);
}

/* LOGIN BACKGROUND */
.login-bg {
    background: radial-gradient(circle at center,#0ea5e9 0%,#0f172a 70%);
    padding:50px;
    border-radius:30px;
    box-shadow:0 0 60px rgba(0,255,255,0.4);
}

</style>
""", unsafe_allow_html=True)

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
    st.markdown("<div class='login-bg'>", unsafe_allow_html=True)
    st.markdown("""
<div class="welcome-container">
    <div class="welcome-text">✨ WELCOME TO AHA WEBSITE ✨</div>
    <div class="sparkle"></div>
    <div class="sparkle"></div>
    <div class="sparkle"></div>
</div>
""", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>🔐 LOGIN DATABASE AKADEMIK</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.login = True
            st.session_state.role = users[username]["role"]
            st.success("Login berhasil 🚀")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Login salah")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ===================================
# LOAD DATA
# ===================================
def load_data():
    res = supabase.table("database-akademik-siswa").select("*").execute()
    return pd.DataFrame(res.data)

def insert_data(nama, nilai):
    supabase.table("database-akademik-siswa").insert({
        "nama": nama,
        "nilai": nilai
    }).execute()

def delete_data(id):
    supabase.table("database-akademik-siswa").delete().eq("id", id).execute()

df = load_data()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===================================
# HEADER
# ===================================
st.markdown("<div class='main-title'>🎓 DATABASE AKADEMIK SISWA</div>", unsafe_allow_html=True)
st.divider()

# ===================================
# METRICS
# ===================================
c1,c2,c3 = st.columns(3)

c1.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

st.divider()

# ===================================
# DATA TABLE
# ===================================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===================================
# ADMIN PANEL
# ===================================
if st.session_state.role == "admin":
    st.divider()
    st.subheader("⚙️ Panel Admin")

    nama = st.text_input("Nama Baru")
    nilai = st.number_input("Nilai Baru", 0, 100, 0)

    if st.button("Tambah Data"):
        insert_data(nama, nilai)
        st.success("Data ditambahkan 🚀")
        time.sleep(1)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        delete_data(id_hapus)
        st.warning("Data dihapus")
        time.sleep(1)
        st.rerun()

# ===================================
# INTERACTIVE CHART
# ===================================
st.divider()
st.subheader("📊 Grafik Interaktif")

fig = px.bar(
    df,
    x="nama",
    y="nilai",
    color="status",
    template="plotly_dark",
    title="Grafik Nilai Siswa"
)

st.plotly_chart(fig, use_container_width=True)

# ===================================
# AUTO REFRESH
# ===================================
st.caption("Auto refresh setiap 30 detik")
time.sleep(30)
st.rerun()

