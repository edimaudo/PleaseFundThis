####################
## Funding lift looking at social media (fb pages) and funding videos
####################
# Clean Currency
df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

df_view = df[df['amt_pledged_$'] <= 10000].copy()
df_view['video_label'] = df_view['project_has_video'].apply(lambda x: 'With Video' if x is True else 'No Video')
success_df = df_view[df_view['project_success'] == True]
failed_df = df_view[df_view['project_success'] == False]

fig_video = go.Figure()

fig_video.add_trace(go.Box(
    x=success_df['video_label'],
    y=success_df['amt_pledged_$'],
    name='Successful',
    marker_color='#00CC96',
    boxpoints=None
))

fig_video.add_trace(go.Box(
    x=failed_df['video_label'],
    y=failed_df['amt_pledged_$'],
    name='Unsuccessful',
    marker_color='#EF553B',
    boxpoints=None
))

fig_video.update_layout(
    title={'text': 'Funding Lift: Impact of Video Assets', 'x': 0.5},
    yaxis_title="Total Amount Pledged ($)",
    xaxis_title="Video Presence",
    boxmode='group',
    template='plotly_white'
)

fig_video.show()