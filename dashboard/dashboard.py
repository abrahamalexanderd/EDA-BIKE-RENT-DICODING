import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
# Nonexist 

# Load cleaned data
all_df = pd.read_csv("day.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Membuat kategori 'Hari Kerja' dan 'Akhir Pekan' menggunakan np.where
all_df['is_weekend'] = np.where(all_df['weekday'].isin([0, 6]), 'Weekend', 'Weekday')

# # Menyiapkan berbagai dataframe
# Nonexist

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


st.caption('Copyright © Abraham Alexander Dared 2024')