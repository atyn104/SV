import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Dashboard Analisis Kesesakan SV", layout="wide")

st.title("📊 Dashboard Analisis Faktor & Kesan Kesesakan")

# URL data mentah daripada GitHub anda
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# --- MULA PROSES DATA ---
try:
    df = load_data(DATA_URL)
    
    # Kenalpasti lajur berdasarkan kata kunci
    faktor_cols = [col for col in df.columns if 'Faktor' in col]
    kesan_cols = [col for col in df.columns if 'Kesan' in col]
    
    # 2. Mencipta Tab Navigasi untuk susunan yang kemas
    tab1, tab2, tab3 = st.tabs(["📈 Analisis Faktor", "🔗 Korelasi & Hubungan", "🗺️ Heatmap Status"])

    # --- TAB 1: ANALISIS FAKTOR (BAR CHARTS) ---
    with tab1:
        st.header("Analisis Skor Faktor")
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Skor Purata Keseluruhan
            overall_means = df[faktor_cols].mean().sort_values(ascending=False).reset_index()
            overall_means.columns = ['Factor', 'Average Score']
            overall_means['Factor'] = overall_means['Factor'].str.replace('Faktor ', '', regex=False)

            fig_ranking = px.bar(
                overall_means, x='Average Score', y='Factor', orientation='h',
                color='Average Score', color_continuous_scale='Viridis',
                text_auto='.2f', title="Ranking Faktor Keseluruhan"
            )
            fig_ranking.update_layout(xaxis_range=[1, 5], yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_ranking, use_container_width=True)

        with col_b:
            # Perbandingan Mengikut Kawasan
            melted_df = df.melt(id_vars=['Jenis Kawasan'], value_vars=faktor_cols, 
                               var_name='Factor', value_name='Score')
            melted_df['Factor'] = melted_df['Factor'].str.replace('Faktor ', '', regex=False)
            summary_area = melted_df.groupby(['Jenis Kawasan', 'Factor'])['Score'].mean().reset_index()

            fig_area = px.bar(
                summary_area, x='Score', y='Factor', color='Jenis Kawasan',
                barmode='group', orientation='h', text_auto='.2f',
                title="Skor Mengikut Jenis Kawasan"
            )
            fig_area.update_layout(xaxis_range=[1, 5])
            st.plotly_chart(fig_area, use_container_width=True)

    # --- TAB 2: KORELASI & HUBUNGAN (SCATTER & HEATMAP) ---
    with tab2:
        st.header("Analisis Hubungan Faktor vs Kesan")
        
        # Heatmap Korelasi Matriks
        correlation_matrix = df[faktor_cols + kesan_cols].corr()
        subset_corr = correlation_matrix.loc[faktor_cols, kesan_cols]
        # Memudahkan nama label
        subset_corr.index = [c.replace('Faktor ', '') for c in subset_corr.index]
        subset_corr.columns = [c.replace('Kesan ', '') for c in subset_corr.columns]

        fig_corr = px.imshow(
            subset_corr, text_auto=".2f", aspect="auto",
            color_continuous_scale='YlGnBu',
            title="Matriks Korelasi (Hubungan Faktor & Kesan)"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        st.divider()
        
        # Scatter Plot dengan Garis Trend (Memerlukan statsmodels)
        st.subheader("Hubungan Spesifik (Scatter Plot)")
        c1, c2 = st.columns(2)
        with c1:
            x_sel = st.selectbox("Pilih Faktor (X-Axis):", faktor_cols)
        with c2:
            y_sel = st.selectbox("Pilih Kesan (Y-Axis):", kesan_cols)

        fig_scatter = px.scatter(
            df, x=x_sel, y=y_sel, trendline="ols", opacity=0.5,
            title=f"Analisis Regresi: {x_sel} vs {y_sel}",
            labels={x_sel: "Skor Faktor", y_sel: "Skor Kesan"}
        )
        fig_scatter.update_traces(line=dict(color="red"))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- TAB 3: HEATMAP STATUS (GROUPED ANALYSIS) ---
    with tab3:
        st.header("Persepsi Mengikut Status Responden")
        if 'Status' in df.columns:
            heatmap_status = df.groupby('Status')[faktor_cols].mean()
            heatmap_status.columns = [c.replace('Faktor ', '') for c in heatmap_status.columns]

            fig_status = px.imshow(
                heatmap_status, text_auto='.2f', aspect="auto",
                color_continuous_scale='YlGnBu',
                title="Purata Skor Faktor Mengikut Kategori Status"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        else:
            st.warning("Lajur 'Status' tidak dijumpai dalam dataset anda.")

except Exception as e:
    st.error(f"Ralat teknikal: {e}")
