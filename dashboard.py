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
# PREMIUM CSS + ANIMATION
# ===================================
st.markdown("""
<style>

/* GLOBAL SMOOTH */
* {
    transition: all 0.4s ease-in-out;
}

/* ANIMATED BACKGROUND */
body {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #0ea5e9, #1e293b);
    background-size: 400% 400%;
    animation: gradientMove 18s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* FADE IN */
.fade-in {
    animation: fadeIn 1s ease forwards;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

/* TITLE */
.main-title {
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#38bdf8,#22d3ee,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
}

@keyframes shimmer {
    0% {background-position: -500px;}
    100% {background-position: 500px;}
}

/* GLASS CARD */
.card {
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.07);
    padding:25px;
    border-radius:25px;
    text-align:center;
    box-shadow: 0 0 40px rgba(0,255,255,0.15);
}

.card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 0 60px rgba(0,255,255,0.4);
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#06b6d4);
    color:white;
    border-radius:20px;
    padding:12px 30px;
    border:none;
    font-weight:600;
}

.stButton>button:hover {
    transform:scale(1.07);
    box-shadow:0 0 25px #38bdf8;
}

/* LOGIN BG */
.login-bg {
    background: radial-gradient(circle at center,#0ea5e9 0%,#0f172a 70%);
    padding:60px;
    border-radius:40px;
    box-shadow:0 0 80px rgba(0,255,255,0.4);
}

</style>
""", unsafe_allow_html=True)

# ===================================
# SOUND FUNCTION
# ===================================
def play_sound(url):
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{url}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )

click_sound = "https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3"
success_sound = "https://assets.mixkit.co/active_storage/sfx/270/270-preview.mp3"

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

    st.markdown("<div class='login-bg fade-in'>", unsafe_allow_html=True)
    st.markdown("<div class='main-title'>🔐 LOGIN DATABASE AKADEMIK</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        play_sound(click_sound)

        if username in users and users[username]["password"] == password:
            play_sound(success_sound)
            st.session_state.login = True
            st.session_state.role = users[username]["role"]
            time.sleep(0.7)
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

if df.empty:
    st.warning("Database kosong.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===================================
# HEADER
# ===================================
st.markdown("<div class='main-title fade-in'>🎓 DATABASE AKADEMIK SISWA</div>", unsafe_allow_html=True)
st.divider()

# ===================================
# METRICS
# ===================================
c1,c2,c3 = st.columns(3)

c1.markdown(f"<div class='card fade-in'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card fade-in'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card fade-in'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

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
        play_sound(click_sound)
        insert_data(nama, nilai)
        play_sound(success_sound)
        time.sleep(0.7)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        play_sound(click_sound)
        delete_data(id_hapus)
        play_sound(success_sound)
        time.sleep(0.7)
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
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# ===================================
# LOGOUT
# ===================================
if st.button("Logout"):
    play_sound(click_sound)
    st.session_state.login = False
    st.rerun()
