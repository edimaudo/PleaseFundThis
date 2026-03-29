####################
## Comparison between goal $ and amount pledged
####################

# Clean currency columns
for col in ['goal_$', 'amt_pledged_$']:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# We use MEDIAN to find the 'typical' experience for each category
df_cat = df.groupby('major_category').agg({
    'goal_$': 'median',
    'amt_pledged_$': 'median'
}).reset_index()

# Sort by Pledged amount for a cleaner "ladder" visual
df_cat = df_cat.sort_values('amt_pledged_$')

fig_cat_dumbbell = go.Figure()

for i, row in df_cat.iterrows():
    fig_cat_dumbbell.add_trace(go.Scatter(
        x=[row['goal_$'], row['amt_pledged_$']],
        y=[row['major_category'], row['major_category']],
        mode='lines',
        line=dict(color='lightgrey', width=4),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add the "Median Goal" dots (Red)
fig_cat_dumbbell.add_trace(go.Scatter(
    x=df_cat['goal_$'],
    y=df_cat['major_category'],
    mode='markers',
    name='Median Goal',
    marker=dict(color='#EF553B', size=14),
    hovertemplate="Typical Goal: $%{x:,.0f}<extra></extra>"
))

# Add the "Median Pledged" dots (Green)
fig_cat_dumbbell.add_trace(go.Scatter(
    x=df_cat['amt_pledged_$'],
    y=df_cat['major_category'],
    mode='markers',
    name='Median Pledged',
    marker=dict(color='#00CC96', size=14),
    hovertemplate="Typical Pledged: $%{x:,.0f}<extra></extra>"
))

fig_cat_dumbbell.update_layout(
    title='"Funding Gap" by Category',
    xaxis_title='Amount ($)', # - Log Scale'
    yaxis_title=None,
    title_x=0.5,
    template='plotly_white',
      title_font_size=20,
    xaxis_type='log',
    height=700,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Set the log-scale ticks
fig_cat_dumbbell.update_xaxes(
    tickvals=[100, 1000, 10000, 100000],
    ticktext=['$100', '$1k', '$10k', '$100k']
)

fig_cat_dumbbell.show()