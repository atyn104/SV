import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# URL Data
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

try:
    data = load_data()

    # --- PERSEDIAAN DATA ---
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]
    kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
    langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

    # --- BAHAGIAN 1: PURATA SKOR ---
    st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion")
    st.write("Analisis visual ini mendedahkan punca utama kesesakan melalui perbandingan demografi dan status.")

    factor_means = data[factor_cols].mean().sort_values(ascending=True).reset_index()
    factor_means.columns = ['Factor', 'Average Score']
    factor_means['Factor'] = factor_means['Factor'].str.replace('Faktor ', '')

    fig1 = px.bar(
        factor_means, x='Average Score', y='Factor', orientation='h',
        title='<b>1. Average Factor Scores (Overall)</b>',
        color='Average Score', color_continuous_scale='Viridis', text_auto='.2f'
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 2: PERBANDINGAN DEMOGRAFI ---
    st.subheader("Sub-Analysis: Demographic")
    melted_data = data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols, var_name='Factor', value_name='Average Score')
    melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '')
    comparison_data = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()

    fig2 = px.bar(
        comparison_data, x='Average Score', y='Factor', color='Jenis Kawasan',
        barmode='group', orientation='h', title='<b>2. Comparison: Urban vs. Rural Areas</b>',
        text_auto='.2f'
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 3: HEATMAP ---
    st.subheader("🌡️ Heatmap Analysis")
    heatmap_df = data.groupby('Status')[factor_cols].mean()
    heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]

    fig3 = px.imshow(
        heatmap_df, color_continuous_scale='YlGnBu',
        title='<b>3. Heatmap: Factors by Status</b>', text_auto=".2f", aspect="auto"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- BAHAGIAN 4: HUBUNGAN (SCATTER PLOT) ---
    st.subheader("🔗 Relationship Analysis")
    c1, c2 = st.columns(2)
    with c1:
        f_select = st.selectbox("Select Factor (X):", factor_cols)
    with c2:
        k_select = st.selectbox("Select Impact (Y):", kesan_cols)

    # Nota: trendline="ols" memerlukan 'statsmodels' dalam requirements.txt
    fig5 = px.scatter(
        data, x=f_select, y=k_select, trendline="ols", 
        trendline_color_override="red", opacity=0.5,
        title=f"Regression: {f_select} vs {k_select}"
    )
    st.plotly_chart(fig5, use_container_width=True)

except Exception as e:
    st.error(f"Gagal memuatkan data atau ralat analisis: {e}")
