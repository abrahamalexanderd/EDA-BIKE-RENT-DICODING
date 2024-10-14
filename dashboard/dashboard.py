import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px
import datetime

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
# Nonexist 

# Load cleaned data
all_df = pd.read_csv("dashboard/day.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Membuat kategori 'Hari Kerja' dan 'Akhir Pekan' menggunakan np.where
all_df['is_weekend'] = np.where(all_df['weekday'].isin([0, 6]), 'Weekend', 'Weekday')

# SIDEBAR
date_range = st.sidebar.date_input("Date Range Filter",
                              (all_df.dteday.min(),all_df.dteday.max()),
                              min_value=all_df.dteday.min(),
                              max_value=all_df.dteday.max(),
                              format="YYYY-MM-DD")

# filter data
if len(date_range)==2:
    all_df = all_df[(all_df['dteday']>=date_range[0].strftime("%Y-%m-%d"))&(all_df['dteday']<=date_range[1].strftime("%Y-%m-%d"))]

# plot number of daily orders
st.header('Bike Rental Dashboard :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = all_df.instant.count()
    st.metric("Total orders", value=total_orders)

with col2:
    pass

# Rentals Difference on Different Time Category
st.subheader("Rentals vs Time Category")


# Rata-rata Jumlah Penyewaan di Weekday vs Weekend dengan Plotly
fig = px.bar(all_df, x='is_weekend', y='cnt',
            labels={
                'is_weekend': 'Kategori Hari',
                'cnt': 'Jumlah Penyewaan Sepeda'
            },
            title='Rata-rata Jumlah Penyewaan Sepeda di Weekday vs Weekend',
            hover_data=['temp', 'hum', 'windspeed'],  # Menampilkan informasi tambahan saat hover
            color='is_weekend',  # Pewarnaan berdasarkan kategori (Weekday/Weekend)
            barmode='group',
            category_orders={"is_weekend": ['Weekday', 'Weekend']})  # Mengatur urutan kategori

st.plotly_chart(fig)


# Pengaruh Cuaca Terhadap Jumlah Pengguna Rental Sepeda dengan Plotly
fig = px.box(all_df, x='weathersit', y='cnt',
            labels={
                'weathersit': 'Situasi Cuaca',
                'cnt': 'Jumlah Penyewaan Sepeda'
            },
            title='Pengaruh Cuaca Terhadap Jumlah Pengguna Rental Sepeda',
            category_orders={"weathersit": [1, 2, 3]},  # Menentukan urutan kategori
            hover_data=['temp', 'hum', 'windspeed'])  # Menampilkan info tambahan saat hover

# Mengatur label kategori cuaca agar lebih deskriptif
fig.update_xaxes(tickvals=[1, 2, 3],
                ticktext=['Cerah/Mendung', 'Berkabut', 'Hujan Ringan'])

st.plotly_chart(fig)


st.caption('Copyright Â© Abraham Alexander Dared 2024')