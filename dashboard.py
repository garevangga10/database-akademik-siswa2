import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

st.set_page_config(page_title="GOD MODE AHA", layout="wide")

# =========================================
# 🌌 GOD MODE PARTICLE BACKGROUND
# =========================================
st.markdown("""
<style>
body {
    margin:0;
    background:#0f172a;
    overflow-x:hidden;
}

/* Particle canvas */
#particles-js {
    position:fixed;
    width:100%;
    height:100%;
    z-index:-1;
    top:0;
    left:0;
}

/* Glass Card */
.card {
    backdrop-filter: blur(25px);
    background: rgba(255,255,255,0.07);
    padding:30px;
    border-radius:30px;
    text-align:center;
    box-shadow:0 0 60px rgba(0,255,255,0.2);
    transition:0.4s;
}

.card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow:0 0 80px rgba(0,255,255,0.5);
}

/* Shimmer Title */
.main-title {
    font-size:55px;
    font-weight:900;
    text-align:center;
    background: linear-gradient(90deg,#38bdf8,#22d3ee,#3b82f6);
    background-size:200% auto;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: shimmer 5s linear infinite;
}

@keyframes shimmer {
    0% {background-position:0%;}
    100% {background-position:200%;}
}

/* Neon Buttons */
.stButton>button {
    background:linear-gradient(90deg,#3b82f6,#06b6d4);
    border:none;
    border-radius:25px;
    padding:14px 40px;
    color:white;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.1);
    box-shadow:0 0 40px #38bdf8;
}
</style>

<div id="particles-js"></div>

<script src="https://cdn.jsdelivr.net/npm/particles.js"></script>
<script>
particlesJS("particles-js", {
  particles: {
    number: { value: 60 },
    size: { value: 3 },
    color: { value: "#38bdf8" },
    line_linked: {
      enable: true,
      distance: 150,
      color: "#22d3ee",
      opacity: 0.4,
      width: 1
    },
    move: { enable: true, speed: 2 }
  }
});
</script>
""", unsafe_allow_html=True)

# =========================================
# 🎵 Ambient Background Music
# =========================================
st.markdown("""
<audio autoplay loop>
<source src="https://assets.mixkit.co/music/preview/mixkit-dreaming-big-31.mp3" type="audio/mp3">
</audio>
""", unsafe_allow_html=True)

# =========================================
# 🔊 SOUND EFFECT
# =========================================
def play_sound(url):
    st.markdown(f"""
    <audio autoplay>
        <source src="{url}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

click_sound = "https://assets.mixkit.co/active_storage/sfx/2568/2568-preview.mp3"
success_sound = "https://assets.mixkit.co/active_storage/sfx/270/270-preview.mp3"

# =========================================
# SUPABASE CONNECT
# =========================================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================================
# LOGIN SYSTEM
# =========================================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "siswa": {"password": "siswa123", "role": "siswa"}
}

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("<div class='main-title'> AL-HAMIDIYAH DATABASE  </div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        play_sound(click_sound)
        if username in users and users[username]["password"] == password:
            play_sound(success_sound)
            st.session_state.login = True
            st.session_state.role = users[username]["role"]
            time.sleep(0.6)
            st.rerun()
        else:
            st.error("Login salah")

    st.stop()

# =========================================
# LOAD DATA
# =========================================
def load_data():
    res = supabase.table("database-akademik-siswa").select("*").execute()
    return pd.DataFrame(res.data)

def insert_data(nama, nilai):
    supabase.table("database-akademik-siswa").insert({"nama": nama, "nilai": nilai}).execute()

def delete_data(id):
    supabase.table("database-akademik-siswa").delete().eq("id", id).execute()

df = load_data()

if df.empty:
    st.warning("Database kosong.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# =========================================
# HEADER
# =========================================
st.markdown("<div class='main-title'>DASHBOARD DATABASE AL-HAMIDIYAH</div>", unsafe_allow_html=True)
st.divider()

# =========================================
# METRICS
# =========================================
c1,c2,c3 = st.columns(3)

c1.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

st.divider()

# =========================================
# DATA TABLE
# =========================================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# =========================================
# ADMIN PANEL
# =========================================
if st.session_state.role == "admin":

    st.subheader("⚙️ Admin Panel")

    nama = st.text_input("Nama Baru")
    nilai = st.number_input("Nilai Baru", 0, 100, 0)

    if st.button("Tambah Data"):
        play_sound(click_sound)
        insert_data(nama, nilai)
        play_sound(success_sound)
        time.sleep(0.6)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        play_sound(click_sound)
        delete_data(id_hapus)
        play_sound(success_sound)
        time.sleep(0.6)
        st.rerun()

# =========================================
# INTERACTIVE CHART
# =========================================
st.subheader("📊 GOD MODE INTERACTIVE CHART")

fig = px.bar(
    df,
    x="nama",
    y="nilai",
    color="status",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================
# LOGOUT
# =========================================
if st.button("Logout"):
    play_sound(click_sound)
    st.session_state.login = False
    st.rerun()




