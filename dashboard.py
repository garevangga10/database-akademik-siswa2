import streamlit as st
import pandas as pd
from supabase import create_client

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Database Akademik Siswa",
    page_icon="📊",
    layout="wide"
)

# =========================
# STYLE ESTETIK
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.glass {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(0,255,255,0.3);
}

.card {
    padding: 20px;
    border-radius: 20px;
    background: rgba(0,0,0,0.5);
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,255,0.4);
}

.card h3 {
    color: #00f7ff;
}

.card p {
    font-size: 32px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SUPABASE CONNECTION
# =========================
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    CONNECTED = True
except:
    CONNECTED = False
    st.warning("⚠ Supabase tidak terhubung.")

# =========================
# LOAD DATA
# =========================
def load_data():
    if not CONNECTED:
        return pd.DataFrame()
    try:
        res = supabase.table("database-akademik-siswa").select("*").execute()
        return pd.DataFrame(res.data)
    except:
        return pd.DataFrame()

df = load_data()

# =========================
# HITUNG STATUS
# =========================
if not df.empty:
    df["status"] = df["nilai"].apply(
        lambda x: "Lulus" if x >= 75 else "Tidak Lulus"
    )

# =========================
# DASHBOARD
# =========================
st.title("📊 DATABASE AKADEMIK SISWA")

if df.empty:
    st.info("Belum ada data.")
else:
    total = len(df)
    lulus = len(df[df["status"] == "Lulus"])
    tidak = len(df[df["status"] == "Tidak Lulus"])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class='card'>
            <h3>Total</h3>
            <p>{total}</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
            <h3>Lulus</h3>
            <p>{lulus}</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='card'>
            <h3>Tidak Lulus</h3>
            <p>{tidak}</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("📋 Data Siswa")
    st.dataframe(df)

# =========================
# TAMBAH DATA
# =========================
st.subheader("➕ Tambah Data")

nama = st.text_input("Nama")
nilai = st.number_input("Nilai", 0, 100, 0)

if st.button("Simpan"):
    if CONNECTED and nama:
        supabase.table("database-akademik-siswa").insert({
            "nama": nama,
            "nilai": nilai
        }).execute()
        st.success("Data ditambahkan")
        st.rerun()

# =========================
# HAPUS DATA
# =========================
if not df.empty:
    st.subheader("🗑 Hapus Data")
    pilih = st.selectbox("Pilih siswa", df["nama"].tolist())

    if st.button("Hapus"):
        if CONNECTED:
            supabase.table("database-akademik-siswa").delete().eq("nama", pilih).execute()
            st.warning("Data dihapus")
            st.rerun()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("✨ Database Akademik Siswa - Supabase + Streamlit Cloud")
