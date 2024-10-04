import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime
from scipy.stats import linregress
import plotly.graph_objects as go
import plotly.express as px

st.markdown("""<h1 style='text-align: center;'
            >Projek Analisis Data: Bike Sharing Dataset</h1>
            oleh: Khoirul Hafidh Purwaraharjo / m200b4ky2213@bangkit.academy / m200b4ky2213
            """, unsafe_allow_html=True)

st.write("")
st.write("")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Pokok Bahasan", ["Penjelasan Dataset", "Pola dan Trend Data", "Pengaruh Cuaca dan Musim", "Korelasi Antar Variabel", "Kesimpulan"])

# Load data
@st.cache_data
def load_data():
    # Data 1 (Data Hour)
    file_data_hour = 'https://drive.google.com/uc?id=1wkscND280FML8nhjNEBD6fVz23Qf-k_1&export=download'
    # Data 2 (Data Day)
    file_data_day = 'https://drive.google.com/uc?id=1N67xh3SopmzNVI0An74yCLORV93TiS1s&export=download'

    data_hour = pd.read_csv(file_data_hour)
    data_day = pd.read_csv(file_data_day)
    data_day['dteday'] = pd.to_datetime(data_day['dteday'])
    return data_hour, data_day

data_hour, data_day = load_data()

# Page 1
if page == "Penjelasan Dataset":
    st.subheader('Analisis Jumlah Penyewaan Sepeda terhadap Cuaca dan Musim')
    st.markdown("""
    <div style='text-align: justify;'>
    Sebuah analisa dan visualisasi data mengenai bagaimana cuaca dan musim dapat mempengaruhi jumlah penyewaan sepeda. Data yang digunakan yaitu data jumlah penyewaan sepeda di Washington D.C., USA pada tahun 2011 hingga 2012. 
    Data yang digunakan dikumpulkan menjadi dua basis yaitu data penyewaan per jam dan data penyewaan per hari. Telah ditambahkan juga data informasi cuaca dan musim yang sesuai pada periode yang sama.<br>
    Sumber Dataset yang diakses pada laman https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset.
    </div>
    """, unsafe_allow_html=True)

    st.write('')
    st.subheader("Data Penyewaan Sepeda")
    st.write("Data penyewaan sepeda dibagi menjadi 2 data, yaitu:")
    st.write("1. Data penyewa dalam jam (data_hour)")
    st.write("2. Data penyewa dalam hari (data_day)")
    st.write("")

    st.subheader("Data Penyewaan dalam Jam")
    st.dataframe(data=data_hour, width=500000, height=420)
    st.write("")
    st.subheader("Data Penyewaan dalam Hari")
    st.dataframe(data=data_day, width=500000, height=420)

