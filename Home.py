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

remove_suspected_livestreams = st.checkbox('Remove suspected livestreams?')

if remove_suspected_livestreams:
    Q1 = df['length_seconds'].quantile(0.25)
    Q3 = df['length_seconds'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['length_seconds'] >= lower_bound) & (df['length_seconds'] <= upper_bound)]

st.markdown(f'''
#### You've watched **{df.shape[0]:,} videos** from **{df['watch_date'].dt.date.min()}** to **{df['watch_date'].dt.date.max()}**.
''')

cols = st.columns(2)

with cols[0]:
    st.markdown(f'''
    ##### Most popular channels by video count:
    ''')
    st.dataframe(df['channel_name'].value_counts().reset_index()[:10][['channel_name', 'count']])

with cols[1]:
    st.markdown(f'''
    ##### Most popular channels by video length:
    ''')
    st.dataframe(df.groupby(['channel_name'])['length_seconds'].sum().reset_index().sort_values(by='length_seconds', ascending=False).reset_index(drop=True)[:10])

fig = px.box(df, x='length_seconds', title=f'Video Length Boxplot')
st.plotly_chart(fig)

fig = go.Figure(data=go.Heatmap(z=z, colorscale='Viridis'))
st.plotly_chart(fig)