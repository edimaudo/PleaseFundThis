##=====================
# Success Drivers and Indicators
##=====================

####################
## Correlation heatmap
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
currency_cols = ['lowest_pledge_reward_$', 'highest_pledge_reward_$', 'amt_pledged_$', 'goal_$']
for col in currency_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# Convert Success and Video to 0 and 1
df['project_success'] = df['project_success'].astype(int)
df['project_has_video'] = df['project_has_video'].astype(int)

# 3. Select Numeric Metrics for the Heatmap
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


####################
## ROI of Communication
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
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

####################
## Funding lift looking at social media (fb pages) and funding videos
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
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

####################
### Social media Availability
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df_view['fb_label'] = df_view['project_has_facebook_page'].apply(lambda x: 'Has Facebook' if x is True else 'No Facebook')
success_df_fb = df_view[df_view['project_success'] == True]
failed_df_fb = df_view[df_view['project_success'] == False]

fig_fb = go.Figure()

fig_fb.add_trace(go.Box(
    x=success_df_fb['fb_label'],
    y=success_df_fb['amt_pledged_$'],
    name='Successful',
    marker_color='#00CC96',
    boxpoints=None
))

fig_fb.add_trace(go.Box(
    x=failed_df_fb['fb_label'],
    y=failed_df_fb['amt_pledged_$'],
    name='Unsuccessful',
    marker_color='#EF553B',
    boxpoints=None
))

fig_fb.update_layout(
    title={'text': 'Social Lift: Impact of Facebook Pages', 'x': 0.5},
    yaxis_title="Total Amount Pledged ($)",
    xaxis_title="Facebook Page Presence",
    boxmode='group',
    template='plotly_white'
)

fig_fb.show()

####################
## Social media impact facebook friends count
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
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

####################
## Duration and goal $
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Clean Goal and Duration
df['goal_$'] = pd.to_numeric(df['goal_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
df['duration_days'] = pd.to_numeric(df['duration_days'], errors='coerce')

# Capping at $100k and 60 days ensures the bins aren't stretched too thin
df_view = df[(df['goal_$'] <= 100000) & (df['duration_days'] <= 60)].copy()

failed_df = df_view[df_view['project_success'] == False]

fig_danger = px.density_heatmap(
    failed_df, 
    x='duration_days', 
    y='goal_$', 
    nbinsx=20, 
    nbinsy=20,
    color_continuous_scale='YlOrRd', # Yellow to Red for "Danger"
    title='<b>The Danger Zone:</b> Where High Goals Meet Short Deadlines',
    labels={'duration_days': 'Campaign Duration (Days)', 'goal_$': 'Funding Goal ($)'},
    template='plotly_white'
)

fig_danger.update_layout(
    title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
    xaxis_title="Days the Campaign Lasted",
    yaxis_title="Financial Goal ($)",
    coloraxis_colorbar=dict(title="Concentration of Failures"),
    height=600
)

fig_danger.add_annotation(
    x=10, y=85000, # Points to the top-left (Short duration, High goal)
    text="<b>DANGER ZONE</b><br>High goals with very short windows<br>show the highest risk of failure.",
    showarrow=True, arrowhead=2,
    ax=50, ay=0,
    bgcolor="white", bordercolor="#EF553B"
)

fig_danger.show()

####################
## Most valuable backers
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['avg_amt$_per_pledger'] = pd.to_numeric(df['avg_amt$_per_pledger'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
# We group by both category and success to see if successful projects attract "higher value" backers
category_stats = df.groupby(['major_category', 'project_success'])['avg_amt$_per_pledger'].mean().reset_index()
# We find the order of categories based on the highest average pledge for successful projects
sort_order = category_stats[category_stats['project_success'] == True].sort_values('avg_amt$_per_pledger', ascending=False)['major_category'].tolist()
success_data = category_stats[category_stats['project_success'] == True]
failed_data = category_stats[category_stats['project_success'] == False]

fig_value = go.Figure()

# Successful Projects Trace
fig_value.add_trace(go.Bar(
    x=success_data['major_category'],
    y=success_data['avg_amt$_per_pledger'],
    name='Reached Goal',
    marker_color='#00CC96',
    text=success_data['avg_amt$_per_pledger'].map('${:,.0f}'.format),
    textposition='auto'
))

# Unsuccessful Projects Trace
fig_value.add_trace(go.Bar(
    x=failed_data['major_category'],
    y=failed_data['avg_amt$_per_pledger'],
    name='Did Not Reach Goal',
    marker_color='#EF553B',
    text=failed_data['avg_amt$_per_pledger'].map('${:,.0f}'.format),
    textposition='auto'
))

fig_value.update_layout(
    title={'text': '<b>The Backer Value Index:</b> Which Categories Attract the Highest Pledges?', 'x': 0.5},
    xaxis_title="Project Category",
    yaxis_title="Average Amount per Backer ($)",
    xaxis={'categoryorder': 'array', 'categoryarray': sort_order}, # Applies our custom sort
    barmode='group',
    template='plotly_white',
    height=600,
    legend_title="Project Status"
)

fig_value.show()