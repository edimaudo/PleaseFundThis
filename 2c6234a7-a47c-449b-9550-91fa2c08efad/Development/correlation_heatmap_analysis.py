##=====================
# Success Drivers and Indicators
##=====================

####################
## Correlation heatmap
####################
currency_cols = ['lowest_pledge_reward_$', 'highest_pledge_reward_$', 'amt_pledged_$', 'goal_$']
for col in currency_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# Convert Success and Video to 0 and 1
df['project_success'] = df['project_success'].astype(int)
df['project_has_video'] = df['project_has_video'].astype(int)

# Select Numeric Metrics for the Heatmap
metrics = [
    'amt_pledged_$', 'percent_raised', 'project_success',
    'project_update_count', 'number_of_pledgers', 'comments_count',
    'facebook_friends_count', 'lowest_pledge_reward_$', 'highest_pledge_reward_$',
    'duration_days', 'project_has_video'
]

# Create the Correlation Matrix
corr_matrix = df[metrics].corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=".2f", # Shows the correlation number in the box
    aspect="auto",
    color_continuous_scale='RdBu_r', # Red for negative, Blue for positive
    zmin=-1, zmax=1,                 # Standard correlation range
    title='What Drives Funding? (Correlation Heatmap)',
    labels={'color': 'Correlation Strength'},
    template='plotly_white'
)

fig_heatmap.update_layout(
    title={'text': 'The Drivers of Success: Correlation Heatmap', 'x': 0.5},
    height=800,
    xaxis_tickangle=-45
)

fig_heatmap.show()