import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Faktor SV", layout="wide")

st.title("📊 Dashboard Analisis Faktor")

# URL data mentah dari GitHub Anda
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    # Membaca data langsung dari URL GitHub
    return pd.read_csv(url)

try:
    # Memuat data
    data = load_data(DATA_URL)
    
    # Menampilkan sedikit cuplikan data
    with st.expander("Lihat Data Mentah"):
        st.write(data.head())

    # 1. Identifikasi kolom yang diawali dengan 'Faktor'
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]

    if factor_cols:
        # 2. Hitung rata-rata untuk setiap faktor
        factor_means = data[factor_cols].mean().sort_values(ascending=False)

        # 3. Format DataFrame untuk plotting
        plot_data = factor_means.reset_index()
        plot_data.columns = ['Factor', 'Average Score']
        
        # Sederhanakan nama faktor (buang kata 'Faktor ')
        plot_data['Factor'] = plot_data['Factor'].str.replace('Faktor ', '', regex=False)

        # 4. Visualisasi menggunakan Plotly Express
        fig = px.bar(
            plot_data, 
            x='Average Score', 
            y='Factor',
            orientation='h',
            title='Rata-rata Skor Faktor Pengaruh (Keseluruhan)',
            color='Average Score',
            color_continuous_scale='Viridis',
            labels={'Average Score': 'Skor Rata-rata (1 - 5)', 'Factor': 'Faktor'},
            text_auto='.2f'
        )

        # Memperbaiki tampilan layout
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            xaxis_range=[1, 5],
            height=600,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        # 5. Tampilkan graf di Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Kolom dengan awalan 'Faktor' tidak ditemukan dalam file CSV tersebut.")

except Exception as e:
    st.error(f"Gagal memuat data dari URL. Pastikan koneksi internet stabil atau URL benar. Error: {e}")
