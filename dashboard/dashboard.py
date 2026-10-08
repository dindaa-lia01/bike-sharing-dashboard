import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Interactive Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Styling visualisasi
sns.set_theme(style="whitegrid")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"

# ==========================================
# 2. MEMUAT DATA
# ==========================================
@st.cache_data
def load_data():
    # Menentukan path file main_data.csv secara dinamis
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    data_path = current_dir / "main_data.csv"
    
    # Jika dijalankan dari root folder
    if not data_path.exists():
        data_path = current_dir / "dashboard" / "main_data.csv"
        
    df = pd.read_csv(data_path)
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

df = load_data()

# ==========================================
# 3. SIDEBAR (FILTER INTERAKTIF)
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=500&q=80", use_container_width=True)
st.sidebar.title("Filter Analisis")

# Filter Rentang Tanggal
min_date = df["dteday"].min().date()
max_date = df["dteday"].max().date()

start_date, end_date = st.sidebar.date_input(
    label="Rentang Waktu:",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter Musim
all_seasons = list(df["season_label"].unique())
selected_seasons = st.sidebar.multiselect(
    label="Pilih Musim:",
    options=all_seasons,
    default=all_seasons
)

# Filter Cuaca
all_weathers = list(df["weather_label"].unique())
selected_weathers = st.sidebar.multiselect(
    label="Pilih Kondisi Cuaca:",
    options=all_weathers,
    default=all_weathers
)

# Menerapkan Filter pada Data
filtered_df = df[
    (df["dteday"].dt.date >= start_date) &
    (df["dteday"].dt.date <= end_date) &
    (df["season_label"].isin(selected_seasons)) &
    (df["weather_label"].isin(selected_weathers))
]

# Validasi jika data kosong setelah difilter
if filtered_df.empty:
    st.warning("Tidak ada data yang cocok dengan kombinasi filter yang dipilih. Silakan sesuaikan kembali filter Anda.")
    st.stop()

# ==========================================
# 4. HEADER UTAMA & KPI METRICS
# ==========================================
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Dashboard interaktif untuk memantau performa, tren waktu, pengaruh cuaca, dan segmentasi pengguna rental sepeda.")

total_sewa = filtered_df["cnt"].sum()
total_casual = filtered_df["casual"].sum()
total_registered = filtered_df["registered"].sum()
avg_harian = filtered_df.groupby("dteday")["cnt"].sum().mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{total_sewa:,}")
with col2:
    st.metric("Pengguna Kasual (Casual)", f"{total_casual:,}")
with col3:
    st.metric("Pengguna Terdaftar (Registered)", f"{total_registered:,}")
with col4:
    st.metric("Rata-rata Sewa/Hari", f"{avg_harian:,.0f} unit")

st.markdown("---")

# ==========================================
# 5. VISUALISASI PERTANYAAN BISNIS 1
# ==========================================
st.subheader("1. Pengaruh Faktor Lingkungan (Musim & Cuaca) terhadap Penyewaan")

tab1, tab2 = st.tabs(["Pengaruh Musim", "Pengaruh Cuaca"])

with tab1:
    col_a, col_b = st.columns([2, 1])
    with col_a:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        season_order = ["Fall", "Summer", "Winter", "Spring"]
        existing_seasons = [s for s in season_order if s in filtered_df["season_label"].unique()]
        
        sns.barplot(
            data=filtered_df,
            x="season_label",
            y="cnt",
            order=existing_seasons,
            palette="Blues_r",
            errorbar=None,
            ax=ax
        )
        ax.set_title("Rata-rata Sewa Sepeda Berdasarkan Musim", fontsize=12, weight="bold")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Jumlah Sewa (Unit)")
        st.pyplot(fig)
    with col_b:
        st.markdown("""
        **Insight Musim:**
        - **Musim Gugur (Fall)** dan **Musim Panas (Summer)** merupakan periode dengan permintaan sewa sepeda tertinggi karena suhu udara yang hangat dan mendukung aktivitas luar ruangan.
        - **Musim Semi (Spring)** memiliki tingkat sewa paling rendah akibat suhu awal tahun yang masih relatif dingin di Washington D.C.
        """)

with tab2:
    col_c, col_d = st.columns([2, 1])
    with col_c:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        weather_order = ["Clear / Few Clouds", "Mist / Cloudy", "Light Snow / Light Rain", "Heavy Rain / Ice Pellets"]
        existing_weathers = [w for w in weather_order if w in filtered_df["weather_label"].unique()]
        
        sns.barplot(
            data=filtered_df,
            x="weather_label",
            y="cnt",
            order=existing_weathers,
            palette="Oranges_r",
            errorbar=None,
            ax=ax
        )
        ax.set_title("Rata-rata Sewa Sepeda Berdasarkan Kondisi Cuaca", fontsize=12, weight="bold")
        ax.set_xlabel("Kondisi Cuaca")
        ax.set_ylabel("Rata-rata Jumlah Sewa (Unit)")
        plt.xticks(rotation=15)
        st.pyplot(fig)
    with col_d:
        st.markdown("""
        **Insight Cuaca:**
        - Kondisi **Cerah (Clear / Few Clouds)** mendominasi volume peminjaman harian tertinggi.
        - Ketika cuaca memburuk menjadi **Hujan/Salju Ringan**, volume penyewaan mengalami penurunan drastis hingga lebih dari 60%.
        """)

st.markdown("---")

# ==========================================
# 6. VISUALISASI PERTANYAAN BISNIS 2
# ==========================================
st.subheader("2. Pola Jam Sibuk (Peak Hours) & Perilaku Tipe Pengguna")

col_e, col_f = st.columns(2)

with col_e:
    hourly_work = filtered_df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
    hourly_work["tipe_hari"] = hourly_work["workingday"].map({1: "Hari Kerja", 0: "Hari Libur / Weekend"})
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(
        data=hourly_work,
        x="hr",
        y="cnt",
        hue="tipe_hari",
        palette=["#FF5733", "#1F77B4"],
        marker="o",
        linewidth=2,
        ax=ax
    )
    ax.set_title("Pola Jam Sewa: Hari Kerja vs Hari Libur", fontsize=12, weight="bold")
    ax.set_xlabel("Jam (0 - 23)")
    ax.set_ylabel("Rata-rata Sewa (Unit)")
    ax.set_xticks(range(0, 24, 2))
    ax.legend(title="Tipe Hari")
    st.pyplot(fig)
    st.caption("Pola bimodal terlihat jelas pada hari kerja dengan dua puncak lonjakan di jam komuter berangkat dan pulang kerja.")

with col_f:
    user_hourly = filtered_df.groupby("hr")[["casual", "registered"]].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(data=user_hourly, x="hr", y="registered", label="Pengguna Terdaftar", color="#2CA02C", linewidth=2, marker="s", ax=ax)
    sns.lineplot(data=user_hourly, x="hr", y="casual", label="Pengguna Kasual", color="#D62728", linewidth=2, marker="o", ax=ax)
    ax.set_title("Perbandingan Pola Jam Sewa: Casual vs Registered", fontsize=12, weight="bold")
    ax.set_xlabel("Jam (0 - 23)")
    ax.set_ylabel("Rata-rata Sewa (Unit)")
    ax.set_xticks(range(0, 24, 2))
    ax.legend(title="Tipe Pengguna")
    st.pyplot(fig)
    st.caption("Pengguna terdaftar mendominasi jam sibuk komuter, sedangkan pengguna kasual lebih aktif pada siang hingga sore hari.")

st.markdown("---")

# ==========================================
# 7. ANALISIS LANJUTAN (MANUAL CLUSTERING / BINNING)
# ==========================================
st.subheader("3. Analisis Lanjutan: Manual Clustering (Waktu vs Suhu)")

col_g, col_h = st.columns([2, 1])

with col_g:
    cluster_matrix = filtered_df.groupby(["time_of_day", "temp_group"])["cnt"].mean().unstack()
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.heatmap(
        cluster_matrix,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        cbar_kws={'label': 'Rata-rata Sewa Per Jam'},
        ax=ax
    )
    ax.set_title("Heatmap Klaster: Rata-rata Sewa Berdasarkan Waktu dan Suhu", fontsize=12, weight="bold")
    ax.set_xlabel("Kelompok Suhu")
    ax.set_ylabel("Kategori Bagian Hari")
    st.pyplot(fig)

with col_h:
    st.markdown("""
    **Segmentasi Klaster Manual:**
    - **Klaster Prime/Tertinggi**: Terbentuk pada kategori waktu **Malam (17-23)** dan **Siang/Sore (12-16)** dengan suhu **Hangat/Panas (>25°C)**.
    - **Klaster Terendah**: Terbentuk pada waktu **Dini Hari (00-05)** di semua kategori suhu, mengindikasikan waktu istirahat dan minimnya aktivitas mobilitas warga.
    """)

# Footer
st.caption("Proyek Analisis Data - Dicoding Collection Dashboard")