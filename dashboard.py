import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

st.set_page_config(page_title="AL-HAMIDIYAH SYSTEM", layout="wide")

# ===============================
# STYLE GOD MODE
# ===============================
st.markdown("""
<style>
body {background:#0f172a;}
.main-title {
    font-size:50px;
    font-weight:900;
    text-align:center;
    background: linear-gradient(90deg,#38bdf8,#22d3ee,#3b82f6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.card {
    backdrop-filter: blur(20px);
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:25px;
    text-align:center;
    box-shadow:0 0 40px rgba(0,255,255,0.2);
}
.stButton>button {
    background:linear-gradient(90deg,#3b82f6,#06b6d4);
    border:none;
    border-radius:20px;
    padding:10px 25px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# SUPABASE CONNECT
# ===============================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===============================
# SESSION INIT
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

# ===============================
# LOGIN / REGISTER
# ===============================
if not st.session_state.user:

    st.markdown("<div class='main-title'>🔐 AL-HAMIDIYAH SYSTEM</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Daftar"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            res = supabase.table("users")\
                .select("*")\
                .eq("username", username)\
                .eq("password", password)\
                .execute()

            if len(res.data) > 0:
                st.session_state.user = res.data[0]
                st.success("Login berhasil 🚀")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Username atau password salah")

    # REGISTER
    with tab2:
        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")

        if st.button("Daftar"):
            try:
                supabase.table("users").insert({
                    "username": new_user,
                    "password": new_pass,
                    "role": "siswa"
                }).execute()

                st.success("Akun berhasil dibuat 🎉")
            except:
                st.error("Username sudah dipakai")

    st.stop()

# ===============================
# LOAD DATA SISWA
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
    st.warning("Database kosong")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===============================
# DASHBOARD
# ===============================
st.markdown("<div class='main-title'>🎓 DASHBOARD SISWA</div>", unsafe_allow_html=True)
st.caption(f"Login sebagai: {st.session_state.user['username']} ({st.session_state.user['role']})")
st.divider()

c1,c2,c3 = st.columns(3)

c1.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

st.divider()

st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===============================
# ADMIN PANEL
# ===============================
if st.session_state.user["role"] == "admin":

    st.subheader("⚙️ Admin Panel")

    nama = st.text_input("Nama Baru")
    nilai = st.number_input("Nilai Baru", 0, 100, 0)

    if st.button("Tambah Data"):
        insert_data(nama, nilai)
        st.success("Data ditambahkan")
        time.sleep(0.5)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        delete_data(id_hapus)
        st.warning("Data dihapus")
        time.sleep(0.5)
        st.rerun()
else:
    st.info("Mode Siswa (View Only)")

# ===============================
# CHART
# ===============================
st.subheader("📊 Grafik Nilai")

fig = px.bar(df, x="nama", y="nilai", color="status", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# ===============================
# LOGOUT
# ===============================
if st.button("Logout"):
    st.session_state.user = None
    st.rerun()
