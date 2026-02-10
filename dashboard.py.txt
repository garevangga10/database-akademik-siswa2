import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Akademik Siswa",
    page_icon="📊",
    layout="wide"
)

# =========================
# CSS SEDERHANA (WARNA & CARD)
# =========================
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #1f2937;
    text-align: center;
}
.card h2 {
    color: #38bdf8;
}
.card p {
    font-size: 24px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# JUDUL
# =========================
st.title("📊 Dashboard Akademik Siswa")
st.caption("Visualisasi data nilai dan kelulusan siswa berbasis web")

# =========================
# DATA
# =========================
data = {
    "Nama": ["Tegar", "Andi", "Siti", "Budi", "Rina", "Dewi"],
    "Nilai": [90, 70, 85, 60, 95, 73]
}

df = pd.DataFrame(data)
df["Status"] = df["Nilai"].apply(
    lambda x: "Lulus" if x >= 75 else "Tidak Lulus"
)

# =========================
# METRIK RINGKAS (CARD)
# =========================
total = len(df)
lulus = (df["Status"] == "Lulus").sum()
tidak = (df["Status"] == "Tidak Lulus").sum()
rata = df["Nilai"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='card'><h2>Total</h2><p>{total}</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><h2>Lulus</h2><p>{lulus}</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><h2>Tidak Lulus</h2><p>{tidak}</p></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='card'><h2>Rata-rata</h2><p>{rata:.1f}</p></div>", unsafe_allow_html=True)

st.divider()

# =========================
# FILTER
# =========================
status_filter = st.selectbox(
    "🔍 Filter Status",
    ["Semua", "Lulus", "Tidak Lulus"]
)

if status_filter != "Semua":
    df_tampil = df[df["Status"] == status_filter]
else:
    df_tampil = df

# =========================
# TABEL
# =========================
st.subheader("📋 Tabel Data Siswa")
st.dataframe(df_tampil, use_container_width=True)

# =========================
# GRAFIK
# =========================
g1, g2 = st.columns(2)

with g1:
    st.subheader("📈 Grafik Nilai Siswa")
    fig1, ax1 = plt.subplots()
    ax1.bar(df["Nama"], df["Nilai"])
    ax1.set_ylabel("Nilai")
    ax1.set_xlabel("Nama")
    st.pyplot(fig1)

with g2:
    st.subheader("🥧 Persentase Kelulusan")
    fig2, ax2 = plt.subplots()
    ax2.pie(
        [lulus, tidak],
        labels=["Lulus", "Tidak Lulus"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.axis("equal")
    st.pyplot(fig2)

# =========================
# CATATAN
# =========================
st.info("📌 Status kelulusan ditentukan berdasarkan nilai ≥ 75")
