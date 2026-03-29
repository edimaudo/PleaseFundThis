##=====================
# Strategic Storylines
##=====================

####################
## Anatomy of an overachiever
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Create the segments based on Percent Raised
def segment_success(percent):
    if percent >= 500: return 'Overachiever (500%+)'
    elif percent >= 100: return 'Standard Winner (100-499%)'
    else: return 'Failed Project (<100%)'

df['Success_Tier'] = df['percent_raised'].apply(segment_success)

# Calculating means for Update Counts and Pledge Level Counts
anatomy_stats = df.groupby('Success_Tier').agg({
    'project_update_count': 'mean',
    'total_count_of_pledge_levels': 'mean',
    'project_id': 'count'
}).reindex(['Overachiever (500%+)', 'Standard Winner (100-499%)', 'Failed Project (<100%)']).reset_index()

fig = go.Figure()

# Add Bars for Update Frequency
fig.add_trace(go.Bar(
    x=anatomy_stats['Success_Tier'],
    y=anatomy_stats['project_update_count'],
    name='Avg Updates',
    marker_color='#636EFA',
    text=anatomy_stats['project_update_count'].round(1),
    textposition='auto'
))

# Add Bars for Pledge Levels
fig.add_trace(go.Bar(
    x=anatomy_stats['Success_Tier'],
    y=anatomy_stats['total_count_of_pledge_levels'],
    name='Avg Pledge Tiers',
    marker_color='#00CC96',
    text=anatomy_stats['total_count_of_pledge_levels'].round(1),
    textposition='auto'
))

fig.update_layout(
    title='<b>Anatomy of an Overachiever:</b> Updates vs. Reward Complexity',
    xaxis_title='Project Success Segment',
    yaxis_title='Average Count',
    barmode='group',
    template='plotly_white',
    title_x=0.5,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show()

# Print Summary for Interpretation
print(anatomy_stats)

"""
Findings: Overachievers update their backers x more often than failed projects (8.5 updates vs. 4.7 on average).
Successful projects offer an average of 10.6 pledge levels, providing significantly more entry points than the 8.4 levels offered by failures.
A direct linear correlation exists between update frequency and the final funding percentage.

1. The "Update" Correlation

The Trend: Typically, Overachievers have a significantly higher update count.
The Insight: This suggests that viral success isn't a "set it and forget it" event. 
Overachievers likely use updates to maintain momentum, announce "stretch goals," and keep the community engaged during the exponential growth phase.
Actionable Advice: If you want to break out of the "Standard Winner" pack, double your communication frequency.

2. The "Pledge Tier" Strategy
The Trend: If Overachievers have more pledge levels than Failures, it indicates that Choice Architecture matters.
The Insight: More tiers allow for "Price Discrimination"—it lets small backers in for $5 while giving high-net-worth fans a way to spend $1,000.
The Trap: If Overachievers have fewer levels than Standard Winners, it suggests that Simplicity wins when a project goes viral. Too many choices can cause "Analysis Paralysis."

3. The "Standard Winner" Gap
Look at the distance between the Standard Winner and the Overachiever. If the Update count jumps significantly (e.g., from 10 to 25 updates), 
that is your "Viral Threshold." That is the extra effort required to cross from "Successful" to "Legendary."
"""

####################
## Global map of Success
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['city'] = df['city'].astype(str).str.strip().str.title()
df['is_success'] = pd.to_numeric(df['project_success'], errors='coerce').fillna(0).astype(bool)
if df['is_success'].sum() == 0:
    df['is_success'] = df['project_success'].astype(str).str.strip().str.upper() == 'TRUE'

# Calculate metrics
city_stats = df.groupby('city')['is_success'].agg(['sum', 'count']).reset_index()
city_stats.columns = ['City', 'Successes', 'Total_Outcomes']
city_stats['Success Rate'] = (city_stats['Successes'] / city_stats['Total_Outcomes']) * 100
top_cities = city_stats[city_stats['Total_Outcomes'] >= 10].sort_values('Success Rate', ascending=False)
# fig_geo = px.bar(
#     top_cities.head(20), 
#     x='City', 
#     y='Success Rate',
#     color='Success Rate',
#     text_auto='.1f',
#     title='<b>Top Cities by Success Rate</b>',
#     labels={'Success Rate': 'Success Rate (%)'},
#     color_continuous_scale='viridis',
#     template='plotly_white'
# )

# fig_geo.update_layout(
#     title_x=0.5
# )
# fig_geo.show()
fig_geo = px.bar(
    top_cities.head(20), 
    x='Success Rate',      # Move numeric value to x
    y='City',              # Move category to y
    color='Success Rate',
    orientation='h',       # Explicitly set horizontal orientation
    text_auto='.1f',
    title='<b>Top Cities by Success Rate</b>',
    labels={'Success Rate': 'Success Rate (%)', 'City': 'Location'},
    color_continuous_scale='viridis',
    template='plotly_white'
)

fig_geo.update_layout(
    title_x=0.5,
    yaxis={'categoryorder':'total ascending'} # Keeps the highest rate at the top
)

fig_geo.show()

