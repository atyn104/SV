import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Kesesakan SV", layout="wide")

st.title("📊 Dashboard Analisis Kesesakan Jalan Raya")

# URL data mentah daripada GitHub
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(DATA_URL)
    
    # Kenalpasti lajur berdasarkan kata kunci
    faktor_cols = [col for col in df.columns if 'Faktor' in col]
    kesan_cols = [col for col in df.columns if 'Kesan' in col]
    langkah_cols = [col for col in df.columns if 'Langkah' in col]
    
    # 2. Mencipta Tab Navigasi
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Analisis Faktor & Kesan", 
        "🛠️ Langkah Penyelesaian",
        "🔗 Korelasi & Hubungan", 
        "🗺️ Heatmap Status"
    ])

    # --- TAB 1: ANALISIS FAKTOR & KESAN ---
    with tab1:
        st.header("Analisis Skor Faktor & Kesan")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Ranking Faktor Utama")
            f_means = df[faktor_cols].mean().sort_values(ascending=True).reset_index()
            f_means.columns = ['Factor', 'Score']
            f_means['Factor'] = f_means['Factor'].str.replace('Faktor ', '', regex=False)

            fig_f = px.bar(f_means, x='Score', y='Factor', orientation='h',
                          color='Score', color_continuous_scale='Reds',
                          text_auto='.2f', range_x=[1,5])
            st.plotly_chart(fig_f, use_container_width=True)

        with col_b:
            st.subheader("Ranking Kesan Utama")
            k_means = df[kesan_cols].mean().sort_values(ascending=True).reset_index()
            k_means.columns = ['Kesan', 'Score']
            k_means['Kesan'] = k_means['Kesan'].str.replace('Kesan ', '', regex=False)

            fig_k = px.bar(k_means, x='Score', y='Kesan', orientation='h',
                          color='Score', color_continuous_scale='Blues',
                          text_auto='.2f', range_x=[1,5])
            st.plotly_chart(fig_k, use_container_width=True)

    # --- TAB 2: LANGKAH PENYELESAIAN ---
    with tab2:
        st.header("Analisis Langkah Penyelesaian")
        l_means = df[langkah_cols].mean().sort_values(ascending=True).reset_index()
        l_means.columns = ['Langkah', 'Score']
        l_means['Langkah'] = l_means['Langkah'].str.replace('Langkah ', '', regex=False)

        fig_l = px.bar(l_means, x='Score', y='Langkah', orientation='h',
                      color='Score', color_continuous_scale='Greens',
                      text_auto='.2f', range_x=[1,5],
                      title="Tahap Persetujuan Langkah Penyelesaian")
        st.plotly_chart(fig_l, use_container_width=True)

    # --- TAB 3: KORELASI & HUBUNGAN ---
    with tab2: # Note: Jika menggunakan tab navigasi, pastikan index 'with' betul
        pass # Kod di bawah diletakkan dalam tab3

    with tab3:
        st.header("Hubungan Faktor vs Kesan")
        
        # Heatmap Korelasi
        corr = df[faktor_cols + kesan_cols].corr().loc[faktor_cols, kesan_cols]
        corr.index = [c.replace('Faktor ', '') for c in corr.index]
        corr.columns = [c.replace('Kesan ', '') for c in corr.columns]

        fig_heatmap = px.imshow(corr, text_auto=".2f", aspect="auto",
                               color_continuous_scale='YlGnBu', title="Matriks Korelasi")
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.divider()
        
        # Scatter Plot (Garis Trend)
        st.subheader("Scatter Plot (Analisis Regresi)")
        c1, c2 = st.columns(2)
        with c1:
            x_sel = st.selectbox("Pilih Faktor (X):", faktor_cols)
        with c2:
            y_sel = st.selectbox("Pilih Kesan (Y):", kesan_cols)

        fig_scatter = px.scatter(df, x=x_sel, y=y_sel, trendline="ols", opacity=0.5)
        fig_scatter.update_traces(line=dict(color="red"))
        st.plotly_
