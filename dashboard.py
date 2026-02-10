import streamlit as st
import pandas as pd
from supabase import create_client

# =====================
# CONFIG
# =====================
st.set_page_config(
    page_title="Dashboard Akademik Siswa",
    layout="wide"
)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================
# LOAD DATA
# =====================
def load_data():
    res = supabase.table("siswa").select("*").execute()
    return pd.DataFrame(res.data)

# =====================
# UI
# =====================
st.title("📊 Dashboard Akademik Siswa")

try:
    df = load_data()

    if df.empty:
        st.warning("⚠️ Data masih kosong")
    else:
        st.success("✅ Data berhasil dimuat dari Supabase")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("❌ Gagal konek Supabase")
    st.code(str(e))
