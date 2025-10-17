import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lulu Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('lulu_uae_master_2000.csv')

df = load_data()

st.title("🛒 Lulu Hypermart UAE Dashboard")
st.metric("Total Sales (AED)", f"{df['line_value_aed'].sum():,.2f}")
st.plotly_chart(px.bar(df.groupby('department')['line_value_aed'].sum().reset_index(),
                       x='department', y='line_value_aed', title="Sales by Department"), use_container_width=True)
