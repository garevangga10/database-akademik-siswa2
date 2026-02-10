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
# STYLE ESTETIK
# =========================
st.markdown("""
<style>
.card {
    background: rgba(15,23,42,0.8);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 0 18px rgba(56,189,248,.35);
}
.card h3 { color:#60a5fa; }
.card p {
    font-size: 30px;
    font-weight: bold;
    color: white;
}
.line {
    height: 6px;
    border-radius: 10px;
    background: linear-gradient(90deg,#22c55e,#3b82f6,#a855f7);
    margin: 15px 0 25px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD GOOGLE SHEETS (NATIVE)
# =========================
conn = st.connection("gsheets", type="google_sheets")

df = conn.read(worksheet="Sheet1", ttl=0)

if df.empty:
    df = pd.DataFrame(columns=["Nama", "Nilai"])

df["Nilai"] = pd.to_numeric(df["Nilai"], errors="coerce").fillna(0)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📚 MENU")
menu = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📋 Data Siswa", "✏️ CRUD", "📊 Grafik"]
)

ambang = st.sidebar.slider("🎯 Ambang Kelulusan", 0, 100, 75)
df["Status"] = df["Nilai"].apply(lambda x: "Lulus" if x >= ambang else "Tidak Lulus")

# =========================
# METRICS
# =========================
total = len(df)
lulus = (df["Status"]=="Lulus").sum()
tidak = (df["Status"]=="Tidak Lulus").sum()
rata = df["Nilai"].mean() if total>0 else 0

# =========================
# DASHBOARD
# =========================
if menu == "🏠 Dashboard":
    st.title("📚 Database Akademik Siswa MAS Al-Hamidiyah")
    st.markdown("<div class='line'></div>", unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><h3>Total</h3><p>{total}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><h3>Lulus</h3><p>{lulus}</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><h3>Tidak Lulus</h3><p>{tidak}</p></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><h3>Rata-rata</h3><p>{rata:.1f}</p></div>", unsafe_allow_html=True)

# =========================
# DATA
# =========================
elif menu == "📋 Data Siswa":
    st.subheader("📋 Data Siswa")
    st.dataframe(df, use_container_width=True)

# =========================
# CRUD
# =========================
elif menu == "✏️ CRUD":
    st.subheader("✏️ Kelola Data")

    nama = st.text_input("Nama")
    nilai = st.number_input("Nilai", 0, 100, 0)

    if st.button("➕ Tambah"):
        df.loc[len(df)] = [nama, nilai]
        conn.update(worksheet="Sheet1", data=df)
        st.success("Data ditambahkan")
        st.rerun()

    st.divider()

    if total > 0:
        pilih = st.selectbox("Pilih Siswa", df["Nama"].tolist())
        nilai_edit = st.number_input(
            "Edit Nilai",
            0, 100,
            int(df[df["Nama"]==pilih]["Nilai"].iloc[0])
        )

        col1,col2 = st.columns(2)
        with col1:
            if st.button("💾 Update"):
                df.loc[df["Nama"]==pilih,"Nilai"] = nilai_edit
                conn.update(worksheet="Sheet1", data=df)
                st.success("Diupdate")
                st.rerun()
        with col2:
            if st.button("🗑️ Hapus"):
                df = df[df["Nama"]!=pilih]
                conn.update(worksheet="Sheet1", data=df)
                st.warning("Dihapus")
                st.rerun()

# =========================
# GRAFIK
# =========================
elif menu == "📊 Grafik":
    g1,g2 = st.columns(2)
    with g1:
        fig,ax = plt.subplots()
        ax.bar(df["Nama"],df["Nilai"])
        ax.axhline(ambang,color="red",linestyle="--")
        st.pyplot(fig)
    with g2:
        fig2,ax2 = plt.subplots()
        ax2.pie(
            [lulus,tidak],
            labels=["Lulus","Tidak Lulus"],
            autopct="%1.1f%%"
        )
        st.pyplot(fig2)

st.caption("✨ Streamlit Native Google Sheets | MAS Al-Hamidiyah")
