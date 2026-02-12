import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import hashlib
import time

st.set_page_config(page_title="AL-HAMIDIYAH PRO SYSTEM", layout="wide")

# ===============================
# STYLE RESPONSIVE
# ===============================
st.markdown("""
<style>
body {background:#0f172a;}
.main-title {
    font-size:45px;
    font-weight:900;
    text-align:center;
    background: linear-gradient(90deg,#38bdf8,#22d3ee,#3b82f6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}
.card {
    backdrop-filter: blur(15px);
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 0 30px rgba(0,255,255,0.2);
}
@media(max-width:768px){
    .main-title{font-size:28px;}
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
# PASSWORD HASH
# ===============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===============================
# SESSION INIT
# ===============================
if "user" not in st.session_state:
    st.session_state.user = None

# ===============================
# LOGIN / REGISTER
# ===============================
if not st.session_state.user:

    st.markdown("<div class='main-title'>🔐 AL-HAMIDIYAH PROFESSIONAL SYSTEM</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Daftar"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed = hash_password(password)

            res = supabase.table("users")\
                .select("*")\
                .eq("username", username)\
                .eq("password", hashed)\
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
                    "password": hash_password(new_pass),
                    "role": "siswa"
                }).execute()
                st.success("Akun berhasil dibuat 🎉")
            except:
                st.error("Username sudah dipakai")

    st.stop()

# ===============================
# LOAD DATA
# ===============================
def load_data():
    res = supabase.table("database-akademik-siswa").select("*").execute()
    return pd.DataFrame(res.data)

def insert_data(nama, nilai, username):
    supabase.table("database-akademik-siswa").insert({
        "nama": nama,
        "nilai": nilai,
        "username": username
    }).execute()

def delete_data(id):
    supabase.table("database-akademik-siswa").delete().eq("id", id).execute()

df = load_data()

if df.empty:
    st.warning("Database kosong")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===============================
# RANKING
# ===============================
df = df.sort_values(by="nilai", ascending=False)
df["ranking"] = range(1, len(df)+1)

# ===============================
# DASHBOARD
# ===============================
st.markdown("<div class='main-title'>🎓 DASHBOARD AKADEMIK</div>", unsafe_allow_html=True)
st.caption(f"Login sebagai: {st.session_state.user['username']} ({st.session_state.user['role']})")
st.divider()

# ===============================
# FILTER ROLE
# ===============================
if st.session_state.user["role"] == "siswa":
    df_view = df[df["username"] == st.session_state.user["username"]]
else:
    df_view = df

# ===============================
# METRICS
# ===============================
c1,c2,c3 = st.columns(3)

c1.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df_view)}</h1></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Rata-rata</h3><h1>{round(df_view['nilai'].mean(),1)}</h1></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>Ranking Tertinggi</h3><h1>{df_view['nilai'].max()}</h1></div>", unsafe_allow_html=True)

st.divider()

# ===============================
# DATA TABLE
# ===============================
st.subheader("📋 Data Siswa")
st.dataframe(df_view, use_container_width=True)

# ===============================
# ADMIN PANEL
# ===============================
if st.session_state.user["role"] == "admin":

    st.subheader("⚙️ Admin Panel")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)
    username_input = st.text_input("Username Pemilik Data")

    if st.button("Tambah Data"):
        insert_data(nama, nilai, username_input)
        st.success("Data ditambahkan")
        time.sleep(0.5)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        delete_data(id_hapus)
        st.warning("Data dihapus")
        time.sleep(0.5)
        st.rerun()

    # ROLE MANAGEMENT
    st.subheader("🔧 Role Management")

    users = supabase.table("users").select("*").execute().data
    user_df = pd.DataFrame(users)

    selected_user = st.selectbox("Pilih User", user_df["username"])
    new_role = st.selectbox("Role Baru", ["admin", "siswa"])

    if st.button("Update Role"):
        supabase.table("users").update({
            "role": new_role
        }).eq("username", selected_user).execute()
        st.success("Role diperbarui")
        time.sleep(0.5)
        st.rerun()

# ===============================
# CHART
# ===============================
st.subheader("📊 Grafik Ranking")

fig = px.bar(df_view, x="nama", y="nilai", color="status")
st.plotly_chart(fig, use_container_width=True)

# ===============================
# LOGOUT
# ===============================
if st.button("Logout"):
    st.session_state.user = None
    st.rerun()
