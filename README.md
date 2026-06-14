# 🗺️ Analisis Data Kependudukan Jawa Barat (2019–2020)

> Proyek analisis data jumlah penduduk berdasarkan jenis kelamin per desa/kelurahan di Provinsi Jawa Barat, dilengkapi dashboard interaktif berbasis Streamlit.

---

## 📑 Daftar Isi

- [Deskripsi Proyek](#-deskripsi-proyek)
- [Struktur Direktori](#-struktur-direktori)
- [Dataset](#-dataset)
- [Pertanyaan Bisnis](#-pertanyaan-bisnis)
- [Library & Tools](#-library--tools)
- [Instalasi & Setup](#-instalasi--setup)
- [Cara Menjalankan Notebook](#-cara-menjalankan-notebook)
- [Cara Menjalankan Dashboard](#-cara-menjalankan-dashboard)
- [Fitur Dashboard](#-fitur-dashboard)
- [Hasil Analisis](#-hasil-analisis)
- [Deploy ke Streamlit Cloud](#-deploy-ke-streamlit-cloud)
- [Troubleshooting](#-troubleshooting)

---

## 📌 Deskripsi Proyek

Proyek ini merupakan submission akhir kelas **Belajar Analisis Data dengan Python** di Dicoding. Analisis dilakukan terhadap data kependudukan Jawa Barat yang bersumber dari **Open Data Jawa Barat (Disdukcapil)**, mencakup 27 kabupaten/kota, 581 kecamatan, dan 3.810 desa/kelurahan pada periode 2019–2020.

Proses analisis mengikuti alur lengkap:
1. Mendefinisikan pertanyaan bisnis (SMART Question)
2. Data Wrangling (Gathering → Assessing → Cleaning)
3. Exploratory Data Analysis (EDA)
4. Visualization & Explanatory Analysis
5. Conclusion & Recommendation

---

## 📁 Struktur Direktori

```
submission/
│
├── dashboard/
│   ├── dashboard.py       ← Source code aplikasi Streamlit
│   └── main_data.csv      ← Dataset bersih yang digunakan dashboard
│
├── data/
│   └── penduduk_jabar.csv ← Dataset mentah original
│
├── notebook.ipynb         ← Notebook analisis data (sudah dieksekusi)
├── README.md              ← Dokumentasi proyek (file ini)
└── requirements.txt       ← Daftar library Python yang dibutuhkan
```

---

## 🗃️ Dataset

| Atribut | Detail |
|---|---|
| **Nama** | Jumlah Penduduk Berdasarkan Jenis Kelamin per Desa/Kelurahan |
| **Sumber** | [Open Data Jawa Barat](https://opendata.jabarprov.go.id/) — Disdukcapil |
| **Periode** | 2019 dan 2020 |
| **Jumlah Baris** | 23.828 baris |
| **Jumlah Kolom** | 18 kolom |
| **Cakupan Wilayah** | 27 Kabupaten/Kota, 581 Kecamatan, 3.810 Desa/Kelurahan |

### Kolom Dataset Mentah (`data/penduduk_jabar.csv`)

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `id` | int | ID unik setiap baris |
| `kode_provinsi` | int | Kode BPS Provinsi (32 = Jawa Barat) |
| `nama_provinsi` | str | Nama provinsi |
| `bps_kode_kabupaten_kota` | int | Kode BPS kabupaten/kota |
| `bps_nama_kabupaten_kota` | str | Nama kabupaten/kota |
| `bps_kode_kecamatan` | int | Kode BPS kecamatan |
| `bps_nama_kecamatan` | str | Nama kecamatan |
| `bps_kode_desa_kelurahan` | int | Kode BPS desa/kelurahan |
| `bps_nama_desa_kelurahan` | str | Nama desa/kelurahan |
| `kemendagri_kode_kecamatan` | str | Kode Kemendagri kecamatan |
| `kemendagri_nama_kecamatan` | str | Nama kecamatan (Kemendagri) |
| `kemendagri_kode_desa_kelurahan` | str | Kode Kemendagri desa/kelurahan |
| `kemendagri_nama_desa_kelurahan` | str | Nama desa/kelurahan (Kemendagri) |
| `status_pemerintahan` | str | `DESA` atau `KELURAHAN` |
| `jenis_kelamin` | str | `LAKI-LAKI` atau `PEREMPUAN` |
| `jumlah_penduduk` | int | Jumlah penduduk (jiwa) |
| `satuan` | str | Satuan pengukuran (`JIWA`) |
| `tahun` | int | Tahun data (`2019` atau `2020`) |

### Kolom Dataset Bersih (`dashboard/main_data.csv`)

Dataset bersih merupakan subset kolom relevan dengan nama yang disederhanakan:

| Kolom Bersih | Kolom Asal |
|---|---|
| `kabupaten_kota` | `bps_nama_kabupaten_kota` |
| `kecamatan` | `bps_nama_kecamatan` |
| `desa_kelurahan` | `bps_nama_desa_kelurahan` |
| `status` | `status_pemerintahan` |
| `jenis_kelamin` | `jenis_kelamin` |
| `jumlah_penduduk` | `jumlah_penduduk` |
| `tahun` | `tahun` |

---

## ❓ Pertanyaan Bisnis

### Pertanyaan 1
> **Kabupaten/kota mana saja yang mengalami pertumbuhan jumlah penduduk tertinggi dan terendah di Provinsi Jawa Barat dari tahun 2019 ke tahun 2020, dan berapa persentase pertumbuhannya?**

### Pertanyaan 2
> **Bagaimana distribusi rasio jenis kelamin (sex ratio) penduduk di setiap kabupaten/kota Jawa Barat pada tahun 2020, dan kabupaten/kota mana yang memiliki ketidakseimbangan gender terbesar?**

Kedua pertanyaan menggunakan kerangka **SMART** (Specific, Measurable, Action-Oriented, Relevant, Time-bound) — penjelasan lengkap ada di `notebook.ipynb`.

---

## 📦 Library & Tools

### Library Python

| Library | Versi | Fungsi |
|---|---|---|
| `pandas` | 2.2.2 | Manipulasi dan analisis data (DataFrame, groupby, pivot, merge) |
| `numpy` | 1.26.4 | Komputasi numerik, operasi array, penanganan nilai ekstrem |
| `matplotlib` | 3.9.0 | Pembuatan grafik dasar (bar chart, scatter plot, line chart) |
| `seaborn` | 0.13.2 | Visualisasi statistik berbasis matplotlib (heatmap, distribusi) |
| `streamlit` | 1.35.0 | Membangun dan menjalankan dashboard web interaktif |

### Tools Pendukung

| Tool | Fungsi |
|---|---|
| **Jupyter Notebook / JupyterLab** | Lingkungan interaktif untuk menulis dan menjalankan kode analisis |
| **Python 3.9+** | Bahasa pemrograman utama |
| **pip** | Package manager untuk instalasi library |
| **Git** (opsional) | Version control dan deploy ke Streamlit Cloud |

---

## ⚙️ Instalasi & Setup

### Prasyarat

Pastikan Python dan pip sudah terinstal di sistem Anda:

```bash
python --version    # Minimal Python 3.9
pip --version
```

### Langkah 1 — Clone / Ekstrak Proyek

Ekstrak file ZIP submission ke direktori pilihan Anda:

```
submission/
├── dashboard/
├── data/
├── notebook.ipynb
├── README.md
└── requirements.txt
```

### Langkah 2 — Buat Virtual Environment

Sangat disarankan menggunakan virtual environment agar library tidak bentrok dengan instalasi Python lain di sistem Anda.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Setelah aktif, prompt terminal akan menampilkan `(venv)` di awal baris.

### Langkah 3 — Install Library

```bash
pip install -r requirements.txt
```

Proses instalasi akan mengunduh dan memasang semua library yang dibutuhkan sesuai versi yang tertera di `requirements.txt`.

Untuk memverifikasi instalasi berhasil:
```bash
pip list
```

---

## 📓 Cara Menjalankan Notebook

Notebook `notebook.ipynb` berisi seluruh proses analisis data dari awal hingga akhir.

### Opsi A — Menggunakan Jupyter Notebook

```bash
# Install Jupyter jika belum ada
pip install notebook

# Jalankan dari direktori submission/
jupyter notebook
```

Browser akan terbuka secara otomatis. Klik file `notebook.ipynb` untuk membukanya, lalu klik **Kernel → Restart & Run All** untuk menjalankan semua sel.

### Opsi B — Menggunakan JupyterLab

```bash
pip install jupyterlab
jupyter lab
```

### Opsi C — Menggunakan Google Colab

1. Buka [colab.research.google.com](https://colab.research.google.com)
2. Pilih **File → Upload notebook** → unggah `notebook.ipynb`
3. Unggah juga file `data/penduduk_jabar.csv` ke sesi Colab:
   ```python
   from google.colab import files
   files.upload()   # pilih penduduk_jabar.csv
   ```
4. Jalankan semua sel dengan **Runtime → Run all**

> **Catatan:** Notebook sudah dalam kondisi telah dieksekusi (output tersimpan). Anda bisa langsung membaca hasilnya tanpa menjalankan ulang.

---

## 🚀 Cara Menjalankan Dashboard

Dashboard dibuat dengan Streamlit dan harus dijalankan dari dalam folder `dashboard/`.

### Langkah 1 — Masuk ke Folder Dashboard

```bash
cd dashboard
```

### Langkah 2 — Jalankan Streamlit

```bash
streamlit run dashboard.py
```

### Langkah 3 — Buka di Browser

Setelah perintah dijalankan, terminal akan menampilkan:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Buka `http://localhost:8501` di browser Anda. Dashboard akan tampil secara otomatis.

### Menghentikan Dashboard

Tekan `Ctrl + C` di terminal untuk menghentikan server Streamlit.

---

## 🖥️ Fitur Dashboard

### Sidebar — Filter Interaktif
- **Pilih Tahun:** Checkbox multiselect untuk memilih tahun analisis (2019, 2020, atau keduanya)
- **Pilih Kabupaten/Kota:** Multiselect untuk memfokuskan analisis pada wilayah tertentu

### Halaman Utama

**KPI Metrics (Baris Atas)**
| Metrik | Keterangan |
|---|---|
| 👥 Total Penduduk | Total jiwa berdasarkan filter aktif |
| 👨 Total Laki-laki | Total penduduk laki-laki |
| 👩 Total Perempuan | Total penduduk perempuan |
| ⚖️ Sex Ratio | Rasio laki-laki per 100 perempuan |

**Visualisasi Pertanyaan 1 — Pertumbuhan Penduduk**
- Tab *Visualisasi:* Bar chart horizontal persentase pertumbuhan + grouped bar chart perbandingan 2019 vs 2020
- Tab *Tabel Data:* Tabel lengkap dengan kolom penduduk 2019, 2020, pertambahan absolut, dan persentase pertumbuhan

**Visualisasi Pertanyaan 2 — Sex Ratio**
- Tab *Visualisasi:* Bar chart sex ratio per kabupaten/kota + stacked bar komposisi gender
- Tab *Tabel Data:* Tabel sex ratio, jumlah laki-laki, perempuan, dan total per kabupaten/kota

**Analisis Lanjutan — Clustering**
- Scatter plot interaktif: Pertumbuhan vs Sex Ratio (ukuran titik = besar populasi)
- Heatmap crosstab: distribusi kabupaten/kota berdasarkan kategori pertumbuhan × kategori sex ratio
- Tabel pengelompokan: hasil binning setiap kabupaten/kota ke dalam kategori

**Kesimpulan & Rekomendasi**
- Ringkasan jawaban dari kedua pertanyaan bisnis
- 4 rekomendasi action item berbasis hasil analisis

---

## 📊 Hasil Analisis

### Kesimpulan 1 — Pertumbuhan Penduduk
Terdapat ketimpangan pertumbuhan yang signifikan antar kabupaten/kota. Wilayah penyangga kawasan industri (seperti Karawang, Bekasi, Purwakarta) mencatat pertumbuhan tertinggi karena daya tarik lapangan kerja. Kota-kota besar seperti Bandung justru mengalami suburbanisasi — penduduk berpindah ke kabupaten sekitarnya.

### Kesimpulan 2 — Sex Ratio
Sex ratio Jawa Barat secara keseluruhan mendekati seimbang (~103). Kabupaten kawasan industri cenderung memiliki sex ratio lebih tinggi karena dominasi migrasi tenaga kerja laki-laki. Tidak ada kabupaten/kota dengan ketidakseimbangan gender yang ekstrem.

### Rekomendasi Action Item
1. Prioritaskan investasi infrastruktur (perumahan, transportasi, sekolah, kesehatan) di kabupaten dengan pertumbuhan tertinggi
2. Rancang program berbasis gender di kabupaten dengan sex ratio tinggi — perlindungan pekerja migran dan pemberdayaan perempuan
3. Evaluasi kebijakan tata kota di wilayah yang mengalami penurunan penduduk untuk merancang program revitalisasi pusat kota
4. Bangun sistem pemantauan kependudukan berbasis data yang diperbarui tahunan untuk mendukung *evidence-based policy*

---

## ☁️ Deploy ke Streamlit Cloud

Untuk membuat dashboard dapat diakses secara online:

### Langkah 1 — Push ke GitHub

```bash
git init
git add .
git commit -m "submission analisis data kependudukan jabar"
git remote add origin https://github.com/username/nama-repo.git
git push -u origin main
```

Pastikan struktur repositori GitHub adalah:
```
nama-repo/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   └── penduduk_jabar.csv
├── notebook.ipynb
├── README.md
└── requirements.txt
```

### Langkah 2 — Deploy di Streamlit Community Cloud

1. Buka [share.streamlit.io](https://share.streamlit.io)
2. Login menggunakan akun GitHub
3. Klik **New app**
4. Isi form:
   - **Repository:** `username/nama-repo`
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard.py`
5. Klik **Deploy!**

Streamlit akan otomatis menginstal library dari `requirements.txt` dan menjalankan dashboard. URL publik akan tersedia dalam format:
```
https://username-nama-repo-dashboard-dashboard-xxxx.streamlit.app
```

Salin URL tersebut dan tuliskan ke dalam file `url.txt`.

---

## 🔧 Troubleshooting

### ❌ Error: `ModuleNotFoundError`
Library belum terinstal. Jalankan ulang:
```bash
pip install -r requirements.txt
```

### ❌ Error: `streamlit: command not found`
Streamlit belum terdeteksi di PATH. Coba:
```bash
python -m streamlit run dashboard/dashboard.py
```

### ❌ Error: `FileNotFoundError: main_data.csv`
Dashboard harus dijalankan dari dalam folder `dashboard/`, bukan dari folder `submission/`:
```bash
# BENAR
cd dashboard
streamlit run dashboard.py

# SALAH (akan error)
streamlit run dashboard/dashboard.py
```

### ❌ Jupyter Notebook tidak bisa dijalankan
Install Jupyter:
```bash
pip install notebook ipykernel
python -m ipykernel install --user --name python3
```

### ❌ Port 8501 sudah digunakan
Jalankan di port lain:
```bash
streamlit run dashboard.py --server.port 8502
```

### ❌ Virtual environment tidak aktif
Pastikan virtual environment aktif sebelum menjalankan perintah apapun:
```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
Tanda aktif: muncul `(venv)` di awal prompt terminal.

---

## 👤 Informasi Proyek

| | |
|---|---|
| **Dataset** | Open Data Jawa Barat — Disdukcapil |
| **Kelas** | Belajar Analisis Data dengan Python — Dicoding |
| **Tools** | Python, Pandas, Matplotlib, Seaborn, Streamlit, Jupyter Notebook |
