import streamlit as st
import pandas as pd
from supabase import create_client

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Database Akademik Siswa",
    page_icon="📚",
    layout="wide"
)

TABLE_NAME = "siswa"

# =========================
# CONNECT SUPABASE (SAFE)
# =========================
def connect_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        return create_client(url, key)
    except Exception:
        return None

supabase = connect_supabase()

# =========================
# LOAD DATA (ANTI CRASH)
# =========================
def load_data():
    if supabase is None:
        return pd.DataFrame()

    try:
        res = supabase.table(TABLE_NAME).select("*").execute()
        return pd.DataFrame(res.data)
    except Exception:
        return pd.DataFrame()

df = load_data()

# =========================
# FALLBACK DATA (JIKA SUPABASE GAGAL)
# =========================
if df.empty:
    st.warning("⚠️ Supabase tidak terhubung. Menggunakan data sementara.")
    df = pd.DataFrame({
        "id": [1,2,3,4],
        "nama": ["Tegar","Andi","Siti","Budi"],
        "nilai": [90,78,85,60]
    })

# =========================
# STYLE
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#020617,#0f172a);
}
.title {
    font-size:38px;
    font-weight:900;
    color:#38bdf8;
    text-shadow:0 0 15px #38bdf8;
}
.card {
    background:rgba(15,23,42,.9);
    padding:20px;
    border-radius:16px;
    box-shadow:0 0 20px rgba(56,189,248,.4);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<div class='title'>🔐 LOGIN ADMIN</div>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Login salah")

    st.stop()

# =========================
# HEADER
# =========================
st.markdown("<div class='title'>📚 DATABASE AKADEMIK SISWA</div>", unsafe_allow_html=True)
st.divider()

# =========================
# STATUS
# =========================
df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

# =========================
# TABLE
# =========================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# =========================
# ADD DATA (HANYA JIKA SUPABASE AKTIF)
# =========================
if supabase is not None:
    st.subheader("➕ Tambah Data")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100)

    if st.button("Simpan"):
        try:
            supabase.table(TABLE_NAME).insert({
                "nama": nama,
                "nilai": nilai
            }).execute()
            st.success("Data ditambahkan")
            st.rerun()
        except Exception:
            st.error("Gagal menyimpan ke Supabase")
