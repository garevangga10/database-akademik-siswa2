import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="AHA Academic System", layout="wide")

# CONNECT SUPABASE
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

# LOGIN SYSTEM
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.markdown("## 🔐 LOGIN DATABASE AKADEMIK")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.rerun()
        elif username == "siswa" and password == "siswa123":
            st.session_state.login = True
            st.session_state.role = "siswa"
            st.rerun()
        else:
            st.error("Username / Password salah")

    st.stop()

# LOAD DATA (SESUIA NAMA TABEL KAMU)
def load_data():
    try:
        res = supabase.table("database-akademik-siswa").select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error("Error Supabase:")
        st.write(e)
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Database kosong atau gagal dimuat.")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

st.title("📊 DATABASE AKADEMIK SISWA")

col1, col2, col3 = st.columns(3)

col1.metric("Total", len(df))
col2.metric("Lulus", (df["status"]=="Lulus").sum())
col3.metric("Tidak Lulus", (df["status"]=="Tidak Lulus").sum())

st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

if st.session_state.role == "admin":

    st.subheader("➕ Tambah Data")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("Simpan"):
        supabase.table("database-akademik-siswa").insert({
            "nama": nama,
            "nilai": nilai
        }).execute()
        st.success("Data ditambahkan")
        time.sleep(1)
        st.rerun()

    st.subheader("🗑️ Hapus Data")

    pilih = st.selectbox("Pilih ID", df["id"])

    if st.button("Hapus"):
        supabase.table("database-akademik-siswa").delete().eq("id", pilih).execute()
        st.warning("Data dihapus")
        time.sleep(1)
        st.rerun()

st.subheader("📈 Grafik")

fig = px.bar(df, x="nama", y="nilai", color="status")
st.plotly_chart(fig, use_container_width=True)

if st.button("Logout"):
    st.session_state.login = False
    st.rerun()
