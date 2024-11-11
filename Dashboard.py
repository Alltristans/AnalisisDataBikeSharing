import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
all_df = pd.read_csv("all_data.csv")
day_df = pd.read_csv("day_data.csv")
hours_df = pd.read_csv("hours_data.csv")

# Convert 'dteday' to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hours_df['dteday'] = pd.to_datetime(hours_df['dteday'])

# --- Title ---
st.title("Dashboard Analisis Data Bike Sharing")

# --- Date Filter ---
start_date = st.date_input("Tanggal Awal", value=day_df['dteday'].min())
end_date = st.date_input("Tanggal Akhir", value=day_df['dteday'].max())

# Filter data based on date range
filtered_day_df = day_df[(day_df['dteday'].dt.date >= start_date) & (day_df['dteday'].dt.date <= end_date)]
filtered_hours_df = hours_df[(hours_df['dteday'].dt.date >= start_date) & (hours_df['dteday'].dt.date <= end_date)]

# --- Trend of Total Rentals Over Time ---
st.header("Tren Total Peminjaman")
st.line_chart(filtered_day_df.set_index('dteday')['cnt'])

# --- Demographics ---
st.header("Demografi")

# --- Weather Conditions ---
st.subheader("Kondisi Cuaca")
fig, ax = plt.subplots()
sns.boxplot(x='weathersit', y='cnt', data=filtered_day_df, ax=ax)
st.pyplot(fig)

# --- Weekends/Holidays/Working Days ---
st.subheader("Hari Libur/Akhir Pekan/Hari Kerja")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Hari Libur:")
    fig, ax = plt.subplots()
    sns.boxplot(x='holiday', y='cnt', data=filtered_day_df, ax=ax)
    st.pyplot(fig)

with col2:
    st.write("Akhir Pekan:")
    fig, ax = plt.subplots()
    sns.boxplot(x='is_weekend', y='cnt', data=filtered_day_df, ax=ax)
    st.pyplot(fig)

with col3:
    st.write("Hari Kerja:")
    fig, ax = plt.subplots()
    sns.boxplot(x='workingday', y='cnt', data=filtered_day_df, ax=ax)
    st.pyplot(fig)

# --- Best and Worst Seasons ---
st.header("Musim Terbaik dan Terburuk")

# Calculate total rentals for each season
season_rentals = filtered_day_df.groupby('season')['cnt'].sum().sort_values(ascending=False)

# Create a bar chart
fig, ax = plt.subplots()
sns.barplot(x=season_rentals.index, y=season_rentals.values, ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Total Peminjaman")
ax.set_title("Total Peminjaman per Musim")
st.pyplot(fig)

# --- User Type Percentage ---
st.header("Persentase Jenis Pengguna")

casual_percentage = (filtered_day_df['casual'].sum() / filtered_day_df['cnt'].sum()) * 100
registered_percentage = (filtered_day_df['registered'].sum() / filtered_day_df['cnt'].sum()) * 100

# Create a pie chart
fig, ax = plt.subplots()
ax.pie([casual_percentage, registered_percentage], labels=['Kasual', 'Terdaftar'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  
st.pyplot(fig)