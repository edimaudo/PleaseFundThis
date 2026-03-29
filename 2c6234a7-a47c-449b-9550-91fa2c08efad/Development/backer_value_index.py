####################
## Most valuable backers
####################
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