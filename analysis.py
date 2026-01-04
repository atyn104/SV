import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Analisis Faktor SV", layout="wide")

st.title("📊 Analisis Faktor Kesesakan")

# URL data mentah
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    # Load data into 'data' variable
    data = load_data(DATA_URL)
    
    # 2. Identify columns starting with 'Faktor'
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]

    if factor_cols:
        # --- CHART 1: Comparison by Jenis Kawasan ---
        st.subheader("1. Perbandingan Mengikut Jenis Kawasan")
        
        # Melt data for grouped bar chart
        melted_data = data.melt(
            id_vars=['Jenis Kawasan'], 
            value_vars=factor_cols,
            var_name='Factor', 
            value_name='Score'
        )
        # Clean factor names
        melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '', regex=False)
        
        # Calculate mean per area and factor
        summary_area = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Score'].mean().reset_index()

        fig1 = px.bar(
            summary_area, x='Score', y='Factor', color='Jenis Kawasan',
            barmode='group', orientation='h', text_auto='.2f',
            title='Skor Purata Faktor Mengikut Jenis Kawasan',
            labels={'Score': 'Skor Purata', 'Factor': 'Faktor'},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig1.update_layout(xaxis_range=[1, 5], height=600)
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        # --- CHART 2: Overall Factor Ranking ---
        st.subheader("2. Skor Purata Keseluruhan (Ranking)")
        
        # Calculate mean for each factor column
        overall_means = data[factor_cols].mean().sort_values(ascending=False).reset_index()
        overall_means.columns = ['Factor', 'Average Score']
        overall_means['Factor'] = overall_means['Factor'].str.replace('Faktor ', '')

        fig2 = px.bar(
            overall_means, x='Average Score', y='Factor', orientation='h',
            title='Ranking Faktor Keseluruhan (Tertinggi ke Terendah)',
            color='Average Score', color_continuous_scale='Viridis',
            text_auto='.2f'
        )
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_range=[1, 5], height=500)
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # --- CHART 3: Heatmap (Status vs Factors) ---
        st.subheader("3. Heatmap Persepsi Mengikut Status")
        
        # Group by Status and get mean
        heatmap_df = data.groupby('Status')[factor_cols].mean()
        # Clean names for heatmap axes
        heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]

        fig3 = px.imshow(
            heatmap_df, text_auto='.2f', aspect="auto",
            color_continuous_scale='YlGnBu',
            title='Hubungan Status Responden dengan Faktor Kesesakan',
            labels=dict(x="Faktor", y="Status Responden", color="Skor Purata")
        )
        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.error("Ralat: Tiada kolum 'Faktor' ditemui dalam data.")

except Exception as e:
    st.error(f"Ralat teknikal semasa memproses data: {e}")
