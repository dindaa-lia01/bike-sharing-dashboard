# Bike Sharing Data Analysis Dashboard 🚲

Proyek analisis data interaktif menggunakan Bike Sharing Dataset untuk memenuhi tugas submission Dicoding.

## Struktur Direktori
- `dashboard/`: Berisi kode aplikasi Streamlit (`dashboard.py`) dan dataset yang sudah dibersihkan (`main_data.csv`).
- `data/`: Berisi dataset mentah (`day.csv` dan `hour.csv`).
- `notebook.ipynb`: Berkas Jupyter Notebook proses analisis data lengkap dari Data Wrangling, EDA, hingga Analisis Lanjutan.
- `requirements.txt`: Daftar library Python yang dibutuhkan.
- `url.txt`: Tautan live dashboard yang sudah dideploy ke Streamlit Community Cloud.

## Cara Menjalankan Dashboard di Komputer Lokal

1. Clone repositori ini atau download sebagai ZIP lalu ekstrak.
2. Buka terminal / command prompt, arahkan ke folder proyek:
   ```bash
   cd submission

## Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate # Untuk Linux/Mac
venv\Scripts\activate # Untuk Windows

## Install library yang dibutuhkan:
pip install -r requirements.txt

## Jalankan aplikasi Streamlit:
streamlit run dashboard/dashboard.py