# Page 2
if page == "Pola dan Trend Data":
    st.subheader("Pola dan Trend Data Jumlah Penyewaan Sepeda")
    data_day['dteday'] = pd.to_datetime(data_day['dteday'])
    fig, ax = plt.subplots(figsize=(15, 6))
        
    ax.plot(data_day['dteday'], data_day['cnt'])
    ax.grid(True)
    ax.set_ylabel('Jumlah Penyewaan Sepeda')
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45, ha='right')

    season_changes = [data_day['dteday'].iloc[0]]
    for i in range(1, len(data_day)):
        if data_day['season'][i] != data_day['season'][i - 1]:
            season_changes.append(data_day['dteday'][i])

    fig = go.Figure()

    # Menambahkan garis tren jumlah penyewa sepeda
    fig.add_trace(go.Scatter(x=data_day['dteday'], y=data_day['cnt'], mode='lines', name='Jumlah Penyewa'))

    # Menambahkan garis vertikal untuk perubahan musim
    for dteday in season_changes:
        season_num = data_day.loc[data_day['dteday'] == dteday, 'season'].iloc[0]
        season_name = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}.get(season_num)
    
    # Garis vertikal
        fig.add_vline(x=dteday, line_width=1, line_dash="dash", line_color="red")
    
    # Menambahkan anotasi dengan teks vertikal dan bergeser ke kanan sedikit
        fig.add_annotation(
            x=dteday, 
            y=max(data_day['cnt']) * 0.9,  
            text=f"{dteday.strftime('%Y-%m-%d')}<br>{season_name}",
            showarrow=False,
            xref='x',
            yref='y',
            align='center',
            font=dict(size=10)
            
        )

    # Pengaturan layout grafik
    fig.update_layout(
        title="Jumlah Penyewa Sepeda Harian tiap Musim",
        xaxis_title="Tanggal",
        yaxis_title="Jumlah Penyewa Sepeda",
        xaxis=dict(
            tickformat='%Y-%m-%d',
            tickangle=-45,
        ),
        showlegend=False,
        height=500,
        width=900
    )

    st.plotly_chart(fig)

    st.write("Dari grafik diatas dapat terlihat bahwa trend penyewaan sepeda mengalami fluktuatif pada tiap musimnya. Terjadi peningkatan trend pada musim semi (spring), trend cenderung stabil pada (panas) summer dan musim gugr (fall), lalu terjadi penurunan trend pada musim dingin (winter).")

