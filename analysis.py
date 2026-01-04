import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load your data
# Ensure your CSV file is in the same folder as this script
url = "https://raw.githubusercontent.com/atyn104/SV/refs/heads/main/employment_sector.csv"
data = pd.read_csv(url) 

# 2. Identify columns related to 'Factors'
factor_cols = [col for col in data.columns if col.startswith('Faktor')]

# 3. Calculate means and sort
factor_means = data[factor_cols].mean().sort_values(ascending=False)

# 4. Format for plotting
plot_data = factor_means.reset_index()
plot_data.columns = ['Factor', 'Average Score']
plot_data['Factor'] = plot_data['Factor'].str.replace('Faktor ', '')

# 5. Visualization
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(
    data=plot_data, 
    x='Average Score', 
    y='Factor',
    hue='Factor', 
    palette='viridis',
    ax=ax
)

plt.title('Average Score of Influencing Factors (Overall)')
plt.xlabel('Average Score (1 - 5)')
plt.ylabel('Factors')

# 6. Save results
# Create an 'outputs' folder if it doesn't exist
os.makedirs('outputs', exist_ok=True)
plt.tight_layout()
plt.savefig('outputs/average_factor_scores.png')
st.pyplot(fig)
