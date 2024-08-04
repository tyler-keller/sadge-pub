import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('data/expanded_watch_history_2024_08_03.csv')

df['watch_date'] = pd.to_datetime(df['watch_date'], format='ISO8601')

df['day'] = df['watch_date'].dt.day
df['month'] = df['watch_date'].dt.month
df['hour'] = df['watch_date'].dt.hour
df['day_of_week'] = df['watch_date'].dt.day_of_week

df['category'] = df['category'].str.replace('\\u0026', 'and')
# df['watch_date'] = pd.to_datetime(df['watch_date'], format="mixed")
# df['watch_date'] = df['watch_date'].dt.date

st.markdown('''
# YTP: YouTube Watchtime Visualizer
## Visualize your Google Takeout data using *AI*
''')

st.dataframe(df)

st.markdown(f'''
You've watched {df.shape[0]} videos from {df['watch_date'].dt.date.min()} to {df['watch_date'].dt.date.max()}.
''')

st.markdown(f'''
You're most popular channels by total videos are:
''')
st.dataframe(df['channel_name'].value_counts().reset_index()[:10][['channel_name', 'count']])

st.markdown(f'''
You're most popular channels by total videos are:
''')
st.dataframe(df.groupby(['channel_name'])['length_seconds'].sum().reset_index().sort_values(by='length_seconds', ascending=False))
# fig = px.pie(df)
# st.plotly_chart(fig)