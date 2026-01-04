import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Perbandingan Kawasan", layout="wide")

st.title("📊 Perbandingan Faktor Mengikut Jenis Kawasan")

# URL data anda
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    data = load_data(DATA_URL)

    # 2. Kenal pasti kolum 'Faktor'
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]

    if factor_cols:
        # 3. Tukar format data dari 'Wide' ke 'Long' (Melt)
        # Ini penting supaya Plotly boleh membezakan 'Jenis Kawasan'
        melted_data = data.melt(
            id_vars=['Jenis Kawasan'], 
            value_vars=factor_cols,
            var_name='Factor', 
            value_name='Average Score'
        )

        # 4. Bersihkan nama faktor (buang perkataan 'Faktor ')
        melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '', regex=False)

        # Kira purata berdasarkan Kawasan dan Faktor
        summary_df = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

        # 5. Bina Graf Plotly (Grouped Bar Chart)
        fig = px.bar(
            summary_df, 
            x='Average Score', 
            y='Factor',
            color='Jenis Kawasan',
            barmode='group',  # Membuat batang bersebelahan (side-by-side)
            orientation='h',
            title='Perbandingan Faktor Mengikut Jenis Kawasan',
            labels={'Average Score': 'Skor Purata (1 - 5)', 'Factor': 'Faktor'},
            color_discrete_sequence=px.colors.qualitative.Muted,
            text_auto='.2f'
        )

        # Kemas kini layout supaya lebih kemas
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            xaxis_range=[1, 5],
            height=800,
            legend_title_text='Jenis Kawasan'
        )

        # 6. Papar dalam Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Kolum 'Faktor' tidak dijumpai.")

except Exception as e:
    st.error(f"Ralat: {e}")
