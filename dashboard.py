import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
import time

st.set_page_config(page_title="BEYOND GOD MODE", layout="wide")

# ===============================
# CONNECT SUPABASE
# ===============================
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

# ===============================
# AUTH SYSTEM (REAL LOGIN)
# ===============================
if "session" not in st.session_state:
    st.session_state.session = None

if not st.session_state.session:

    st.title("🚀 BEYOND GOD LOGIN")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res.user:
            st.session_state.session = res.session
            st.rerun()
        else:
            st.error("Login gagal")

    st.stop()

# ===============================
# REALTIME DATA LOAD
# ===============================
@st.cache_data(ttl=5)
def load_data():
    res = supabase.table("database-akademik-siswa").select("*").execute()
    return pd.DataFrame(res.data)

df = load_data()

if df.empty:
    st.warning("Database kosong")
    st.stop()

df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# ===============================
# DASHBOARD UI
# ===============================
st.title("⚡ BEYOND GOD DASHBOARD")

col1, col2, col3 = st.columns(3)

col1.metric("Total", len(df))
col2.metric("Lulus", (df["status"]=="Lulus").sum())
col3.metric("Tidak Lulus", (df["status"]=="Tidak Lulus").sum())

st.divider()

st.subheader("📊 Animated Chart")

fig = px.bar(
    df,
    x="nama",
    y="nilai",
    color="status",
    template="plotly_dark",
    animation_frame=None
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# ===============================
# LOGOUT
# ===============================
if st.button("Logout"):
    supabase.auth.sign_out()
    st.session_state.session = None
    st.rerun()
