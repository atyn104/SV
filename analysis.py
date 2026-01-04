import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Analisis Faktor SV", layout="wide")

st.title("📊 Perbandingan Faktor Mengikut Jenis Kawasan")

# URL data mentah anda
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/test/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    data = load_data(DATA_URL)

    # 2. Kenal pasti kolum 'Faktor'
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]

    if factor_cols:
        # 3. Tukar format data (Melt) untuk perbandingan Jenis Kawasan
        melted_data = data.melt(
            id_vars=['Jenis Kawasan'], 
            value_vars=factor_cols,
            var_name='Factor', 
            value_name='Average Score'
        )

        # 4. Bersihkan nama faktor
        melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '', regex=False)
        summary_df = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

        # 5. Bina Graf Plotly (Grouped Bar)
        fig = px.bar(
            summary_df, 
            x='Average Score', 
            y='Factor',
            color='Jenis Kawasan',
            barmode='group',
            orientation='h',
            title='Perbandingan Faktor Mengikut Jenis Kawasan',
            labels={'Average Score': 'Skor Purata (1 - 5)', 'Factor': 'Faktor'},
            text_auto='.2f'
        )

        fig.update_layout(xaxis_range=[1, 5], height=800)

        # 6. Papar graf
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Kolum 'Faktor' tidak dijumpai.")

except Exception as e:
    st.error(f"Ralat: {e}")
