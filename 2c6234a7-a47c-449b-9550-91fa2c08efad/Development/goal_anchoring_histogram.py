####################
## Goal $ Histogram 
####################
df_filtered = df[(df['goal_$'] > 0) & (df['goal_$'] <= 100000)].copy()

fig_anchors = px.histogram(
    df_filtered, 
    x="goal_$", 
    nbins=500, # High bin count is CRITICAL to see the narrow spikes
    title='Funding Goal Target Amount Distribution',
    labels={'goal_$': 'Funding Goal ($)'},
    template='plotly_white',
    color_discrete_sequence=['#636EFA']
)


fig_anchors.update_layout(
    title_x=0.5,
    xaxis_title="Funding Goal Amount ($)",
    yaxis_title="Frequency (Number of Projects)",
    bargap=0.1,
    xaxis=dict(
        tickvals=[0, 1000, 5000, 10000, 20000, 25000, 50000, 75000, 100000],
        tickformat='$,.0f',
        range=[0, 100000]
    )
)


fig_anchors.add_annotation(x=10000, yref='paper', y=0.9, text="The $10k Peak", showarrow=True, arrowhead=1)
fig_anchors.add_annotation(x=5000, yref='paper', y=0.7, text="$5k Peak", showarrow=True, arrowhead=1)

fig_anchors.show()