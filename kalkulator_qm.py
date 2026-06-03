from sympy.logic import simplify_logic
import sympy

# =========================================================
# TAHAP 1: INPUT JUMLAH VARIABEL (MINIMAL 6 VARIABEL)
# =========================================================
print("=" * 65)
print("   PROGRAM KELOMPOK 8 : Kalkulator Quine McCluskey POS method  ")
print("=" * 65 + "\n")

while True:
    try:
        # Meminta input angka dari user
        jumlah_variabel = int(input("Masukkan jumlah variabel (Minimal 6): "))

        # cek apakah angkanya sudah 6 atau lebih
        if jumlah_variabel >= 6:
            print(f"-> Sukses: Jumlah variabel ditetapkan {jumlah_variabel}.\n")
            break  # Keluar dari perulangan karena input sudah benar
        else:
            print("-> Error: Program mewajibkan minimal 6 variabel. Silakan coba lagi.\n")

    except ValueError:
        # Jika user input huruf, bukan angka
        print("-> Error: Harap masukkan angka yang valid!\n")
# =========================================================
# TAHAP 2: INPUT DATA MAXTERM
# =========================================================
while True:
    input_maxterm = input("Masukkan nilai Maxterm (Contoh: 0,1,2): ")
    if input_maxterm.strip() != "":
        try:
            daftar_maxterm = [int(x) for x in input_maxterm.split(",") if x.strip() != ""]
            print(f"-> Sukses: Daftar Maxterm disimpan: {daftar_maxterm}\n")
            break
        except ValueError:
            print("-> Error: Format salah! Pastikan hanya angka dan koma saja.\n")
    else:
        print("-> Error: Maxterm tidak boleh kosong!\n")
# =========================================================
# TAHAP 3: INPUT DATA DON'T CARE
# =========================================================
while True:
    input_dont_care = input("Masukkan nilai Don't Care (Contoh: 3,4 atau isi 0 jika tidak ada): ")
    if input_dont_care.strip() != "":
        try:
            daftar_dont_care = [int(x) for x in input_dont_care.split(",") if x.strip() != ""]
            print(f"-> Sukses: Daftar Don't Care disimpan: {daftar_dont_care}\n")
            break
        except ValueError:
            print("-> Error: Format salah! Pastikan hanya angka dan koma saja.\n")
    else:
        print("-> Error: Harap isi angka atau ketik 0 jika tidak ada Don't Care.\n")
# =========================================================
# TAHAP 4: PROSES KONVERSI DESIMAL KE BINER SERAGAM
# =========================================================
biner_maxterm = []
biner_dont_care = []

for angka in daftar_maxterm:
    format_biner = format(angka, f'0{jumlah_variabel}b')
    biner_maxterm.append(format_biner)

for angka in daftar_dont_care:
    format_biner = format(angka, f'0{jumlah_variabel}b')
    biner_dont_care.append(format_biner)
# =========================================================
# TAHAP 5: MENAMPILKAN HASILNYA DI LAYAR
# =========================================================
print("\n--- DATA AWAL YANG BERHASIL DITAMPUNG ---")
print(f"Daftar Maxterm Asli    : {daftar_maxterm}")
print(f"Biner Maxterm          : {biner_maxterm}")
print(f"Biner Don't Care       : {biner_dont_care}")

print("\n" + "=" * 45)
print(" MENU OPSI:")
print(" [1] Sederhanakan Fungsi (Metode Quine-McCluskey)")
print("=" * 45)

# Konfirmasi tunggal, user cukup menekan enter untuk memproses tindakan
input("-> Tekan [ENTER] untuk mengonfirmasi dan memulai penyederhanaan... ")
print("\nMemproses... Silakan tunggu hasil perhitungan.")
# =========================================================
# TAHAP 6: TABEL TABULASI (PROSES KOMBINASI)
# =========================================================
semua_desimal = sorted(list(set(daftar_maxterm + daftar_dont_care)))
tabel_sekarang = [((x,), format(x, f'0{jumlah_variabel}b')) for x in semua_desimal]

prime_implicants = set()
kolom = 1

while True:
    print(f"\n=== TABEL TABULASI KOLOM {kolom} ===")
    print(f"{'Grup':<7} | {'Nilai Desimal':<18} | {'Format Biner':<12}")
    print("-" * 45)

    grup = {}
    for desimal, biner in tabel_sekarang:
        n_ones = biner.count('1')
        if n_ones not in grup:
            grup[n_ones] = []
        grup[n_ones].append((desimal, biner))

    for g in sorted(grup.keys()):
        for desimal, biner in grup[g]:
            nama_desimal = ",".join(map(str, desimal))
            print(f"Grup {g:<2} | {nama_desimal:<18} | {biner:<12}")

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
# =========================================================
# TAHAP 7: TABEL CAKUPAN PRIME IMPLICANT (PI CHART)
# =========================================================
print("\n=== TABEL CAKUPAN PRIME IMPLICANT (PI CHART) ===")
print("Catatan: Tanda '✓' berarti PI tersebut mencakup Maxterm di kolom tersebut.")
print("Kolom HANYA berisi Maxterm (Don't Care diabaikan).\n")

