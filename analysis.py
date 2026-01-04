import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Analisis Faktor SV", layout="wide")

st.title("📊 Dashboard Analisis Faktor")

# URL data anda
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    data = load_data(DATA_URL)
    
    with st.expander("Lihat Data Mentah"):
        st.write(data.head())

    # Kenal pasti kolum 'Faktor'
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]

    if factor_cols:
        # Kira purata skor
        factor_means = data[factor_cols].mean().sort_values(ascending=False)
        plot_data = factor_means.reset_index()
        plot_data.columns = ['Factor', 'Average Score']
        plot_data['Factor'] = plot_data['Factor'].str.replace('Faktor ', '', regex=False)

        # Visualisasi Plotly
        fig = px.bar(
            plot_data, 
            x='Average Score', 
            y='Factor',
            orientation='h',
            title='Purata Skor Faktor Pengaruh (Keseluruhan)',
            color='Average Score',
            color_continuous_scale='Viridis',
            labels={'Average Score': 'Skor Purata (1 - 5)', 'Factor': 'Faktor'},
            text_auto='.2f'
        )

        fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_range=[1, 5], height=600)

        # Papar graf
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Kolum 'Faktor' tidak dijumpai dalam fail CSV.")

except Exception as e:
    st.error(f"Ralat memuatkan data: {e}")
