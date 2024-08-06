import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

df = pd.read_csv('data/expanded_watch_history_2024_08_03.csv')

df['watch_date'] = pd.to_datetime(df['watch_date'], format='ISO8601')

df['day'] = df['watch_date'].dt.day
# df['week'] = df['watch_date'].dt.isocalendar().week
df['week'] = pd.to_datetime(df['watch_date']).dt.strftime('%W').astype(int)
df['month'] = df['watch_date'].dt.month
df['year'] = df['watch_date'].dt.year
df['hour'] = df['watch_date'].dt.hour
df['day_of_week'] = df['watch_date'].dt.day_of_week

df['category'] = df['category'].str.replace('\\u0026', 'and')
# df['watch_date'] = pd.to_datetime(df['watch_date'], format="mixed")
# df['watch_date'] = df['watch_date'].dt.date

st.markdown('''
# YTP: YouTube Watchtime Visualizer
## Visualize your Google Takeout data with *AI*
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
fig.update_traces(customdata=df[['video_title', 'channel_name', 'video_url']])
fig.update_traces(hovertemplate='Video Title: %{customdata[0]}<br>Channel Name: %{customdata[1]}<br>Length (seconds): %{x}')

# click_js = """
# <script>
#     document.addEventListener('DOMContentLoaded', function() {
#         var plot = document.querySelectorAll('div.js-plotly-plot')[0];
#         plot.on('plotly_click', function(data) {
#             var point = data.points[0];
#             var video_url = point.customdata[2];
#             window.open(video_url, '_blank');
#         });
#     });
# </script>
# """

st.plotly_chart(fig)

tab_titles = [str(x) for x in sorted(df['year'].unique().tolist())]
tabs = st.tabs(tab_titles)

for i, tab in enumerate(tabs):
    with tab:
        a_df = df[df['year'] == int(tab_titles[i])]
        
        num_weeks = 52
        num_days = 7

        base_date = a_df['watch_date'].min()
        dates = [base_date + datetime.timedelta(days=i) for i in range(num_weeks * num_days)]
        b_df = a_df.groupby(['day_of_week', 'week']).size().to_frame('contributions').reset_index()

        pivot_df = b_df.pivot(index='day_of_week', columns='week', values='contributions')
        pivot_df = pivot_df.fillna(0)

        fig = px.imshow(pivot_df,
                        labels=dict(x="Week", y="Day", color="Contributions"),
                        x=pivot_df.columns,
                        y=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                        color_continuous_scale='Greens')

        fig.update_layout(
            title=f'GitHub-style Watch History Heatmap ({tab_titles[i]})',
            xaxis_nticks=53,
            yaxis_nticks=7,
            height=300,
            width=1000
        )

        st.plotly_chart(fig)