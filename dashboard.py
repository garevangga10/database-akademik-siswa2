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

body {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.main-title {
    font-size:40px;
    font-weight:800;
    color:#38bdf8;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 10px #38bdf8; }
    to { text-shadow: 0 0 25px #22d3ee; }
}

.card {
    backdrop-filter: blur(12px);
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:20px;
    text-align:center;
    box-shadow: 0 0 25px rgba(56,189,248,0.3);
    margin-bottom:15px;
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
st.divider()

# ===============================
# METRIC CARDS
# ===============================
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><h3>Total</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><h3>Lulus</h3><h2>{(df['status']=='Lulus').sum()}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h2>{(df['status']=='Tidak Lulus').sum()}</h2></div>", unsafe_allow_html=True)

st.divider()

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
