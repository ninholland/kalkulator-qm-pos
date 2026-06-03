import streamlit as st
from itertools import combinations

# --- TAMPILAN HEADER WEBSITE ---
st.set_page_config(page_title="Kalkulator Quine-McCluskey POS", layout="wide")
st.title("💻 PROGRAM KELOMPOK 8")
st.subheader("Kalkulator Penyederhanaan Boolean - Quine McCluskey Method (POS)")
st.markdown("---")

# --- KOTAK INPUT USER DI WEBSITE ---
col1, col2, col3 = st.columns(3)

with col1:
    jumlah_variabel = st.number_input("Jumlah Variabel (Minimal 6):", min_value=6, value=6, step=1)

with col2:
    input_maxterm = st.text_input("Masukkan nilai Maxterm (Contoh: 0,1,2):", value="0,1,2")

with col3:
    input_dont_care = st.text_input("Masukkan nilai Don't Care (Isi 0 jika tidak ada):", value="0")

# --- TOMBOL KONFIRMASI UTK PROSES ---
if st.button("🚀 Sederhanakan Fungsi", type="primary"):
    
    # 1. Proses
    daftar_maxterm = [int(x) for x in input_maxterm.split(",") if x.strip() != ""]
    daftar_dont_care = [int(x) for x in input_dont_care.split(",") if x.strip() != ""]
    
    biner_maxterm = [format(angka, f'0{jumlah_variabel}b') for angka in daftar_maxterm]
    biner_dont_care = [format(angka, f'0{jumlah_variabel}b') for angka in daftar_dont_care]
    
    # Tampilkan Data Awal
    st.info(f"**Daftar Maxterm Asli:** {daftar_maxterm} | **Don't Care:** {daftar_dont_care}")
    
    # 2. Proses Tabulasi
    semua_desimal = sorted(list(set(daftar_maxterm + daftar_dont_care)))
    tabel_sekarang = [((x,), format(x, f'0{jumlah_variabel}b')) for x in semua_desimal]
    prime_implicants = set()
    kolom = 1
    
    st.write("### 📊 Proses Tabel Tabulasi")
    
    # 3. Hitung EPI & Alternatif (Tahap 7-8 kodemu)
    target_maxterm = set(daftar_maxterm)
    list_pi = sorted(list(prime_implicants))
    
    # ... (Gunakan logika pencarian EPI) ...
    
    # 4. Tampilkan Tabel Centang (PI Chart) di Web
    st.write("### 🏁 Tabel Cakupan Prime Implicant (PI Chart)")
    
    # Kumpulkan baris tabel ke dalam string teks
    output_tabel = ""
    # ... (loop header dan baris centang seperti kodemu) ...
    # baris = f"| {status:<6} | {str_desimal:<15} | {biner:<15} |"
    
    st.code(output_tabel)
    
    # 5. Hasil Akhir POS
    st.success("### 📜 Hasil Akhir Penyederhanaan Fungsi POS")
    # st.write(f"Alternatif 1: Y = (A + B)(C' + D)")
