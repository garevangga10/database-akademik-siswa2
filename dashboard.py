import streamlit as st
import pandas as pd
from supabase import create_client

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Database Akademik Siswa",
    page_icon="📚",
    layout="wide"
)

# =====================
# SUPABASE
# =====================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_ANON_KEY"]
)

# =====================
# STYLE (NEON + ANIMASI)
# =====================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f172a,#020617);
}
@keyframes glow {
  0% {text-shadow:0 0 5px #38bdf8;}
  50% {text-shadow:0 0 20px #38bdf8;}
  100% {text-shadow:0 0 5px #38bdf8;}
}
.title {
  font-size:42px;
  font-weight:900;
  color:#38bdf8;
  animation:glow 2s infinite;
}
.card {
  background:rgba(15,23,42,.85);
  border-radius:18px;
  padding:20px;
  box-shadow:0 0 20px rgba(56,189,248,.3);
  text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =====================
# LOGIN
# =====================
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

# =====================
# LOAD DATA
# =====================
def load_data():
    res = supabase.table("siswa").select("*").execute()
    return pd.DataFrame(res.data)

df = load_data()

if not df.empty:
    df["status"] = df["nilai"].apply(lambda x: "Lulus" if x >= 75 else "Tidak Lulus")

# =====================
# HEADER
# =====================
st.markdown("<div class='title'>📚 DATABASE AKADEMIK SISWA</div>", unsafe_allow_html=True)
st.divider()

# =====================
# METRIC
# =====================
c1,c2,c3 = st.columns(3)

with c1:
    st.markdown(f"<div class='card'><h3>Total</h3><h1>{len(df)}</h1></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><h3>Lulus</h3><h1>{(df['status']=='Lulus').sum()}</h1></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><h3>Tidak Lulus</h3><h1>{(df['status']=='Tidak Lulus').sum()}</h1></div>", unsafe_allow_html=True)

# =====================
# TABLE
# =====================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# =====================
# ADD DATA
# =====================
st.subheader("➕ Tambah Data")

nama = st.text_input("Nama Siswa")
nilai = st.number_input("Nilai", 0, 100)

if st.button("Simpan"):
    supabase.table("siswa").insert({
        "nama": nama,
        "nilai": nilai
    }).execute()
    st.success("Data ditambahkan")
    st.rerun()

# =====================
# EDIT & DELETE
# =====================
st.subheader("✏️ Edit / Hapus")

if not df.empty:
    pilih = st.selectbox("Pilih siswa", df["nama"])
    row = df[df["nama"] == pilih].iloc[0]

    nilai_edit = st.number_input("Edit nilai", 0, 100, int(row["nilai"]))

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Update"):
            supabase.table("siswa").update({
                "nilai": nilai_edit
            }).eq("id", int(row["id"])).execute()
            st.success("Data diupdate")
            st.rerun()

    with col2:
        if st.button("Hapus"):
            supabase.table("siswa").delete().eq("id", int(row["id"])).execute()
            st.warning("Data dihapus")
            st.rerun()

st.caption("✨ Supabase • Streamlit • Database Permanen")
