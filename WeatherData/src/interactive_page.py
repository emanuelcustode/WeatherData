import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px



st.sidebar.title("Options")

jahr_start, jahr_end = st.sidebar.slider("Zeitraum", 1935, 2025, (2000,2025))
schwelle = st.sidebar.slider("Temperaturschwelle (°C)", 25, 40, 30)


data_frame_old = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_19350701_20241231_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])
data_frame_new = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_20231229_20250630_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])

data_frame_new.columns = data_frame_new.columns.str.strip()
data_frame_old.columns = data_frame_old.columns.str.strip()

df_combined = pd.concat([data_frame_old, data_frame_new], ignore_index=True)

df_combined["year"] = df_combined["MESS_DATUM"].dt.year

df_filtered = df_combined[(df_combined["year"] >= jahr_start) & (df_combined["year"] <= jahr_end)]
df_events = df_filtered[df_filtered["TXK"] >= schwelle]

events_per_year = df_events.groupby("year").size()
events_per_year = events_per_year.reindex(range(jahr_start, jahr_end + 1), fill_value=0)
events_per_year.index = events_per_year.index.astype(int)

df_plot = events_per_year.reset_index()
df_plot.columns = ["year", "Anzahl"]

fig = px.bar(
    df_plot,
    x="year",
    y="Anzahl",
    text="Anzahl",
    labels={"year": "Year", "events": "Anzahl"},
    title=f"Tage mir °C ≥ {schwelle} ({jahr_start} - {jahr_end})",
)

fig.update_traces(marker_color="lightblue",  hovertemplate="Jahr: %{x}<br>Tage: %{y}")
fig.update_layout(xaxis_tickformat="d", xaxis=dict(dtick=5), showlegend=False)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
### 🌡️ Interaktive Klima-Analyse

Auf dieser Seite kannst du selbst analysieren, wie sich extreme Hitzetage im Laufe der Zeit verändert haben.  
Nutze die Optionen in der Seitenleiste, um:

- den **Zeitraum** einzugrenzen (z. B. nur die letzten 10 Jahre),
- die **Temperaturschwelle** individuell anzupassen (z. B. ab 30 °C, 35 °C oder extremer),
- und zu entdecken, in welchen Jahren besonders viele heiße Tage aufgetreten sind.

Die Werte werden automatisch aktualisiert und als interaktives Balkendiagramm dargestellt.  
Wenn du mit der Maus über einen Balken fährst, siehst du die genaue Anzahl an Tagen für dieses Jahr.

Diese Ansicht ermöglicht es, Temperaturveränderungen und Extremereignisse **direkt erfahrbar zu machen**.
""")

