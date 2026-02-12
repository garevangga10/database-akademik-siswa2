import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

st.set_page_config(page_title="AL-HAMIDIYAH SYSTEM", layout="wide")

# ===============================
# CONNECT SUPABASE
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
# LOGIN / REGISTER PAGE
# ===============================
if not st.session_state.user:

    st.title("🔐 AL-HAMIDIYAH SYSTEM")

    tab1, tab2 = st.tabs(["Login", "Daftar"])

    # ================= LOGIN =================
    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if res.user:
                    st.session_state.user = res.user
                    st.success("Login berhasil 🚀")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Login gagal")

            except Exception:
                st.error("Email atau password salah")

    # ================= REGISTER =================
    with tab2:
        email_reg = st.text_input("Email Baru")
        password_reg = st.text_input("Password Baru", type="password")

        if st.button("Daftar Akun"):

            if len(password_reg) < 6:
                st.error("Password minimal 6 karakter")
            else:
                try:
                    res = supabase.auth.sign_up({
                        "email": email_reg,
                        "password": password_reg
                    })

                    if res.user:
                        st.success("Akun berhasil dibuat 🎉 Silakan login.")
                    else:
                        st.error("Gagal daftar akun")

                except Exception:
                    st.error("Email sudah terdaftar atau Auth belum diaktifkan.")

    st.stop()

# ===============================
# LOAD DATA
# ===============================
def load_data():
    try:
        res = supabase.table("database-akademik-siswa").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception:
        return pd.DataFrame()

def insert_data(nama, nilai):
    supabase.table("database-akademik-siswa").insert({
        "nama": nama,
        "nilai": nilai
    }).execute()

def delete_data(id):
    supabase.table("database-akademik-siswa").delete().eq("id", id).execute()

df = load_data()

if df.empty:
    st.warning("Database kosong atau gagal dimuat.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===============================
# DASHBOARD
# ===============================
st.title("🚀 DASHBOARD DATABASE AL-HAMIDIYAH")
st.caption(f"Login sebagai: {st.session_state.user.email}")
st.divider()

# ===============================
# METRICS
# ===============================
c1, c2, c3 = st.columns(3)

c1.metric("Total", len(df))
c2.metric("Lulus", (df['status'] == 'Lulus').sum())
c3.metric("Tidak Lulus", (df['status'] == 'Tidak Lulus').sum())

st.divider()

# ===============================
# DATA TABLE
# ===============================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===============================
# ADMIN CHECK (EMAIL ADMIN)
# ===============================
ADMIN_EMAIL = "admin@gmail.com"

if st.session_state.user.email == ADMIN_EMAIL:

    st.subheader("⚙️ Admin Panel")

    nama = st.text_input("Nama Baru")
    nilai = st.number_input("Nilai Baru", 0, 100, 0)

    if st.button("Tambah Data"):
        insert_data(nama, nilai)
        st.success("Data ditambahkan")
        time.sleep(1)
        st.rerun()

    id_hapus = st.number_input("ID Hapus", 0, 1000, 0)

    if st.button("Hapus Data"):
        delete_data(id_hapus)
        st.warning("Data dihapus")
        time.sleep(1)
        st.rerun()

else:
    st.info("Anda login sebagai siswa (hanya bisa melihat data)")

# ===============================
# CHART
# ===============================
st.subheader("📊 Grafik Interaktif")

fig = px.bar(
    df,
    x="nama",
    y="nilai",
    color="status",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# LOGOUT
# ===============================
if st.button("Logout"):
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()
