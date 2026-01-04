import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Factor Analysis Dashboard")

# 1. File Uploader for Streamlit
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # 2. Identify columns and calculate means
    factor_cols = [col for col in data.columns if col.startswith('Faktor')]
    
    if factor_cols:
        factor_means = data[factor_cols].mean().sort_values(ascending=False)

        # 3. Prepare data for Plotly
        plot_data = factor_means.reset_index()
        plot_data.columns = ['Factor', 'Average Score']
        plot_data['Factor'] = plot_data['Factor'].str.replace('Faktor ', '')

        # 4. Create Plotly Figure
        fig = px.bar(
            plot_data, 
            x='Average Score', 
            y='Factor',
            orientation='h',
            title='Average Score of Influencing Factors (Overall)',
            color='Average Score',
            color_continuous_scale='Viridis',
            labels={'Average Score': 'Average Score (1 - 5)', 'Factor': 'Factors'}
        )

        # Improve layout
        fig.update_layout(
            yaxis={'categoryorder':'total ascending'},
            xaxis_range=[1, 5],
            height=600
        )

        # 5. Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No columns starting with 'Faktor' were found in the dataset.")