# Page 3
if page == "Pengaruh Cuaca dan Musim":
    st.subheader("Bagaimana faktor musiman dan kondisi cuaca mempengaruhi jumlah penyewaan sepeda?")
    st.write("Dengan fluktuatifnya jumlah penyewaan sepeda dari hari ke hari, pastinya terdapat faktor eksternal yang mempengaruhi tinggi rendahnya fluktuatif tersebut.")
    st.write("")

    # Parameter Statistik
    st.write("**Parameter Statistik Data:**")
    st.write(data_day.describe())
    st.write(data_hour.describe())
    st.write("")
    st.write("Dari analisis parameter statistik di atas juga dapat disimpulkan adanya fluktuasi yang signifikan dalam jumlah penyewaan sepeda baik dalam skala hari maupun jam.")
    st.write("Beberapa faktor seperti cuaca (suhu, kelembapan, kecepatan angin) dapat berpengaruh terhadap jumlah penyewa, yang dapat menjadi area untuk analisis lebih lanjut.")

    # Mengelompokkan data berdasarkan musim dan menjumlahkan cnt
    season_daily_total = data_day.groupby('season').agg({'cnt': 'sum'}).reset_index()
    season_hourly_total = data_hour.groupby('season').agg({'cnt': 'sum'}).reset_index()
    weather_daily_total = data_day.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()
    weather_hourly_total = data_hour.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()

    # Pengaruh Musim terhadap Jumlah Penyewaan Sepeda (Daily Data)
    st.write("")
    fig = px.bar(season_daily_total, x='season', y='cnt', color='season', 
                color_discrete_sequence=['#32CD32','#FF6347','#FFD700','#4682B4'],
                labels={'season':'Musim', 'cnt':'Total Jumlah Penyewaan'},
                title="Pengaruh Musim terhadap Jumlah Penyewaan Sepeda (Daily Data)")
    fig.update_layout(xaxis_title="Musim<br>1:Spring, 2:Summer, 3:Fall, 4:Winter", 
                    yaxis_title="Total Jumlah Penyewaan Sepeda",
                    yaxis_tickformat=".0f", 
                    yaxis=dict(gridcolor='lightgray'))  
    st.plotly_chart(fig)

    # Pengaruh Musim terhadap Jumlah Penyewaan Sepeda (Hourly Data)
    st.write("")
    fig = px.bar(season_hourly_total, x='season', y='cnt', color='season', 
                color_discrete_sequence=['#32CD32','#FF6347','#FFD700','#4682B4'],
                labels={'season':'Musim', 'cnt':'Total Jumlah Penyewaan'},
                title="Pengaruh Musim terhadap Jumlah Penyewaan Sepeda (Hourly Data)")
    fig.update_layout(xaxis_title="Musim<br>1:Spring, 2:Summer, 3:Fall, 4:Winter", 
                    yaxis_title="Total Jumlah Penyewaan Sepeda",
                    yaxis_tickformat=".0f", 
                    yaxis=dict(gridcolor='lightgray'))
    st.plotly_chart(fig)

    # Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda (Daily Data)
    st.write("")
    fig = px.bar(weather_daily_total, x='weathersit', y='cnt', color='weathersit',
                labels={'weathersit':'Kondisi Cuaca', 'cnt':'Total Jumlah Penyewaan'},
                title="Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda (Daily Data)")
    fig.update_layout(xaxis_title='Kondisi Cuaca<br>1: Clear, Few clouds, Partly cloudy<br>2: Mist + Cloudy<br>3: Light Snow, Light Rain + Thunderstorm<br>4: Heavy Rain + Thunderstorm + Fog', 
                    yaxis_title="Total Jumlah Penyewaan Sepeda",
                    yaxis_tickformat=".0f", 
                    yaxis=dict(gridcolor='lightgray'))
    st.plotly_chart(fig)

    # Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda (Hourly Data)
    st.write("")
    fig = px.bar(weather_hourly_total, x='weathersit', y='cnt', color='weathersit',
                labels={'weathersit':'Kondisi Cuaca', 'cnt':'Total Jumlah Penyewaan'},
                title="Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda (Hourly Data)")
    fig.update_layout(xaxis_title='Kondisi Cuaca<br>1: Clear, Few clouds, Partly cloudy<br>2: Mist + Cloudy<br>3: Light Snow, Light Rain + Thunderstorm<br>4: Heavy Rain + Thunderstorm + Fog', 
                    yaxis_title="Total Jumlah Penyewaan Sepeda",
                    yaxis_tickformat=".0f", 
                    yaxis=dict(gridcolor='lightgray'))
    st.plotly_chart(fig)

    st.markdown("""
    <div style='text-align: justify;'>
    Berdasarkan barplot diatas, terlihat bahwa:
    <ul>
        <li>Musim gugur (Fall) memiliki jumlah penyewaan sepeda yang cenderung lebih tinggi dibandingkan musim lainnya.</li>
        <li>Hal yang sama juga terjadi pada nilai Korelasi Pearson dan Korelasi Spearman antara penyewa sepeda (cnt) dengan variabel apparent temperature (atemp). Hubungan antara kedua variabel cenderung positif kuat secara monoton naik.</li>
        Hal ini menunjukkan bahwa musim dan cuaca memiliki pengaruh yang signifikan terhadap jumlah penyewaan sepeda.<br><br>
        Untuk mendukung pernyataan diatas, akan dilakukan perhitungan korelasi antara variabel penyewa sepeda (cnt) dengan variabel bebas lainnya (temp, atemp, hum, windspeed) pada data day.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

if page == "Korelasi Antar Variabel":
    st.subheader('**Korelasi Antara Variabel Penyewa Sepeda (cnt) dengan Variabel Bebas Lainnya (temp, atemp, hum, windspeed).**')
    st.write('Menggunakan Metode Korelasi Pearson dan Spearman')
    st.write('')
    correlation_pearson = data_day[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr(method='pearson')
    correlation_spearman = data_day[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr(method='spearman')

    st.write("Metode Korelasi Pearson")
    st.write(correlation_pearson)

    st.write("Metode Korelasi Spearman")
    st.write(correlation_spearman)
    st.write('')
    st.write('catatan:')
    st.write('- Nilai Korelasi berada pada interval:')
    st.latex(r'-1 \leq x \leq 1')
    st.write('- Nilai Korelasi yang lebih dari nol menandakan adanya Korelasi Positif antar Variabel.')
    st.write('- Nilai Korelasi yang kurang dari nol menandakan adanya Korelasi Negatif antar Variabel.')
    st.write('- Nilai Korelasi yang semakin mendekati batas interval (1 atau -1) menandakan semakin kuat korelasi antar Variabel.')
    st.write('- Nilai Korelasi nol (0) menandakan tidak adanya Korelasi antar Variabel.')
    st.write('')

    st.write("Scatter Plot dengan Linear Regression")

    for col in ['temp', 'atemp', 'hum', 'windspeed']:
        st.write(f"Scatter plot `cnt` dan `{col}`:")
        
        fig = px.scatter(data_day, x=col, y='cnt', trendline="ols", 
                        labels={'cnt': 'Jumlah Penyewaan Sepeda (cnt)', col: col}, 
                        title=f'{col} vs cnt')
        
        fig.update_traces(line=dict(color="red"))
        
        st.plotly_chart(fig)
    
    st.markdown("""
    <div style='text-align: justify;'>
    Berdasarkan Scatterplot di atas, terlihat bahwa:
    <ul>
        <li>Nilai Korelasi Pearson dan Korelasi Spearman antara penyewa sepeda (cnt) dengan variabel suhu (temp) menunjukkan nilai yang mendekati 1 yaitu 0.63 dan 0.62. Hal ini menunjukkan adanya hubungan positif yang kuat secara monoton naik antara suhu (temp) dan jumlah penyewa sepeda (cnt).</li>
        <li>Hal yang sama juga terjadi pada nilai Korelasi Pearson dan Korelasi Spearman antara penyewa sepeda (cnt) dengan variabel apparent temperature (atemp). Hubungan antara kedua variabel cenderung positif kuat secara monoton naik.</li>
        <li>Sebaliknya, nilai Korelasi Pearson dan Korelasi Spearman antara penyewa sepeda (cnt) dengan variabel kelembapan (hum) menunjukkan nilai yang mendekati di bawah nol/negatif yaitu -0.10 dan -0.10. Hal ini menunjukkan adanya hubungan negatif yang lemah secara monoton turun antara kelembapan (hum) dan jumlah penyewa sepeda (cnt).</li>
        <li>Nilai Korelasi Pearson dan Korelasi Spearman antara penyewa sepeda (cnt) dengan variabel kecepatan angin (windspeed) juga menunjukkan nilai yang mendekati di bawah nol/negatif yaitu -0.23 dan -0.22. Hal ini menunjukkan adanya hubungan negatif yang lemah secara monoton turun antara kecepatan angin (windspeed) dan jumlah penyewa sepeda (cnt).</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Page 4
if page == "Kesimpulan":
    st.markdown("""
    <div style='text-align: justify;'>
    Trend penyewaan sepeda di Washington D.C., USA pada tahun 2011 hingga 2012 dapat dikategorikan sebagai pola data trend musiman.<br><br>
    Terdapat fluktuasi jumlah penyewa sepeda baik dari segi penyewaan hari dan jam. Fluktuasi tersebut dipengaruhi oleh faktor musim dan cuaca. Terlihat bahwa jumlah penyewa sepeda pada musim gugur (fall) cenderung lebih tinggi dibandingkan musim lainnya dan ketika cuaca cerah (kondisi 1) memiliki jumlah penyewaan sepeda yang paling tinggi, sedangkan cuaca buruk (kondisi 3 dan 4) memiliki jumlah penyewaan sepeda yang paling rendah.<br><br>
    Pengukuran nilai Korelasi Pearson dan Korelasi Spearman juga menunjukkan adanya hubungan antara faktor musim dan cuaca terhadap jumlah penyewa sepeda dengan melihat variabel-variabel bebas yang mempengaruhi musim dan cuaca (temp, atemp, hum, dan windspeed). Jumlah penyewa sepeda cenderung monoton naik ketika nilai variabel suhu (temp) dan apparent temperature (atemp) naik, sebaliknya jumlah penyewa akan turun ketika variabel kelembapan (hum) dan kecepatan angin (windspeed) turun.
    </div>
    """, unsafe_allow_html=True)