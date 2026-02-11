import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

# ===============================
# CONFIG
# ===============================
st.set_page_config(
    page_title="Database Akademik Siswa",
    layout="wide",
    page_icon="📚"
)

# ===============================
# SUPABASE CONNECTION
# ===============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===============================
# STYLE SUPER UI
# ===============================
st.markdown("""
<style>

/* BACKGROUND */
body {
    background: radial-gradient(circle at top left, #1e293b, #0f172a 60%);
}

/* MOTIF HALUS */
body::before {
    content: "";
    position: fixed;
    width: 100%;
    height: 100%;
    background-image: radial-gradient(rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 25px 25px;
    opacity: 0.3;
    z-index: -1;
}

/* TITLE */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #38bdf8;
    text-align: center;
    margin-bottom: 10px;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #38bdf8; }
    to { text-shadow: 0 0 25px #22d3ee; }
}

/* RUNNING TEXT */
.marquee {
    white-space: nowrap;
    overflow: hidden;
    box-sizing: border-box;
}

.marquee span {
    display: inline-block;
    padding-left: 100%;
    animation: marquee 15s linear infinite;
    color: #94a3b8;
    font-weight: 500;
}

@keyframes marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-100%); }
}

/* GLASS CARD */
.card {
    backdrop-filter: blur(15px);
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 0 25px rgba(56,189,248,0.15);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 40px rgba(56,189,248,0.4);
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
}

/* TABLE */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03);
    border-radius: 15px;
    padding: 10px;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {
    .main-title {
        font-size: 28px;
    }
}

</style>
""", unsafe_allow_html=True)

# ===============================
# LOGIN SYSTEM
# ===============================
users = {
    "admin": {"password": "admin123", "role": "admin"},
    "siswa": {"password": "siswa123", "role": "siswa"}
}

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<div class='main-title'>🔐 LOGIN SISTEM</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.login = True
            st.session_state.role = users[username]["role"]
            st.success("Login berhasil!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()

# ===============================
# LOAD DATA
# ===============================
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
    st.warning("Belum ada data.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===============================
# HEADER
# ===============================
st.markdown("<div class='main-title'>📚 DATABASE AKADEMIK SISWA</div>", unsafe_allow_html=True)

st.markdown("""
<div class="marquee">
<span>✨ Sistem Akademik Modern • Supabase Cloud • Real-Time Data • MAS Al-Hamidiyah ✨</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ===============================
# METRIC CARDS
# ===============================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='card'>
        <h3>Total Siswa</h3>
        <h1>{len(df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='card'>
        <h3>Lulus</h3>
        <h1>{(df['status']=='Lulus').sum()}</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='card'>
        <h3>Tidak Lulus</h3>
        <h1>{(df['status']=='Tidak Lulus').sum()}</h1>
    </div>
    """, unsafe_allow_html=True)

# ===============================
# DATA TABLE
# ===============================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===============================
# ADMIN PANEL
# ===============================
if st.session_state.role == "admin":
    st.divider()
    st.subheader("⚙️ Panel Admin")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)

    colA, colB = st.columns(2)

    with colA:
        if st.button("Tambah Data"):
            insert_data(nama, nilai)
            st.success("Data ditambahkan!")
            time.sleep(1)
            st.rerun()

    with colB:
        id_hapus = st.number_input("ID Hapus", 0, 1000, 0)
        if st.button("Hapus Data"):
            delete_data(id_hapus)
            st.warning("Data dihapus!")
            time.sleep(1)
            st.rerun()

# ===============================
# INTERACTIVE GRAPH
# ===============================
st.divider()
st.subheader("📊 Grafik Interaktif")

fig = px.bar(
    df,
    x="nama",
    y="nilai",
    color="status",
    title="Grafik Nilai Siswa",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# AUTO REFRESH
# ===============================
st.caption("Auto refresh setiap 30 detik")
time.sleep(30)
st.rerun()

