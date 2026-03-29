####################
## Whales vs the crowd
####################
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