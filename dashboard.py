import streamlit as st
import pandas as pd
from supabase import create_client
import time

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Dashboard Akademik Siswa",
    page_icon="📊",
    layout="wide"
)

# =============================
# SUPABASE CONNECT
# =============================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_ANON_KEY"]
)

# =============================
# STYLE (GLASS + NEON)
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
}
.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 0 20px rgba(56,189,248,0.4);
}
.neon {
    color: #38bdf8;
    text-shadow: 0 0 10px #38bdf8;
}
.blink {
    animation: blink 1.5s infinite;
}
@keyframes blink {
    0% {opacity:1;}
    50% {opacity:0.3;}
    100% {opacity:1;}
}
</style>
""", unsafe_allow_html=True)

# =============================
# LOGIN SYSTEM
# =============================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = None

def login_page():
    st.markdown("<h1 class='neon'>🔐 LOGIN SISTEM</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # LOGIN SEDERHANA (NANTI BISA DIGANTI AUTH SUPABASE)
        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.success("Login Admin berhasil")
            time.sleep(1)
            st.rerun()
        elif username == "siswa" and password == "siswa123":
            st.session_state.login = True
            st.session_state.role = "siswa"
            st.success("Login Siswa berhasil")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Username / Password salah")

if not st.session_state.login:
    login_page()
    st.stop()

# =============================
# LOAD DATA
# =============================
def load_data():
    data = supabase.table("database-akademik-siswa").select("*").execute()
    return pd.DataFrame(data.data)

df = load_data()

# =============================
# SIDEBAR
# =============================
st.sidebar.markdown("## 📚 MENU")
menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📋 Data Siswa", "✏️ Kelola Data"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"👤 Role: **{st.session_state.role}**")

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.session_state.role = None
    st.rerun()

# =============================
# DASHBOARD
# =============================
if menu == "🏠 Dashboard":
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown("<h1 class='neon blink'>📊 DASHBOARD AKADEMIK SISWA</h1>", unsafe_allow_html=True)

    total = len(df)
    rata = df["nilai"].mean() if total > 0 else 0

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Siswa", total)
    with c2:
        st.metric("Rata-rata Nilai", round(rata, 2))

    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# DATA SISWA
# =============================
elif menu == "📋 Data Siswa":
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("📋 Data Nilai Siswa")
    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# CRUD (ADMIN ONLY)
# =============================
elif menu == "✏️ Kelola Data":
    if st.session_state.role != "admin":
        st.error("⛔ Hanya admin yang boleh mengelola data")
        st.stop()

    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.subheader("✏️ Tambah Data Siswa")

    nama = st.text_input("Nama Siswa")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("💾 Simpan"):
        supabase.table("database-akademik-siswa").insert({
            "nama": nama,
            "nilai": nilai
        }).execute()
        st.success("Data berhasil ditambahkan")
        time.sleep(1)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
