## Flow and Distribution

## Sankey chart major category --> minor category --> success
top_minors = df['minor_category'].value_counts().nlargest(30).index
df_filtered = df[df['minor_category'].isin(top_minors)].copy()

# Map outcomes to strings
df_filtered['outcome'] = df_filtered['project_success'].map({True: 'Successful', False: 'Failed'})

# 3. Create Node List and Mapping
majors = sorted(df_filtered['major_category'].unique().tolist())
minors = sorted(df_filtered['minor_category'].unique().tolist())
outcomes = ['Successful', 'Failed']
label_list = majors + minors + outcomes
label_map = {label: i for i, label in enumerate(label_list)}

source_list = []
target_list = []
value_list = []
link_colors = []

# --- Layer 1: Major -> Minor ---
flow1 = df_filtered.groupby(['major_category', 'minor_category']).size().reset_index(name='count')
for _, row in flow1.iterrows():
    source_list.append(label_map[row['major_category']])
    target_list.append(label_map[row['minor_category']])
    value_list.append(row['count'])
    link_colors.append("rgba(200, 200, 200, 0.3)") # Neutral grey for the middle

# --- Layer 2: Minor -> Outcome ---
flow2 = df_filtered.groupby(['minor_category', 'outcome']).size().reset_index(name='count')
for _, row in flow2.iterrows():
    source_list.append(label_map[row['minor_category']])
    target_list.append(label_map[row['outcome']])
    value_list.append(row['count'])
    # Color the final path: Green for Success, Red for Failure
    if row['outcome'] == 'Successful':
        link_colors.append("rgba(0, 204, 150, 0.5)")
    else:
        link_colors.append("rgba(239, 85, 59, 0.5)")

# 4. Create the Figure
fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 30,         # Increased padding makes nodes easier to click/hover
      thickness = 15,
      line = dict(color = "white", width = 2),
      label = label_list,
      color = "#333333" # Dark nodes for a professional "light mode" look
    ),
    link = dict(
      source = source_list,
      target = target_list,
      value = value_list,
      color = link_colors
    )
)])

# 5. Styling for "Mobile-Friendly" Clarity
fig_sankey.update_layout(
    title_text="<b>Project Flow: From Category to Success</b>",
    title_x=0.5,
    font=dict(size=12, color="black"),
    height=700,
    margin=dict(l=20, r=20, t=60, b=20), # Tight margins to maximize use of space
    template='plotly_white'
)

fig_sankey.show()

## Parallel Categories Diagram
# We map the boolean values to descriptive strings for a cleaner UI
df['Video?'] = df['project_has_video'].map({True: 'Has Video', False: 'No Video'})
df['FB Page?'] = df['project_has_facebook_page'].map({True: 'Has FB Page', False: 'No FB Page'})
df['Outcome'] = df['project_success'].map({True: 'Successful', False: 'Failed'})

# 3. Create the Parallel Categories Plot
fig_parallel = px.parallel_categories(
    df, 
    dimensions=['Video?', 'FB Page?', 'Outcome'],
    color='project_success', # Colors the paths based on the final result
    color_continuous_scale=['#EF553B', '#00CC96'], # Red (Fail) to Green (Success)
    title='Multi-Factor Success Paths: Video & Facebook Influence',
    labels={'Video?': 'Video Presence', 'FB Page?': 'Facebook Presence', 'Outcome': 'Project Outcome'},
    template='plotly_white'
)

# 4. Styling for Clarity
fig_parallel.update_layout(
    title_x=0.5,
    margin=dict(l=100, r=100, t=100, b=100),
    coloraxis_showscale=False, # Hide the color scale bar for a cleaner look
    height=600
)

fig_parallel.show()

## Whales vs the crowd
def get_quadrant(row):
    avg_pledge = row['amt_pledged_$'] / max(1, row['number_of_pledgers'])
    high_backers = row['number_of_pledgers'] > 500
    high_value = avg_pledge > 100
    
    if high_backers and high_value:
        return "The Unicorns (High Volume & High Value)"
    if high_backers and not high_value:
        return "The Crowd (Mass Appeal, Low Cost)"
    if not high_backers and high_value:
        return "The Whales (Boutique, High Cost)"
    return "The Baseline (Small Scale)"

df['Project_Type'] = df.apply(get_quadrant, axis=1)
df['Outcome'] = df['project_success'].map({True: 'Successful', False: 'Failed'})

# 3. Create a Simple Percentage Bar Chart
# This shows the "Success Rate" for each of the 4 buckets
quadrant_stats = df.groupby('Project_Type')['project_success'].mean().reset_index()
quadrant_stats['Success_Rate_%'] = quadrant_stats['project_success'] * 100

fig_quadrant = px.bar(
    quadrant_stats.sort_values('Success_Rate_%', ascending=False),
    x='Success_Rate_%',
    y='Project_Type',
    orientation='h',
    title='Which Strategy Actually Works? (Success Rate by Project Type)',
    color='Success_Rate_%',
    color_continuous_scale='RdYlGn',
    labels={'Success_Rate_%': 'Probability of Success (%)', 'Project_Type': ''},
    template='plotly_white',
    text_auto='.1f'
)

fig_quadrant.update_layout(showlegend=False, height=400,    title_x=0.5,)
fig_quadrant.show()

# Density price rewards

# Clean Currency
df['lowest_pledge_reward_$'] = pd.to_numeric(df['lowest_pledge_reward_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# 2. THE FIX: Separate by Project Result (Your provided logic)
# We filter to $200 for a readable linear scale
df_low = df[df['lowest_pledge_reward_$'] <= 10000]
success_df = df_low[df_low['project_success'] == True]
failed_df = df_low[df_low['project_success'] == False]

fig_low = go.Figure()

# Add Successful Trace
fig_low.add_trace(go.Violin(
    y=success_df['lowest_pledge_reward_$'],
    name='Successful',
    line_color='#00CC96',
    box_visible=True,
    meanline_visible=True
))

# Add Unsuccessful Trace
fig_low.add_trace(go.Violin(
    y=failed_df['lowest_pledge_reward_$'],
    name='Unsuccessful',
    line_color='#EF553B',
    box_visible=True,
    meanline_visible=True
))

fig_low.update_layout(
    title={'text': 'Entry Level Pledge Density (Up to $200)', 'x': 0.5},
    yaxis_title="Pledge Amount ($)",
    template='plotly_white'
)

fig_low.show()




# 1. Clean Currency for High Tier
df['highest_pledge_reward_$'] = pd.to_numeric(df['highest_pledge_reward_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# 2. Separate by Project Result (Your provided logic)
# We filter to $1000 to maintain a non-technical linear scale
df_high = df[df['highest_pledge_reward_$'] <= 10000]
success_df_h = df_high[df_high['project_success'] == True]
failed_df_h = df_high[df_high['project_success'] == False]

fig_high = go.Figure()

# Add Successful Trace
fig_high.add_trace(go.Violin(
    y=success_df_h['highest_pledge_reward_$'],
    name='Successful',
    line_color='#00CC96',
    box_visible=True,
    meanline_visible=True
))

# Add Unsuccessful Trace
fig_high.add_trace(go.Violin(
    y=failed_df_h['highest_pledge_reward_$'],
    name='Unsuccessful',
    line_color='#EF553B',
    box_visible=True,
    meanline_visible=True
))

fig_high.update_layout(
    title={'text': 'High-Tier Pledge Density', 'x': 0.5},
    yaxis_title="Pledge Amount ($)",
    template='plotly_white'
)

fig_high.show()