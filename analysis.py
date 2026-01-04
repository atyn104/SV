import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Analisis Faktor SV", layout="wide")

st.title("📊 Perbandingan Faktor Mengikut Jenis Kawasan")

# URL data mentah anda (Pastikan URL ini betul dan boleh diakses)
DATA_URL = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/project_dataSV_data.csv"

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
        
        # Kira purata skor mengikut kawasan dan faktor
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

        fig.update_layout(
            xaxis_range=[1, 5], 
            height=800,
            yaxis={'categoryorder':'total ascending'}
        )

        # 6. Papar graf
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Ralat: Kolum yang bermula dengan perkataan 'Faktor' tidak dijumpai dalam CSV anda.")

except Exception as e:
    st.error(f"Ralat teknikal: {e}")


# --- Data Processing (Same as your original logic) ---
factor_cols = [col for col in data.columns if col.startswith('Faktor')]
factor_means = data[factor_cols].mean().sort_values(ascending=False)

plot_data = factor_means.reset_index()
plot_data.columns = ['Factor', 'Average Score']
plot_data['Factor'] = plot_data['Factor'].str.replace('Faktor ', '')

# --- Plotly Visualization ---
fig = px.bar(
    plot_data, 
    x='Average Score', 
    y='Factor', 
    orientation='h',  # Horizontal bar chart
    title='Average Score of Influencing Factors (Overall)',
    labels={'Average Score': 'Average Score (1 - 5)', 'Factor': 'Factors'},
    color='Average Score',      # Color bars by value
    color_continuous_scale='Viridis',
    text_auto='.2f'            # Automatically shows the value on the bar
)

# Improve layout for Streamlit
fig.update_layout(
    yaxis={'categoryorder': 'total ascending'}, # Ensures the highest score is at the top
    xaxis_range=[1, 5],                         # Set range based on your 1-5 scale
    height=600                                  # Adjust height based on number of factors
)

# --- Streamlit Display ---
st.plotly_chart(fig, use_container_width=True)

faktor_cols = [col for col in df.columns if 'Faktor' in col]

# Group and calculate mean
heatmap_data = df.groupby('Status')[faktor_cols].mean()

# Simplify factor names
heatmap_data.columns = [col.replace('Faktor ', '') for col in heatmap_data.columns]

# --- 2. Create Plotly Heatmap ---
fig = px.imshow(
    heatmap_data,
    text_auto='.2f',               # Replaces annot=True
    aspect="auto",                 # Ensures it fills the space properly
    color_continuous_scale='YlGnBu', # Matches your Seaborn cmap
    labels=dict(x="Faktor-faktor Kesesakan", y="Status Responden", color="Skor Purata"),
    title='Persepsi Faktor Kesesakan Mengikut Status Responden (Purata Skor)'
)

# --- 3. Refine Layout for Streamlit ---
fig.update_layout(
    xaxis_title='Faktor-faktor Kesesakan',
    yaxis_title='Status Responden',
    title_x=0.5,                   # Centers the title
)

# --- 4. Render in Streamlit ---
st.plotly_chart(fig, use_container_width=True)
