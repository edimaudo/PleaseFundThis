####################
## City Success
####################
df['city'] = df['city'].astype(str).str.strip().str.title()
df['is_success'] = pd.to_numeric(df['project_success'], errors='coerce').fillna(0).astype(bool)
if df['is_success'].sum() == 0:
    df['is_success'] = df['project_success'].astype(str).str.strip().str.upper() == 'TRUE'

# Calculate metrics
city_stats = df.groupby('city')['is_success'].agg(['sum', 'count']).reset_index()
city_stats.columns = ['City', 'Successes', 'Total_Outcomes']
city_stats['Success Rate'] = (city_stats['Successes'] / city_stats['Total_Outcomes']) * 100
top_cities = city_stats[city_stats['Total_Outcomes'] >= 10].sort_values('Success Rate', ascending=False)

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