import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_trend_bike_hourly_df(df):
    trend_bike_hourly = df.groupby(by=["hr","weekday"]).agg({
        "cnt": "sum"
    }).reset_index()
    
    return trend_bike_hourly

def create_season_trend_hourly_df(df):
    season_trend_hourly = df.groupby(by=["hr","season"]).agg({
        "cnt": "sum"
    }).reset_index()
    
    return season_trend_hourly

def create_trend_bike_daily_df(df):
    df['mnth'] = pd.Categorical(df['mnth'], categories=
        ['January','February','March','April','May','June','July','August','September','October','November','December'],
        ordered=True)

    trend_bike_daily = df.groupby(by=["mnth","yr"]).agg({
        "cnt": "sum"
    }).reset_index()
    
    return trend_bike_daily

def create_weekday_trend_df(df):
    df['weekday'] = pd.Categorical(df['weekday'], categories=
        ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        ordered=True)

    weekday_trend = df.groupby('weekday')[['registered', 'casual']].sum().reset_index()
    
    return weekday_trend

day_df = pd.read_csv("day_cleaned.csv")
hour_df = pd.read_csv("hour_cleaned.csv")

trend_bike_hourly = create_trend_bike_hourly_df(hour_df)
season_trend_hourly = create_season_trend_hourly_df(hour_df)
trend_bike_daily = create_trend_bike_daily_df(day_df)
weekday_trend = create_weekday_trend_df(day_df)

st.write('# Proyek Analisis Data :sparkles:')

st.markdown(
    """
    Nama    : Muhammad Dinan Islamanda\n
    Email   : dinanislamanda@gmail.com\n
    Username: dinan_islamanda\n
    Dataset : Bike Sharing Dataset
    """
)

tab1, tab2, tab3, tab4 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3", "Pertanyaan 4"])

with tab1:
    st.write(
    """
    Bagaimana pola tren penyewaan sepeda harian (Perjam)?
    """
    )
    
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=trend_bike_hourly,
        x="hr",
        y="cnt",
        hue="weekday",
        hue_order=weekday_order,
        palette="viridis",
        marker="o"
    )

    ax.set_title("Pola Sewa Sepeda Harian (Perjam)")
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.set_xlabel('Jam')
    ax.set_xticks(range(0, 24, 1))
    ax.legend()
    st.pyplot(fig)

    st.markdown(
    """
     Pada grafik terlihat bahwa terdapat 2 pola yang berbeda yaitu untuk Workingday dan Holiday. 
     Pada Workingday (Senin s.d. Jumat) terjadi peningkatan jumlah penyewaan sepeda pada jam 8.00 
     dan juga jam 17.00-18.00. Sedangkan pada Holiday (Sabtu dan Minggu) puncak jumlah penyewaan sepeda terjadi pada 
     jam 12.00-16.00.
     """
    )

with tab2:
    st.write(
    """
    Bagaimana pola tren penyewaan sepeda tiap musim (Perjam)?
    """
    )
    
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=season_trend_hourly,
        x="hr",
        y="cnt",
        hue="season",
        palette="rocket",
        marker="o"
    )

    ax.set_title("Pola Sewa Sepeda Tiap Musim (Perjam)")
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.set_xlabel('Jam')
    ax.set_xticks(range(0, 24, 1))
    ax.legend()
    st.pyplot(fig)

    st.markdown(
    """
    Pola tren penyewaan sepeda untuk tiap musim relatif mirip yaitu terjadi puncak jumlah 
    penyewaan sepeda pada jam 8.00 dan jam 17.00-18.00. Dimana musim Springer menjadi musim 
    dengan jumlah pengguna sepeda paling sedikit dan musim Fall menjadi musim dengan jumlah 
    pengguna sepeda paling banyak.
    """
    )

with tab3:
    st.write(
    """
    Bagaimana tren penyewaan sepeda tiap tahunnya?
    """
    )
    
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.lineplot(
        data=trend_bike_daily,
        x="mnth",
        y="cnt",
        hue="yr",
        palette="viridis",
        marker="o"
    )

    ax.set_title("Tren Sewa Sepeda", loc="center")
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.set_xlabel('Bulan')
    ax.legend(title="Tahun")
    st.pyplot(fig)

    st.markdown(
    """
    Tren sewa sepeda meningkat ditahun 2012 jika dibandingkan dengan tahun 2011. Terjadi 
    penurunan pada pertengahan tahun 2011 hingga akhir tahun. Kemudian meningkat drastis di tahun 2012.
    """
    )

with tab4:
    st.write(
    """
    Bagaimana perbandingan penyewaan sepeda harian?
    """
    )
    
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        weekday_trend['weekday'],
        weekday_trend['registered'],
        label='Registered',
        color='#97BC62FF'
    )

    ax.bar(
        weekday_trend['weekday'],
        weekday_trend['casual'],
        label='Casual',
        color='#2C5F2D'
    )

    ax.set_title('Perbandingan Penyewa Sepeda Setiap Hari')
    ax.set_ylabel('Jumlah Pengguna Sepeda')
    ax.set_xlabel("Hari")
    ax.legend()
    st.pyplot(fig)

    st.markdown(
    """
    Terjadi penurunan penyewaan sepeda oleh pengguna pada hari Sabtu dan Minggu. 
    Jumlah penyewaan sepeda meningkat lagi pada hari Senin hingga Jumat. Pengguna 
    lebih jarang menyewa sepeda pada weekend dibandingkan weekday (Senin s.d. Jumat).
    """
    )