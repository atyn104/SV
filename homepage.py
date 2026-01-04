import streamlit as st
import pandas as pd

st.header("Survey Dataset: Public Opinions on School Traffic Congestion During Peak Hours")

# Load Google Sheet CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8nPPwgVKnGxpQLQFTH6EQLpO6l1l2BlEAdGqmb0Bq7FGQzViLwKbb78NMjJSA1-eHl-Ebq5Wl4LRU/pub?gid=745446698&single=true&output=csv"
df = pd.read_csv(url)

# Remove unnecessary columns
df = df.drop(columns=["Timestamp", "Score", "What language do you prefer?\n  Apakah bahasa pilihan anda?  "], errors="ignore")

#Count total submitted
total_all = len(df)
st.write(f"Total Respondents: {total_all}/100  ")

# --------------------------------------------------------
# 1) FIXED NAMES FOR ENGLISH COLUMNS
# --------------------------------------------------------
fixed_columns_en = {
    df.columns[0]: "Age Group",
    df.columns[1]: "Status",
    df.columns[2]: "Gender",
    df.columns[3]: "Race",
    df.columns[4]: "Area Type",
    df.columns[5]: "Rainy Weather Factor",
    df.columns[6]: "Increasing Population Factor",
    df.columns[7]: "Undisciplined Driver Factor",
    df.columns[8]: "Damaged Road Factor",
    df.columns[9]: "Students Not Sharing Vehicles",
    df.columns[10]: "Leaving Work Late Factor",
    df.columns[11]: "Narrow Road Factor",
    df.columns[12]: "Single Gate Factor",
    df.columns[13]: "Lack of Pedestrian Bridge Factor",
    df.columns[14]: "Lack of Parking Space Factor",
    df.columns[15]: "Late Drop-off/Pick-up Factor",
    df.columns[16]: "Construction/Roadworks Factor",
    df.columns[17]: "Unintended Road Accidents Effect",
    df.columns[18]: "Time Wastage Effect",
    df.columns[19]: "Pressure on Road Users Effect",
    df.columns[20]: "Students Late to School Effect",
    df.columns[21]: "Environmental Pollution Effect",
    df.columns[22]: "Fuel Wastage Effect",
    df.columns[23]: "Pedestrian Bridge Step",
    df.columns[24]: "Widening Road Step",
    df.columns[25]: "Vehicle Sharing Step",
    df.columns[26]: "Two Gates Step",
    df.columns[27]: "Arrive Early Step",
    df.columns[28]: "Traffic Officers Step",
    df.columns[29]: "Special Drop-off Area Step"
}

df_english = df.rename(columns=fixed_columns_en)

# --------------------------------------------------------
# 2) FIXED NAMES FOR MALAY COLUMNS
# --------------------------------------------------------
# (Assuming Malay columns are in positions 30 onward — adjust based on your sheet)
fixed_columns_my = {
    df.columns[30]: "Kumpulan Umur",
    df.columns[31]: "Status",
    df.columns[32]: "Jantina",
    df.columns[33]: "Bangsa",
    df.columns[34]: "Jenis Kawasan",
    df.columns[35]: "Faktor Cuaca Hujan",
    df.columns[36]: "Faktor Peningkatan Populasi",
    df.columns[37]: "Faktor Pemandu Tidak Berdisiplin",
    df.columns[38]: "Faktor Kerosakan Jalan",
    df.columns[39]: "Faktor Pelajar Tidak Berkongsi Kenderaan",
    df.columns[40]: "Faktor Bertolak Lewat ke Tempat Kerja",
    df.columns[41]: "Faktor Jalan Sempit",
    df.columns[42]: "Faktor Satu Pintu Masuk/Keluar",
    df.columns[43]: "Faktor Kekurangan Jejambat Pejalan Kaki",
    df.columns[44]: "Faktor Kekurangan Ruang Parkir",
    df.columns[45]: "Faktor Ibu Bapa Lewat Hantar/Ambil Anak",
    df.columns[46]: "Faktor Pembinaan / Kerja Jalan",
    df.columns[47]: "Kesan Kemalangan Jalan Raya",
    df.columns[48]: "Kesan Pembaziran Masa",
    df.columns[49]: "Kesan Tekanan pada Pengguna Jalan",
    df.columns[50]: "Kesan Pelajar Lewat ke Sekolah",
    df.columns[51]: "Kesan Pencemaran Alam Sekitar",
    df.columns[52]: "Kesan Pembaziran Bahan Api",
    df.columns[53]: "Langkah Jejambat Pejalan Kaki",
    df.columns[54]: "Langkah Melebarkan Jalan",
    df.columns[55]: "Langkah Berkongsi Kenderaan",
    df.columns[56]: "Langkah Dua Pintu Masuk/Keluar",
    df.columns[57]: "Langkah Tiba Awal ke Sekolah",
    df.columns[58]: "Langkah Menempatkan Pegawai Trafik",
    df.columns[59]: "Langkah Kawasan Khas Hantar/Tunggu Anak"
}

