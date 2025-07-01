import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import streamlit as st


data_frame_old = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_19350701_20241231_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])
data_frame_new = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_20231229_20250630_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])

data_frame_new.columns.str.strip()
data_frame_old.columns.str.strip()

df_combined = pd.concat([data_frame_old, data_frame_new], ignore_index=True)


df_combined = df_combined.drop_duplicates(subset=['MESS_DATUM'])

df_higher_than_thirty = df_combined[df_combined[' TXK'] > 30]

df_higher_than_thirty['jahr'] = df_combined['MESS_DATUM'].dt.year

hot_days = df_higher_than_thirty.groupby(['jahr']).size().reset_index(name='count_hot_days')

fig, ax = plt.subplots(figsize=(12, 8))
ax.plot(hot_days['jahr'], hot_days['count_hot_days'], marker='o')
ax.set_xlabel('Jahr')
ax.set_ylabel('Count Hot Days')
ax.set_title("Hot Days per year")
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.grid(True)
st.pyplot(fig)

st.markdown(
    "Diese Grafik zeigt die Anzahl der Hitzetage (Tagesmaximum ≥ 30°C) in Frankfurt pro Jahr seit 1935. "
    "Besonders ab den 1990er Jahren ist eine deutliche Zunahme "
    "der heißen Tage erkennbar mit extremen Spitzen in den letzten Jahren."
)

m, b = np.polyfit(hot_days['jahr'], hot_days['count_hot_days'], deg=1)
trend = m *  hot_days["jahr"] + b

fig2, ax2 = plt.subplots(figsize=(12, 8))
ax2.plot(hot_days['jahr'], hot_days['count_hot_days'], marker='o')
ax2.plot(hot_days["jahr"], trend, color="red", linestyle="-", label=f"Trendlinie (+{m:.2f} Tage/Jahr)")
ax2.set_xlabel('Jahr')
ax2.set_ylabel('Count Hot Days')
ax2.set_title("Hot Days per year with regression")
ax2.xaxis.set_major_locator(MultipleLocator(5))
ax2.yaxis.set_major_locator(MultipleLocator(5))
ax2.grid(True)
st.pyplot(fig2)

st.markdown(
    "Hier wird die Entwicklung der Hitzetage durch eine lineare Trendlinie ergänzt. Die stetig steigende Tendenz bestätigt, "
    "dass heiße Tage über die Jahrzehnte häufiger auftreten, das ist ein klarer Hinweis auf die Auswirkungen des Klimawandels in der Region."
)




