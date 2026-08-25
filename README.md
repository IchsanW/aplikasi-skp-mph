# 🏛️ Aplikasi Penyusunan SKP & Matriks Peran Hasil (MPH) Berbasis AI Lokal

Aplikasi web privat dan offline untuk membantu penyusunan **Matriks Peran Hasil (MPH)** dan **Indikator Kinerja Individu (IKI) SKP** Aparatur Sipil Negara (ASN) sesuai dengan ketentuan **Permenpan RB No. 6 Tahun 2022** dan standar nomenklatur **Permen ATR/BPN No. 17 Tahun 2020**.

Aplikasi ini menggunakan model Large Language Model (LLM) yang berjalan **100% lokal/offline** di komputer Anda tanpa memerlukan koneksi internet, sehingga kerahasiaan data kinerja pegawai tetap terjaga aman.

---

## 🌟 Fitur Utama

- **Cascading Performance Matrix (MPH):** Penyusunan Rencana Hasil Kerja (RHK) otomatis yang berjenjang dari Atasan (Kakanwil/Kabag TU) ke bawahan (Kasubbag/Pelaksana).
- **Smart Elaborate & Steering IKI (SKP):** Mengubah kata kunci draf sederhana atau tugas ad-hoc pegawai di lapangan menjadi kalimat IKI kuantitatif berstandar **SMART-C** (*Jumlah...*, *Persentase...*, *Tingkat...*).
- **TUSI Boundary Guardrail:** Memiliki validasi otomatis untuk membelokkan atau menyesuaikan input tugas fisik agar tetap selaras dengan Tugas dan Fungsi (TUSI) jabatan resmi.
- **100% Privat & Offline:** Menggunakan peramban lokal dan Ollama AI engine tanpa mengirim data ke server luar.

---

## 🖥️ Spesifikasi Sistem Minimum

* **Sistem Operasi:** Windows 10 / 11 (64-bit)
* **RAM:** Minimum 8 GB (Disarankan 16 GB)
* **Penyimpanan:** Minimal 10 GB ruang kosong (untuk model AI)

---

## 🚀 Panduan Instalasi Cepat (Pengguna Baru)

### Langkah 1: Persiapan Aplikasi Utama (Diinstal Sekali Saja)

1. **Install Python (v3.11 atau v3.12):**
   - Unduh dari [python.org](https://www.python.org/downloads/).
   - ⚠️ **SANGAT PENTING:** Saat membuka installer, beri centang pada opsi **`Add python.exe to PATH`** di bagian bawah sebelum mengklik *Install Now*.
2. **Install Ollama AI Engine:**
   - Unduh dan jalankan installer dari [ollama.com/download](https://ollama.com/download).

---

### Langkah 2: Unduh & Setup Otomatis

1. Download repositori ini dengan mengklik tombol **`Code`** (warna hijau di kanan atas) $\rightarrow$ pilih **`Download ZIP`**.
2. Ekstrak file ZIP ke dalam folder di komputer Anda.
3. Klik **2 kali** pada file:
   ```text
   1-Installer-Otomatis.bat
