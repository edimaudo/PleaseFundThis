####################
# Density pledge rewards (high)
####################
df['highest_pledge_reward_$'] = pd.to_numeric(df['highest_pledge_reward_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
# Separate by Project Result (Your provided logic)
df_high = df[df['highest_pledge_reward_$'] <= 10000]
success_df_h = df_high[df_high['project_success'] == True]
failed_df_h = df_high[df_high['project_success'] == False]

fig_high = go.Figure()

fig_high.add_trace(go.Violin(
    y=success_df_h['highest_pledge_reward_$'],
    name='Successful Projects',
    line_color='#00CC96',
    box_visible=True,
    meanline_visible=True
))

fig_high.add_trace(go.Violin(
    y=failed_df_h['highest_pledge_reward_$'],
    name='Unsuccessful Projects',
    line_color='#EF553B',
    box_visible=True,
    meanline_visible=True
))

fig_high.update_layout(
    title={'text': 'High-Tier Pledge Rewards Density', 'x': 0.5},
    yaxis_title="Pledge Amount ($)",
    template='plotly_white'
)

fig_high.show()