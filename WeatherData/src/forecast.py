import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


data_frame_old = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_19350701_20241231_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])
data_frame_new = pd.read_csv('WeatherData/dataset/frankfurt/produkt_klima_tag_20231229_20250630_01420.txt',
                             sep=";", na_values=-999, parse_dates=['MESS_DATUM'])

data_frame_new.columns = data_frame_new.columns.str.strip()
data_frame_old.columns = data_frame_old.columns.str.strip()

df_combined = pd.concat([data_frame_old, data_frame_new], ignore_index=True)
df_combined = df_combined.drop_duplicates(subset=['MESS_DATUM'])

df_combined["jahr"] = df_combined["MESS_DATUM"].dt.year



df_recent = df_combined[(df_combined['jahr'] >= 2015) & (df_combined['jahr'] <= 2025) ]

df_hot = df_recent[df_recent['TXK']>=30]

hot_per_year = df_hot.groupby('jahr').size().reindex(range(2015, 2026), fill_value=0)

current_year = pd.Timestamp.now().year
partial = current_year == 2025


fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.bar(hot_per_year.index, hot_per_year.values, color=['tab:blue'] * len(hot_per_year))

if partial and 2025 in hot_per_year.index:
    bars[-1].set_color('orange')
    ax.text(2025, hot_per_year[2025]+1, "bis heute", ha='center')

avg =  hot_per_year.loc[2015:2024].mean()
ax.axhline(avg, color='red', linestyle='--', linewidth=1, label=f"Ø 2015–2024: {avg:.1f}")


ax.set_title("Anzahl Hitzetage pro Jahr (2015–2025)")
ax.set_ylabel("Hitzetage (TXK ≥ 30 °C)")
ax.set_xlabel("Jahr")
ax.set_xticks(range(2015, 2026))
ax.set_ylim(0, max(hot_per_year.max() + 5, 10))
ax.legend()

st.pyplot(fig)

st.markdown(
    "In dieser Abbildung werden die Hitzetage der letzten 10 Jahre mit dem bisherigen Stand für 2025 (orange) verglichen. Die gestrichelte Linie zeigt"
    "den Durchschnittswert der Jahre 2015–2024 (ca. 23,9 Tage). "
    "Schon jetzt liegt 2025 leicht darunter, zu beachten allerdings ist das Jahr noch nicht abgeschlossen."
)

df_this_year = df_combined[df_combined['jahr']==2025]

today = pd.Timestamp.now()
df_today = df_this_year[df_this_year['MESS_DATUM']<=today]
count_actual_hot_days = df_today[df_today['TXK']>=30].shape[0]

days_in_year = 366 if today.is_leap_year else 365
days_gone = today.dayofyear
year = days_gone / days_in_year

forecast_for_this_year = round(count_actual_hot_days / year) if year > 0 else 0



hot_per_year = df_combined[
    (df_combined["jahr"] >= 2015) & (df_combined["jahr"] <= 2024) & (df_combined["TXK"] >= 30)
].groupby("jahr").size()

hot_per_year.loc[2025] = forecast_for_this_year

fig2, ax2 = plt.subplots(figsize=(12, 8))
bars2 = ax2.bar(hot_per_year.index, hot_per_year.values, color=['tab:blue'] * len(hot_per_year))
bars2[-1].set_color('orange')
ax2.set_title("Forecast")
ax2.set_xlabel("Jahr")
ax2.set_ylabel("Forecast")
st.pyplot(fig2)


st.markdown(
    """Diese Grafik zeigt eine Hochrechnung der Hitzetage für das laufende Jahr 2025. 
    Auf Basis der bisherigen Entwicklung (bis Anfang Juli) werden rund 18 Hitzetage prognostiziert. 
    Das liegt aktuell unter dem Durchschnitt, könnte sich aber im weiteren Jahresverlauf noch deutlich ändern."""
)





