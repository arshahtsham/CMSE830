import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px  # Import Plotly Express for 3D scatter plot

# Load the iris dataset from Seaborn
iris_data = sns.load_dataset('iris')

# Update the text to describe the iris dataset
st.write("""
# Iris Dataset
This dataset contains information about different species of iris flowers.
""")

# Create a 3D scatter plot using Plotly Express
fig = px.scatter_3d(iris_data, x='sepal_length', y='sepal_width', z='petal_length',
                    color='species', size='petal_width', title='Iris Dataset 3D Scatter Plot')

# Show the plot in the Streamlit app
st.plotly_chart(fig)