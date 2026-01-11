import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Analysis of Factors and Perceptions of Traffic Congestion in School Areas", layout="wide")

# 2. Masukkan URL data mentah
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

# 3. Baca data daripada GitHub (dengan Cache)
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

data = load_data()

# --- PERSEDIAAN DATA ASAS ---
factor_cols = [col for col in data.columns if col.startswith('Faktor')]
kesan_cols = [col for col in data.columns if col.startswith('Kesan')]
langkah_cols = [col for col in data.columns if col.startswith('Langkah')]

# --- BAHAGIAN 1: OVERALL AVERAGE SCORE ---
st.title("📊 Analysis of Factors and Perceptions of Traffic Congestion in School Areas")

factor_means = data[factor_cols].mean().sort_values(ascending=True)
plot_data_overall = factor_means.reset_index()
plot_data_overall.columns = ['Factor', 'Average Score']
plot_data_overall['Factor'] = plot_data_overall['Factor'].str.replace('Factor ', '')

fig1 = px.bar(
    plot_data_overall, 
    x='Average Score', 
    y='Factor',
    orientation='h',
    title='<b>1. Average Factor Scores (Overall)</b>',
    labels={'Average Score': 'Average Score', 'Factor': 'Factor'},
    color='Average Score',
    color_continuous_scale='Viridis',
    text_auto='.2f'
)
fig1.update_layout(xaxis_range=[0, 5], height=500)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# --- BAHAGIAN 2: DEMOGRAPHIC COMPARISON & STATUS HEATMAP ---
st.subheader("🏙️ Demographic Analysis")
col1, col2 = st.columns(2)

with col1:
    melted_data = data.melt(id_vars=['Jenis Kawasan'], value_vars=factor_cols, var_name='Factor', value_name='Average Score')
    melted_data['Factor'] = melted_data['Factor'].str.replace('Faktor ', '')
    comparison_data = melted_data.groupby(['Jenis Kawasan', 'Factor'])['Average Score'].mean().reset_index()
    fig2 = px.bar(comparison_data, x='Average Score', y='Factor', color='Jenis Kawasan', barmode='group', orientation='h',
                 title='<b>2. Comparison: Urban vs. Rural Areas</b>', labels={'Jenis Kawasan': 'Area Type'}, text_auto='.2f')
  fig2.update_layout(height=700)  
  st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# --- SECTION 3: HEATMAP ANALYSIS ---
st.subheader("🌡️ Heatmap Analysis")

with col2:
    heatmap_df = data.groupby('Status')[factor_cols].mean()
    heatmap_df.columns = [col.replace('Faktor ', '') for col in heatmap_df.columns]
    fig3 = px.imshow(heatmap_df, color_continuous_scale='YlGnBu', title='<b>3. Heatmap: Factors by Status</b>', text_auto=".2f", aspect="auto")
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# --- BAHAGIAN 3: RELATIONSHIP ANALYSIS (SCATTER PLOT) ---
# Matriks Korelasi telah dibuang mengikut permintaan
st.subheader("🔗 Relationship Between Factors & Impacts")

col_scatter_1, col_scatter_2 = st.columns([1, 2]) # Ratio untuk dropdown dan graf

with col_scatter_1:
    st.write("<b>Please select variables:</b>", unsafe_allow_html=True)
    f_select = st.selectbox("Select Factor (Paksi-X):", factor_cols)
    k_select = st.selectbox("Select Impact (Paksi-Y):", kesan_cols)

with col_scatter_2:
    fig5 = px.scatter(
        data, 
        x=f_select, 
        y=k_select, 
        trendline="ols", 
        trendline_color_override="red", 
        opacity=0.5,
        title=f"Regression Analysis: {f_select.replace('Faktor ','')} vs {k_select.replace('Kesan ','')}"
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# --- BAHAGIAN 4: CAUSE (FACTOR) VS SOLUTION (MEASURES) ---
st.subheader("💡 Summary: Main Causes vs. Proposed Solutions")
col5, col6 = st.columns(2)

f_means = data[factor_cols].mean().sort_values(ascending=True)
f_plot = f_means.reset_index()
f_plot.columns = ['Faktor', 'Skor']
f_plot['Faktor'] = f_plot['Faktor'].str.replace('Faktor ', '')

l_means = data[langkah_cols].mean().sort_values(ascending=True)
l_plot = l_means.reset_index()
l_plot.columns = ['Langkah', 'Skor']
l_plot['Langkah'] = l_plot['Langkah'].str.replace('Langkah ', '')

with col5:
    fig6 = px.bar(f_plot, x='Skor', y='Faktor', orientation='h',
                 title='<b>Punca Utama (Faktor)</b>',
                 color_discrete_sequence=['#e74c3c'], text_auto='.2f')
    fig6.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    fig7 = px.bar(l_plot, x='Skor', y='Langkah', orientation='h',
                 title='<b>Penyelesaian Paling Dipersetujui (Langkah)</b>',
                 color_discrete_sequence=['#2ecc71'], text_auto='.2f')
    fig7.update_layout(xaxis_range=[1, 5])
    st.plotly_chart(fig7, use_container_width=True)
