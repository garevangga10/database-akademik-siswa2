import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Database Akademik Siswa MAS Al-Hamidiyah",
    page_icon="📚",
    layout="wide"
)

# =========================
# STYLE (GLASS + NEON)
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #000);
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid #1e293b;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #22c55e, #3b82f6, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(56,189,248,0.6);
}

/* Divider */
.line {
    height: 6px;
    border-radius: 12px;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#a855f7);
    margin: 20px 0 30px;
}

/* Cards */
.card {
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 25px rgba(56,189,248,0.35);
    transition: transform .3s;
}
.card:hover {
    transform: translateY(-6px) scale(1.02);
}
.card h3 {
    color: #60a5fa;
    font-size: 18px;
}
.card p {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg,#22c55e,#3b82f6);
    border-radius: 12px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE (SESSION)
# =========================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Nama": ["Tegar", "Andi", "Siti", "Budi"],
        "Nilai": [90, 78, 85, 60]
    })

df = st.session_state.df
df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📚 MENU")
menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📋 Data Siswa", "✏️ Kelola Data", "📊 Grafik"]
)

ambang = st.sidebar.slider("🎯 Ambang Kelulusan", 0, 100, 75)
df["Status"] = df["Nilai"].apply(lambda x: "Lulus" if x >= ambang else "Tidak Lulus")

# =========================
# METRIC
# =========================
total = len(df)
lulus = (df["Status"] == "Lulus").sum()
tidak = (df["Status"] == "Tidak Lulus").sum()
rata = df["Nilai"].mean()

# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":
    st.markdown(
        "<div class='main-title'>DATABASE AKADEMIK SISWA<br>MAS AL-HAMIDIYAH</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><h3>Total Siswa</h3><p>{total}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><h3>Lulus</h3><p>{lulus}</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><h3>Tidak Lulus</h3><p>{tidak}</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><h3>Rata-rata</h3><p>{rata:.1f}</p></div>", unsafe_allow_html=True)

    st.success("✅ Aplikasi database akademik siap dipresentasikan")

# =========================
# DATA
# =========================
elif menu == "📋 Data Siswa":
    st.subheader("📋 Data Siswa")
    st.dataframe(df, use_container_width=True)

# =========================
# CRUD
# =========================
elif menu == "✏️ Kelola Data":
    st.subheader("✏️ Tambah / Edit / Hapus Data")

    nama = st.text_input("Nama Siswa")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("➕ Tambah Data"):
        if nama.strip() == "":
            st.warning("Nama tidak boleh kosong")
        else:
            df.loc[len(df)] = [nama, nilai]
            st.session_state.df = df
            st.success("Data berhasil ditambahkan")
            st.rerun()

    st.divider()

    if total > 0:
        pilih = st.selectbox("Pilih Siswa", df["Nama"].tolist())
        nilai_edit = st.number_input(
            "Edit Nilai",
            0, 100,
            int(df[df["Nama"] == pilih]["Nilai"].iloc[0])
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Update"):
                df.loc[df["Nama"] == pilih, "Nilai"] = nilai_edit
                st.session_state.df = df
                st.success("Data diperbarui")
                st.rerun()
        with col2:
            if st.button("🗑️ Hapus"):
                df = df[df["Nama"] != pilih]
                st.session_state.df = df
                st.warning("Data dihapus")
                st.rerun()

# =========================
# GRAFIK
# =========================
elif menu == "📊 Grafik":
    g1, g2 = st.columns(2)

    with g1:
        fig, ax = plt.subplots()
        ax.bar(df["Nama"], df["Nilai"], color="#38bdf8")
        ax.axhline(ambang, color="red", linestyle="--")
        ax.set_title("Nilai Siswa")
        st.pyplot(fig)

    with g2:
        fig2, ax2 = plt.subplots()
        ax2.pie(
            [lulus, tidak],
            labels=["Lulus", "Tidak Lulus"],
            colors=["#22c55e", "#ef4444"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)

st.caption("✨ Database Akademik Siswa MAS Al-Hamidiyah | Streamlit")
