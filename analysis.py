import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Kesesakan SV", layout="wide")

st.title("📊 Dashboard Analisis Faktor, Kesan & Penyelesaian")

# URL data mentah daripada GitHub
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# --- MULA BLOK TRY ---
try:
    df = load_data(DATA_URL)
    
    # Kenalpasti lajur
    faktor_cols = [col for col in df.columns if 'Faktor' in col]
    kesan_cols = [col for col in df.columns if 'Kesan' in col]
    langkah_cols = [col for col in df.columns if 'Langkah' in col]
    
    # 2. Mencipta Tab Navigasi
    tab1, tab2, tab3 = st.tabs([
        "📈 Faktor & Langkah", 
        "🔗 Korelasi & Hubungan", 
        "🗺️ Analisis Status"
    ])

    # --- TAB 1: FAKTOR VS LANGKAH ---
    with tab1:
        st.header("Perbandingan Punca dan Penyelesaian")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Punca Utama (Faktor)")
            f_means = df[faktor_cols].mean().sort_values(ascending=True).reset_index()
            f_means.columns = ['Faktor', 'Skor']
            f_means['Faktor'] = f_means['Faktor'].str.replace('Faktor ', '', regex=False)
            
            fig_f = px.bar(f_means, x='Skor', y='Faktor', orientation='h',
                          color='Skor', color_continuous_scale='Reds', range_x=[1, 5])
            st.plotly_chart(fig_f, use_container_width=True)

        with col2:
            st.subheader("Penyelesaian (Langkah)")
            l_means = df[langkah_cols].mean().sort_values(ascending=True).reset_index()
            l_means.columns = ['Langkah', 'Skor']
            l_means['Langkah'] = l_means['Langkah'].str.replace('Langkah ', '', regex=False)
            
            fig_l = px.bar(l_means, x='Skor', y='Langkah', orientation='h',
                          color='Skor', color_continuous_scale='Greens', range_x=[1, 5])
            st.plotly_chart(fig_l, use_container_width=True)

    # --- TAB 2: KORELASI & SCATTER ---
    with tab2:
        st.header("Analisis Hubungan Faktor & Kesan")
        
        # Matriks Korelasi
        corr = df[faktor_cols + kesan_cols].corr().loc[faktor_cols, kesan_cols]
        corr.index = [c.replace('Faktor ', '') for c in corr.index]
        corr.columns = [c.replace('Kesan ', '') for c in corr.columns]
        
        fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale='YlGnBu')
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.divider()
        
        # Scatter Plot (Pastikan kurungan ditutup rapat)
        st.subheader("Scatter Plot (Trendline)")
        c1, c2 = st.columns(2)
        with c1:
            x_axis = st.selectbox("Pilih Faktor (X):", faktor_cols)
        with c2:
            y_axis = st.selectbox("Pilih Kesan (Y):", kesan_cols)
            
        fig_scatter = px.scatter(
            df, 
            x=x_axis, 
            y=y_axis, 
            trendline="ols", 
            opacity=0.5,
            labels={x_axis: "Skor Faktor", y_axis: "Skor Kesan"}
        )
        fig_scatter.update_traces(line=dict(color="red"))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- TAB 3: HEATMAP STATUS ---
    with tab3:
        st.header("Analisis Mengikut Status Responden")
        if 'Status' in df.columns:
            h_status = df.groupby('Status')[faktor_cols].mean()
            h_status.columns = [c.replace('Faktor ', '') for c in h_status.columns]
            fig_h = px.imshow(h_status, text_auto='.2f', color_continuous_scale='YlGnBu')
            st.plotly_chart(fig_h, use_container_width=True)

# --- BLOK EXCEPT ---
except Exception as e:
    st.error(f"Ralat teknikal: {e}")
