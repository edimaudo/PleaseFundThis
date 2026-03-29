####################
## ROI of Communication
####################
df['project_update_count'] = pd.to_numeric(df['project_update_count'], errors='coerce')
df['percent_raised'] = pd.to_numeric(df['percent_raised'], errors='coerce')

df_filtered = df[df['percent_raised'] <= 1000].copy()

success_df = df_filtered[df_filtered['project_success'] == True]
failed_df = df_filtered[df_filtered['project_success'] == False]

fig_roi = go.Figure()

fig_roi.add_trace(go.Scatter(
    x=success_df['project_update_count'],
    y=success_df['percent_raised'],
    mode='markers',
    name='Successful Projects',
    marker=dict(color='#00CC96', opacity=0.5),
    hovertemplate="Updates: %{x}<br>Raised: %{y}%<extra></extra>"
))

# Add Unsuccessful Projects (Dots + Trendline)
fig_roi.add_trace(go.Scatter(
    x=failed_df['project_update_count'],
    y=failed_df['percent_raised'],
    mode='markers',
    name='Unsuccessful Projects',
    marker=dict(color='#EF553B', opacity=0.5),
    hovertemplate="Updates: %{x}<br>Raised: %{y}%<extra></extra>"
))

fig_roi.update_layout(
    title={'text': 'The ROI of Communication: Updates vs. Funding Percentage', 'x': 0.5},
    xaxis_title="Number of Project Updates",
    yaxis_title="Percent of Goal Raised (%)",
    template='plotly_white',
    legend_title="Project Result",
    height=600
)

fig_roi.show()