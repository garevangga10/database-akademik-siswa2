import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Database Akademik Siswa MAS Al-Hamidiyah",
    page_icon="📚",
    layout="wide"
)

# =========================
# STYLE SUPER ESTETIK
# =========================
st.markdown("""
<style>
.stApp {
    background:
    linear-gradient(135deg, rgba(34,197,94,.15), rgba(59,130,246,.15)),
    repeating-linear-gradient(
        45deg,
        rgba(168,85,247,.15),
        rgba(168,85,247,.15) 10px,
        rgba(59,130,246,.15) 10px,
        rgba(59,130,246,.15) 20px
    );
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#020617);
    border-right: 2px solid #38bdf8;
}

/* Running text */
@keyframes marquee {
    from { transform: translateX(100%); }
    to { transform: translateX(-100%); }
}
.running-text {
    white-space: nowrap;
    font-size: 34px;
    font-weight: 900;
    color: #38bdf8;
    animation: marquee 15s linear infinite;
}

/* Blink */
@keyframes blink {
    0%,100% {opacity:1;}
    50% {opacity:.4;}
}
.blink {
    animation: blink 1.5s infinite;
}

/* Cards */
.card {
    background: rgba(15,23,42,.75);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 30px rgba(56,189,248,.45);
}
.card h3 {color:#60a5fa;}
.card p {
    font-size:32px;
    font-weight:bold;
}

/* Divider */
.line {
    height:6px;
    border-radius:10px;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#a855f7);
    margin:20px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOGIN DEMO
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.role = None

if not st.session_state.login:
    st.title("🔐 LOGIN SISTEM")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state.login = True
            st.session_state.role = "admin"
            st.rerun()
        elif u == "user" and p == "user123":
            st.session_state.login = True
            st.session_state.role = "user"
            st.rerun()
        else:
            st.error("Username atau password salah")

    st.stop()

# =========================
# DATABASE SESSION
# =========================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Nama": ["Tegar", "Andi", "Siti", "Budi"],
        "Nilai": [90, 78, 85, 60]
    })

df = st.session_state.df

# =========================
# HEADER
# =========================
st.markdown(
    "<div class='running-text'>📚 DATABASE AKADEMIK SISWA MAS AL-HAMIDIYAH 📚</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='line'></div>", unsafe_allow_html=True)

# =========================
# METRIC
# =========================
ambang = 75
df["Status"] = df["Nilai"].apply(lambda x: "Lulus" if x >= ambang else "Tidak Lulus")

total = len(df)
lulus = (df["Status"]=="Lulus").sum()
tidak = (df["Status"]=="Tidak Lulus").sum()
rata = df["Nilai"].mean()

c1,c2,c3,c4 = st.columns(4)
c1.markdown(f"<div class='card'><h3>Total</h3><p>{total}</p></div>",unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h3>Lulus</h3><p>{lulus}</p></div>",unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h3>Tidak Lulus</h3><p>{tidak}</p></div>",unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h3>Rata-rata</h3><p>{rata:.1f}</p></div>",unsafe_allow_html=True)

st.markdown("<div class='line'></div>", unsafe_allow_html=True)

# =========================
# DATA
# =========================
st.subheader("📋 Data Siswa")
st.dataframe(df, use_container_width=True)

# =========================
# CRUD (ADMIN ONLY)
# =========================
if st.session_state.role == "admin":
    st.subheader("✏️ Kelola Data (Admin)")
    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai",0,100,0)

    if st.button("Tambah Data"):
        df.loc[len(df)] = [nama,nilai]
        st.session_state.df = df
        st.success("Data ditambahkan")
        st.rerun()

# =========================
# GRAFIK
# =========================
g1,g2 = st.columns(2)
with g1:
    fig,ax = plt.subplots()
    ax.bar(df["Nama"],df["Nilai"],color="#38bdf8")
    st.pyplot(fig)
with g2:
    fig2,ax2 = plt.subplots()
    ax2.pie([lulus,tidak],labels=["Lulus","Tidak Lulus"],autopct="%1.1f%%")
    st.pyplot(fig2)

st.markdown("<p class='blink'>⚡ Sistem aktif | Demo Online ⚡</p>",unsafe_allow_html=True)