# Urutkan Maxterm agar kolom tabelnya rapi
target_maxterm_urut = sorted(daftar_maxterm)

# 1. Membuat Header Tabel
# Mengatur jarak spasi agar tabel sejajar
header = f"| {'PI (Biner)':<15} |"
for m in target_maxterm_urut:
    header += f" {m:<3} |"

panjang_tabel = len(header)
print("-" * panjang_tabel)
print(header)
print("-" * panjang_tabel)

# 2. Membuat Baris Isi Tabel (Centang/Silang)
for desimal, biner in list_pi:
    baris = f"| {biner:<15} |"
    for m in target_maxterm_urut:
        # Cek apakah Maxterm (m) ada di dalam daftar cakupan PI ini (desimal)
        if m in desimal:
            baris += f" {'✓':<3} |" # Gunakan '✓' atau 'X' sebagai tanda
        else:
            baris += f" {' ':<3} |"
    print(baris)

print("-" * panjang_tabel)
# =========================================================
# TAHAP 8: PENCARIAN EPI & ALTERNATIF
# =========================================================
target_maxterm = set(daftar_maxterm)
list_pi = sorted(list(prime_implicants)) # Diurutkan biar tabel lebih rapi

epi_terpilih = []
sisa_maxterm = target_maxterm.copy()

# 1. Cari Essential Prime Implicants (EPI)
for m in target_maxterm:
    pi_pencakup = [pi for pi in list_pi if m in pi[0]]
    if len(pi_pencakup) == 1:
        if pi_pencakup[0] not in epi_terpilih:
            epi_terpilih.append(pi_pencakup[0])
            sisa_maxterm -= set(pi_pencakup[0][0])

# 2. Cari PI Alternatif (Kombinasi sisa)
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

# Mengumpulkan semua PI yang terpilih sebagai alternatif (buat ditandai di tabel)
pi_alternatif_semua = set()
for kombi in kombinasi_tambahan_valid:
    for pi in kombi:
        pi_alternatif_semua.add(pi)

# =========================================================
# TAHAP 9: TABEL CAKUPAN DENGAN MARKER (* DAN **)
# =========================================================
print("Keterangan Status:")
print("[ * ]  : EPI (Essential Prime Implicant)")
print("[ ** ] : Alternatif Terpilih\n")

target_maxterm_urut = sorted(daftar_maxterm)

# Mengatur lebar kolom Nilai Desimal
max_len_desimal = max([len(",".join(map(str, pi[0]))) for pi in list_pi]) if list_pi else 15
lebar_desimal = max(15, max_len_desimal)

# 1. Membuat Header Tabel
header = f"| {'Status':<6} | {'Nilai Desimal':<{lebar_desimal}} | {'Format Biner':<15} |"
for m in target_maxterm_urut:
    header += f" {m:<3} |"

panjang_tabel = len(header)
print("-" * panjang_tabel)
print(header)
print("-" * panjang_tabel)

# 2. Mengisi Baris Tabel dengan Marker dan Centang
for desimal, biner in list_pi:
    # Cek status PI (EPI, Alternatif, atau tidak terpakai)
    if (desimal, biner) in epi_terpilih:
        status = "*"
    elif (desimal, biner) in pi_alternatif_semua:
        status = "**"
    else:
        status = ""
        
    str_desimal = ",".join(map(str, desimal))
    baris = f"| {status:<6} | {str_desimal:<{lebar_desimal}} | {biner:<15} |"
    
    # Ceklis Maxterm
    for m in target_maxterm_urut:
        if m in desimal:
            baris += f" {'✓':<3} |"
        else:
            baris += f" {' ':<3} |"
            
    print(baris)

print("-" * panjang_tabel)

# =========================================================
# TAHAP 10: HASIL AKHIR PENYEDERHANAAN POS
# =========================================================
semua_solusi_pi = []
for kombi in kombinasi_tambahan_valid:
    solusi_lengkap = epi_terpilih + kombi
    semua_solusi_pi.append(solusi_lengkap)

print("\n=== HASIL PENYEDERHANAAN FUNGSI POS ===")
print(f"Fokus Utama Maxterm : {daftar_maxterm}")
print(f"Ditemukan {len(semua_solusi_pi)} alternatif persamaan yang paling sederhana:\n")

for index, solusi in enumerate(semua_solusi_pi):
    grup_huruf_pos = []
    for desimal, biner in solusi:
        komponen_sum = []
        for i in range(jumlah_variabel):
            nama_variabel = chr(65 + i) # A, B, C, dst...
            if biner[i] == '0':
                komponen_sum.append(nama_variabel)
            elif biner[i] == '1':
                komponen_sum.append(f"{nama_variabel}'")
                
        teks_sum = f"({ ' + '.join(komponen_sum) })"
        grup_huruf_pos.append(teks_sum)
        
    HASIL_AKHIR_POS = "".join(grup_huruf_pos)
    print(f"Alternatif {index + 1} : Y = {HASIL_AKHIR_POS}")
