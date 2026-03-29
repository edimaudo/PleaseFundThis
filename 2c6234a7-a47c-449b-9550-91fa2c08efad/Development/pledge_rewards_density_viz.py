####################
# Density pledge rewards (low)
####################
# Clean Currency
df['lowest_pledge_reward_$'] = pd.to_numeric(df['lowest_pledge_reward_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
# We filter to $200 for a readable linear scale
df_low = df[df['lowest_pledge_reward_$'] <= 10000]
success_df = df_low[df_low['project_success'] == True]
failed_df = df_low[df_low['project_success'] == False]

fig_low = go.Figure()

fig_low.add_trace(go.Violin(
    y=success_df['lowest_pledge_reward_$'],
    name='Successful Projects',
    line_color='#00CC96',
    box_visible=True,
    meanline_visible=True
))

fig_low.add_trace(go.Violin(
    y=failed_df['lowest_pledge_reward_$'],
    name='Unsuccessful Projects',
    line_color='#EF553B',
    box_visible=True,
    meanline_visible=True
))

fig_low.update_layout(
    title={'text': 'Entry Level Pledge Rewards Density', 'x': 0.5},
    yaxis_title="Pledge Amount ($)",
    template='plotly_white'
)

fig_low.show()
