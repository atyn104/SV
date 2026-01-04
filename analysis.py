import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Kesesakan SV", layout="wide")

st.title("📊 Dashboard Analisis Faktor & Kesan Kesesakan Jalan Raya")

# URL data mentah (Gunakan salah satu; di sini saya gunakan DATA_URL untuk kemudahan Cloud Deployment)
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    # Jika anda ingin guna fail tempatan, tukar url kepada 'project data.csv'
    return pd.read_csv(url)

try:
    df = load_data(DATA_URL)
    
    # 2. Kenalpasti lajur penting
    faktor_cols = [col for col in df.columns if 'Faktor' in col]
    kesan_cols = [col for col in df.columns if 'Kesan' in col]
    
    # Mencipta Tab untuk navigasi yang lebih bersih
    tab1, tab2, tab3 = st.tabs(["📈 Analisis Faktor", "🔗 Korelasi & Hubungan", "🗺️ Heatmap Status"])

    # --- TAB 1: ANALISIS FAKTOR ---
    with tab1:
        st.header("Analisis Skor Faktor")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Skor Purata Keseluruhan")
            overall_means = df[faktor_cols].mean().sort_values(ascending=False).reset_index()
            overall_means.columns = ['Factor', 'Average Score']
            overall_means['Factor'] = overall_means['Factor'].str.replace('Faktor ', '')

            fig_ranking = px.bar(
                overall_means, x='Average Score', y='Factor', orientation='h',
                color='Average Score', color_continuous_scale='Viridis',
                text_auto='.2f', title="Ranking Faktor Keseluruhan"
            )
            fig_ranking.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_range=[1, 5])
            st.plotly_chart(fig_ranking, use_container_width=True)

        with col_b:
            st.subheader("Perbandingan Mengikut Kawasan")
            melted_df = df.melt(id_vars=['Jenis Kawasan'], value_vars=faktor_cols, 
                               var_name='Factor', value_name='Score')
            melted_df['Factor'] = melted_df['Factor'].str.replace('Faktor ', '')
            summary_area = melted_df.groupby(['Jenis Kawasan', 'Factor'])['Score'].mean().reset_index()

            fig_area = px.bar(
                summary_area, x='Score', y='Factor', color='Jenis Kawasan',
                barmode='group', orientation='h', text_auto='.2f',
                title="Skor Mengikut Jenis Kawasan"
            )
            fig_area.update_layout(xaxis_range=[1, 5])
            st.plotly_chart(fig_area, use_container_width=True)

    # --- TAB 2: KORELASI & HUBUNGAN ---
    with tab2:
        st.header("Analisis Hubungan Faktor vs Kesan")
        
        # Heatmap Korelasi
        st.subheader("Matriks Korelasi (Faktor vs Kesan)")
        correlation_matrix = df[faktor_cols + kesan_cols].corr()
        subset_corr = correlation_matrix.loc[faktor_cols, kesan_cols]
        # Bersihkan nama lajur untuk visual
        subset_corr.index = [c.replace('Faktor ', '') for c in subset_corr.index]
        subset_corr.columns = [c.replace('Kesan ', '') for c in subset_corr.columns]

        fig_corr = px.imshow(
            subset_corr, text_auto=".2f", aspect="auto",
            color_continuous_scale='YlGnBu',
            labels=dict(x="Kesan", y="Faktor", color="Korelasi")
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.divider()
        
        #
