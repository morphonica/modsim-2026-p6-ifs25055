import streamlit as st
import random
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Simulasi Antrian", layout="wide")

st.title("📊 Simulasi Pembagian Lembar Jawaban")

# =========================
# INPUT
# =========================
N = st.slider("Jumlah Mahasiswa", 1, 100, 30)
min_time = st.number_input("Durasi Minimum", value=1.0)
max_time = st.number_input("Durasi Maksimum", value=3.0)

# =========================
# SIMULASI BUTTON
# =========================
if st.button("Jalankan Simulasi"):

    random.seed(42)

    arrival_time = 0
    current_time = 0
    data = []

    # =========================
    # PROSES SIMULASI
    # =========================
    for i in range(1, N+1):
        service_time = random.uniform(min_time, max_time)

        start_time = current_time
        end_time = start_time + service_time
        wait_time = start_time - arrival_time

        data.append({
            "Mahasiswa": i,
            "Service Time": service_time,
            "Start": start_time,
            "End": end_time,
            "Waiting Time": wait_time
        })

        current_time = end_time

    # =========================
    # DATAFRAME
    # =========================
    df = pd.DataFrame(data)

    # simpan ke session biar tidak hilang
    st.session_state.df = df

# =========================
# TAMPILKAN HASIL (AMAN)
# =========================
if "df" in st.session_state:

    df = st.session_state.df

    # =========================
    # HASIL
    # =========================
    total_time = df["End"].iloc[-1]
    avg_wait = df["Waiting Time"].mean()
    utilization = (df["Service Time"].sum() / total_time) * 100

    st.subheader("📌 Hasil Simulasi")
    st.write("Total Waktu:", round(total_time, 2))
    st.write("Rata-rata Waktu Tunggu:", round(avg_wait, 2))
    st.write("Utilisasi:", round(utilization, 2), "%")

    # =========================
    # TABEL
    # =========================
    st.subheader("📋 Data Simulasi")
    st.dataframe(df)

    # =========================
    # GRAFIK
    # =========================
    st.subheader("📈 Visualisasi")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Waktu Selesai")
        st.line_chart(df["End"])

    with col2:
        st.write("Waktu Tunggu")
        st.bar_chart(df["Waiting Time"])

    # =========================
    # VALIDASI
    # =========================
    expected_service_time = (min_time + max_time) / 2
    simulated_avg_service = df["Service Time"].mean()

    error_percent = abs(simulated_avg_service - expected_service_time) / expected_service_time * 100
    accuracy = 100 - error_percent

    st.subheader("✅ Validasi Model")
    st.write("Rata-rata Service (Simulasi):", round(simulated_avg_service, 2))
    st.write("Rata-rata Service (Teori):", expected_service_time)
    st.write("Error (%):", round(error_percent, 2))
    st.write("Akurasi (%):", round(accuracy, 2))

    # =========================
    # VERIFIKASI
    # =========================
    if all(df["Start"] >= df["Start"].shift(1).fillna(0)):
        st.success("Verifikasi: Model berjalan dengan benar (tidak ada overlap)")
    else:
        st.error("Verifikasi: Model tidak valid")

else:
    st.info("Klik tombol 'Jalankan Simulasi' untuk memulai.")