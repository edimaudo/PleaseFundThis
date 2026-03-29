####################
## Social media impact facebook friends count
####################
df['facebook_friends_count'] = pd.to_numeric(df['facebook_friends_count'], errors='coerce')

df_view = df[df['facebook_friends_count'] <= 10000].copy()

success_df = df_view[df_view['project_success'] == True]
failed_df = df_view[df_view['project_success'] == False]

fig_strip = go.Figure()

# Successful Projects
fig_strip.add_trace(go.Box(
    y=success_df['facebook_friends_count'],
    name='Reached Goal',
    marker=dict(color='#00CC96', size=5, opacity=0.4),
    boxpoints='all', jitter=0.5, pointpos=0,
    fillcolor='rgba(0,0,0,0)', line_color='rgba(0,0,0,0)',
    hovertext="Successful Project"
))

# Unsuccessful Projects
fig_strip.add_trace(go.Box(
    y=failed_df['facebook_friends_count'],
    name='Did Not Reach Goal',
    marker=dict(color='#EF553B', size=5, opacity=0.4),
    boxpoints='all', jitter=0.5, pointpos=0,
    fillcolor='rgba(0,0,0,0)', line_color='rgba(0,0,0,0)',
    hovertext="Unsuccessful Project"
))

fig_strip.update_layout(
    title={
        'text': "<b>Crowdsourcing Power:</b> How Personal Networks Impact Success",
        'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
    },
    yaxis_title="Total Facebook Friends",
    xaxis_title="Final Project Status",
    template='plotly_white',
    height=600,
    showlegend=False,
)

fig_strip.show()
