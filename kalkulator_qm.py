import streamlit as st
from itertools import combinations

# =========================================================
# HEADER & SETTING INTERFACE WEBSITE
# =========================================================
st.set_page_config(page_title="Kalkulator QM Kelompok 8", layout="wide")

st.markdown("<h2 style='text-align: center;'>💻 PROGRAM KELOMPOK 8</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4CAF50;'>KALKULATOR Quine McCluskey method POS</h3>", unsafe_allow_html=True)
st.markdown("---")

# Baris Atas: Input Jumlah Variabel
jumlah_variabel = st.number_input(
    "Masukkan jumlah variabel (Minimal 6):", 
    min_value=6, 
    value=6, 
    step=1
)

# Hitung rentang maksimum
rentang = (2 ** jumlah_variabel) - 1
st.info(f"💡 Rentang maksimal desimal yang valid: **0 - {rentang}**")

# Baris Bawah: Dua Kolom Berdampingan untuk Maxterm dan Don't Care
col_input1, col_input2 = st.columns(2)

with col_input1:
    input_maxterm = st.text_input("Nilai Maxterm (Pisahkan dengan koma):", placeholder="Contoh: 0,1,2")

with col_input2:
    input_dont_care = st.text_input("Nilai Don't Care (Kosongkan jika tidak ada):", placeholder="Contoh: 3,4")

# Tombol Eksekusi di Bawah Kolom Input
st.markdown(" ")
tombol_proses = st.button("Sederhanakan Fungsi", type="primary", use_container_width=True)
st.markdown("---")

