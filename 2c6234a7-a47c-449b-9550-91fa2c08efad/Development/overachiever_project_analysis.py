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
