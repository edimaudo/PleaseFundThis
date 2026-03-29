####################
## analyze top 20 projects to compare overfunding
####################

# Calculate the 'overfunding' amount and select Top 20 for readability
df['overfunding_gap'] = df['amt_pledged_$'] - df['goal_$']
top_20 = df.sort_values(by='overfunding_gap', ascending=False).head(20).copy()

# 2. Build the Figure
fig_dumbbell = go.Figure()

# Loop through each project to draw the "bar" part of the dumbbell
for i, row in top_20.iterrows():
    fig_dumbbell.add_shape(
        type='line',
        x0=row['goal_$'], y0=row['project_name'],
        x1=row['amt_pledged_$'], y1=row['project_name'],
        line=dict(color='lightgrey', width=3)
    )

# 3. Add the "Goal" dots (Red)
fig_dumbbell.add_trace(go.Scatter(
    x=top_20['goal_$'],
    y=top_20['project_name'],
    mode='markers',
    name='Goal',
    marker=dict(color='#EF553B', size=12, symbol='circle'),
    hovertemplate="<b>%{y}</b><br>Goal: $%{x:,.0f}<extra></extra>"
))

# 4. Add the "Pledged" dots (Green)
fig_dumbbell.add_trace(go.Scatter(
    x=top_20['amt_pledged_$'],
    y=top_20['project_name'],
    mode='markers',
    name='Pledged Amount',
    marker=dict(color='#00CC96', size=12, symbol='circle'),
    hovertemplate="<b>%{y}</b><br>Pledged: $%{x:,.0f}<extra></extra>"
))


fig_dumbbell.update_layout(
    title='Magnitude of Overfunding: Top 20 Most Successful Projects',
    title_x=0.5,
    xaxis_title='Funding Amount ($)', ## log scale
    yaxis_title=None,
    template='plotly_white',
    xaxis_type='log', # Log scale allows us to see different orders of magnitude
    height=800,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Optional: Add clear log-scale ticks
fig_dumbbell.update_xaxes(
    tickvals=[10, 100, 1000, 10000, 100000, 1000000],
    ticktext=['$10', '$100', '$1k', '$10k', '$100k', '$1M']
)

fig_dumbbell.show()