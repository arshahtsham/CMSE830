import streamlit as st
import pandas as pd

# Load the S&P 500 company data 
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
html = pd.read_html(url, header=0)
df = html[0]

# Streamlit app
st.title('S&P 500 Company Information')

# Sidebar
st.sidebar.title('Filter Options')
sector = st.sidebar.selectbox('Select Sector', df['GICS Sector'].unique())
industry = st.sidebar.selectbox('Select Industry', df[df['GICS Sector'] == sector]['GICS Sub-Industry'].unique())

# Filter the DataFrame based on user selections
filtered_df = df[(df['GICS Sector'] == sector) & (df['GICS Sub-Industry'] == industry)]

# Display the filtered data
st.write(f"Showing data for {sector} - {industry}")
st.dataframe(filtered_df)

# Additional features can be added as needed