df_malay = df.rename(columns=fixed_columns_my)


# --------------------------------------------------------
# KEEP ONLY RELEVANT COLUMNS FOR EACH LANGUAGE
# --------------------------------------------------------

# English only → keep English columns only
df_english = df_english[list(fixed_columns_en.values())]

# Malay only → keep Malay columns only
df_malay = df_malay[list(fixed_columns_my.values())]

# --------------------------------------------------------
# REMOVE EMPTY ROWS (people who answered in the other language)
# --------------------------------------------------------
df_english = df_english.dropna(subset=["Age Group"], how="all")
df_malay = df_malay.dropna(subset=["Kumpulan Umur"], how="all")

# --------------------------------------------------------
# FIX ROW NUMBER CONFUSION
# --------------------------------------------------------
df_english = df_english.reset_index(drop=True)
df_malay = df_malay.reset_index(drop=True)

# --------------------------------------------------------
# SHOW OUTPUT
# --------------------------------------------------------
st.subheader("English Responses Only")
st.dataframe(df_english)

st.subheader("Malay Responses Only")
st.dataframe(df_malay)

#--------------------------
# Cleaned Dataset
#--------------------------
# Load Google Sheet CSV
url = "https://raw.githubusercontent.com/wannurizzatiwanabdazizktb-arch/SV-Project/refs/heads/main/cleaned_data.csv"
df_cleaned = pd.read_csv(url)

st.subheader("Cleaned Dataset")
st.dataframe(df_cleaned)

#Count total submitted
total_all = len(df_cleaned)
st.write(f"Total Respondents: {total_all}")

#-----------------------
# CONTOH
#-----------------------

import plotly.graph_objects as go

urban_df = df_cleaned[df_cleaned['Area Type'] == 'Urban areas']

likert_cols = [
    col for col in df_cleaned.columns
    if 'Factor' in col or 'Effect' in col or 'Step' in col
]

def classify_item(col):
    if 'Factor' in col:
        return 'Factor'
    elif 'Effect' in col:
        return 'Effect'
    elif 'Step' in col:
        return 'Step'
    else:
        return 'Other'

disagreement_data = []

for col in likert_cols:
    if col in urban_df.columns:
        count_sd = (urban_df[col] == 1).sum()
        count_d  = (urban_df[col] == 2).sum()

        if count_sd > 0 or count_d > 0:
            disagreement_data.append({
                'Likert Scale Item': col,
                'Item Category': classify_item(col),
                'Strongly Disagree (1)': count_sd,
                'Disagree (2)': count_d
            })

disagreement_df = pd.DataFrame(disagreement_data)

disagreement_df['Total'] = (
    disagreement_df['Strongly Disagree (1)'] +
    disagreement_df['Disagree (2)']
)

disagreement_df = disagreement_df.sort_values('Total')

fig = go.Figure()

fig.add_trace(go.Bar(
    x=disagreement_df['Strongly Disagree (1)'],
    y=disagreement_df['Likert Scale Item'],
    orientation='h',
    name='Strongly Disagree (1)'
))

fig.add_trace(go.Bar(
    x=disagreement_df['Disagree (2)'],
    y=disagreement_df['Likert Scale Item'],
    orientation='h',
    name='Disagree (2)'
))

fig.update_layout(
    title='Disagreement Responses (1 vs 2) among Urban Respondents',
    xaxis_title='Number of Disagreement Responses',
    yaxis_title='Likert Scale Item',
    barmode='group',
    template='plotly_white',
    height=900
)

st.plotly_chart(fig)
st.dataframe(disagreement_df)