# =========================================================
# PROSES UTAMA LOGIKA QUINE-MCCLUSKEY
# =========================================================
if tombol_proses:
    # --- Validasi Maxterm ---
    if not input_maxterm.strip():
        st.error("❌ Error: Maxterm tidak boleh kosong!")
        st.stop()
        
    try:
        daftar_maxterm = [int(x) for x in input_maxterm.split(",") if x.strip() != ""]
        hasil_maks = max(daftar_maxterm)
        if hasil_maks > rentang:
            st.error(f"❌ Error: Ada maxterm yang melebihi rentang (Maksimal {rentang})!")
            st.stop()
    except ValueError:
        st.error("❌ Error: Format Maxterm salah! Pastikan hanya angka dan koma.")
        st.stop()

    # --- Validasi Don't Care ---
    daftar_dont_care = []
    if input_dont_care.strip():
        try:
            daftar_dont_care = [int(x) for x in input_dont_care.split(",") if x.strip() != ""]
            if daftar_dont_care:
                hasil_maks_dc = max(daftar_dont_care)
                if hasil_maks_dc > rentang:
                    st.error(f"❌ Error: Ada Don't Care yang melebihi rentang (Maksimal {rentang})!")
                    st.stop()
        except ValueError:
            st.error("❌ Error: Format Don't Care salah! Pastikan hanya angka dan koma.")
            st.stop()
            
        # PROSES KONVERSI BINER
        biner_maxterm = [format(angka, f'0{jumlah_variabel}b') for angka in daftar_maxterm]
        biner_dont_care = [format(angka, f'0{jumlah_variabel}b') for angka in daftar_dont_care]
        
        # TAHAP 6: TABEL TABULASI
        semua_desimal = sorted(list(set(daftar_maxterm + daftar_dont_care)))
        tabel_sekarang = [((x,), format(x, f'0{jumlah_variabel}b')) for x in semua_desimal]

        prime_implicants = set()
        kolom = 1
        
        st.markdown("---")
        st.subheader("📊 PROSES TABEL TABULASI")

        while True:
            teks_tabulasi = f"=== TABEL TABULASI KOLOM {kolom} ===\n"
            teks_tabulasi += f"{'Grup':<7} | {'Nilai Desimal':<18} | {'Format Biner':<12}\n"
            teks_tabulasi += "-" * 45 + "\n"

            grup = {}
            for desimal, biner in tabel_sekarang:
                n_ones = biner.count('1')
                if n_ones not in grup:
                    grup[n_ones] = []
                grup[n_ones].append((desimal, biner))

            for g in sorted(grup.keys()):
                for desimal, biner in grup[g]:
                    nama_desimal = ",".join(map(str, desimal))
                    teks_tabulasi += f"Grup {g:<2} | {nama_desimal:<18} | {biner:<12}\n"

            st.code(teks_tabulasi) # Nampilin tabel biner di web biar fontnya sejajar

            tabel_berikutnya = []
            di_eliminasi = set()

            for i in range(len(tabel_sekarang)):
                for j in range(i + 1, len(tabel_sekarang)):
                    d1, b1 = tabel_sekarang[i]
                    d2, b2 = tabel_sekarang[j]

                    bisa_kombinasi = True
                    diff = 0
                    pos = -1

                    for k in range(jumlah_variabel):
                        if (b1[k] == '-' and b2[k] != '-') or (b1[k] != '-' and b2[k] == '-'):
                            bisa_kombinasi = False
                            break
                        if b1[k] != b2[k]:
                            diff += 1
                            pos = k

                    if bisa_kombinasi and diff == 1:
                        di_eliminasi.add(b1)
                        di_eliminasi.add(b2)
                        b_baru = list(b1)
                        b_baru[pos] = '-'
                        b_baru = "".join(b_baru)
                        d_baru = tuple(sorted(list(set(d1 + d2))))

                        if (d_baru, b_baru) not in tabel_berikutnya:
                            tabel_berikutnya.append((d_baru, b_baru))

            for d, b in tabel_sekarang:
                if b not in di_eliminasi:
                    prime_implicants.add((d, b))

            if not tabel_berikutnya:
                break

            tabel_sekarang = tabel_berikutnya
            kolom += 1

        # TAHAP 7 & 8: HITUNG EPI & ALTERNATIF DI BALIK LAYAR + MATRIKS CHART
        target_maxterm = set(daftar_maxterm)
        list_pi = sorted(list(prime_implicants))

        epi_terpilih = []
        sisa_maxterm = target_maxterm.copy()

        for m in target_maxterm:
            pi_pencakup = [pi for pi in list_pi if m in pi[0]]
            if len(pi_pencakup) == 1:
                if pi_pencakup[0] not in epi_terpilih:
                    epi_terpilih.append(pi_pencakup[0])
                    sisa_maxterm -= set(pi_pencakup[0][0])

        sisa_pi = [pi for pi in list_pi if pi not in epi_terpilih]
        kombinasi_tambahan_valid = []

        if not sisa_maxterm:
            kombinasi_tambahan_valid.append([])
        else:
            for r in range(1, len(sisa_pi) + 1):
                for kombi in combinations(sisa_pi, r):
                    cakupan = set()
                    for pi in kombi:
                        cakupan.update(pi[0])
                    if sisa_maxterm.issubset(cakupan):
                        kombinasi_tambahan_valid.append(list(kombi))
                if kombinasi_tambahan_valid:
                    break

        pi_alternatif_semua = set()
        for kombi in kombinasi_tambahan_valid:
            for pi in kombi:
                pi_alternatif_semua.add(pi)

        # TAMPILKAN TABEL CAKUPAN DI WEB
        st.markdown("---")
        st.subheader("TABEL CAKUPAN PRIME IMPLICANT (PI CHART)")
        st.write("**Keterangan Status:** `[*]` = EPI (Wajib) | `[**]` = Alternatif Terpilih")
        
        target_maxterm_urut = sorted(daftar_maxterm)
        max_len_desimal = max([len(",".join(map(str, pi[0]))) for pi in list_pi]) if list_pi else 15
        lebar_desimal = max(15, max_len_desimal)

        header = f"| {'Status':<6} | {'Nilai Desimal':<{lebar_desimal}} | {'Format Biner':<15} |"
        for m in target_maxterm_urut:
            header += f" {m:<3} |"

        teks_tabel = "-" * len(header) + "\n" + header + "\n" + "-" * len(header) + "\n"

        for desimal, biner in list_pi:
            status = "*" if (desimal, biner) in epi_terpilih else ("**" if (desimal, biner) in pi_alternatif_semua else "")
            str_desimal = ",".join(map(str, desimal))
            baris = f"| {status:<6} | {str_desimal:<{lebar_desimal}} | {biner:<15} |"
            
            for m in target_maxterm_urut:
                baris += f" {'✓':<3} |" if m in desimal else f" {' ':<3} |"
            teks_tabel += baris + "\n"

        teks_tabel += "-" * len(header)
        st.code(teks_tabel)

        # TAHAP 8: HASIL AKHIR POS
        st.markdown("---")
        st.subheader("HASIL PENYEDERHANAAN FUNGSI POS")
        
        semua_solusi_pi = [epi_terpilih + kombi for kombi in kombinasi_tambahan_valid]
        st.write(f"Ditemukan **{len(semua_solusi_pi)}** alternatif persamaan paling sederhana:")

        for index, solusi in enumerate(semua_solusi_pi):
            grup_huruf_pos = []
            for desimal, biner in solusi:
                komponen_sum = []
                for i in range(jumlah_variabel):
                    nama_variabel = chr(65 + i)
                    if biner[i] == '0':
                        komponen_sum.append(nama_variabel)
                    elif biner[i] == '1':
                        komponen_sum.append(f"{nama_variabel}'")
                grup_huruf_pos.append(f"({ ' + '.join(komponen_sum) })")
                
            st.success(f"**Alternatif {index + 1} :** Y = {''.join(grup_huruf_pos)}")
            
