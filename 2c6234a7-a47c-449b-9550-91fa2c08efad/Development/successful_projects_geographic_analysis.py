## Geographical Succes and Failure

region_fixes = {
    'Glasgow': 'Scotland',
    'Los Angeles': 'United States',
    'Queens': 'United States',
    'Kyoto': 'Japan'
}
df['region'] = df['region'].replace(region_fixes)

df_success = df[df['project_success'].astype(str).str.upper() == 'TRUE'].copy()

# Visualization
region_success_counts = df_success.groupby('region').size().reset_index(name='Successful Projects')

fig_map = px.choropleth(
    region_success_counts,
    locations="region",
    locationmode="country names", # Matches full names like 'United States', 'Japan'
    color="Successful Projects",
    hover_name="region",
    title="Global Success Hotspots by Region",
    color_continuous_scale=px.colors.sequential.Plasma,
    template='plotly_white'
)

fig_map.update_layout(height=600,title_font_size=20, title_x=0.5)
fig_map.show()

# Ranked Bar Chart by Region 
region_rank = df_success.groupby('region').size().reset_index(name='Successful Projects')
region_rank = region_rank.sort_values('Successful Projects', ascending=True).tail(5)

fig_region = px.bar(
    region_rank,
    x='Successful Projects',
    y='region',
    orientation='h',
    title='Top 5 Successful Regions',
    labels={'Successful Projects': 'Count of Successes', 'region': 'Region'},
    color='Successful Projects',
    color_continuous_scale='viridis',
    text_auto=True
)

fig_region.update_layout(
    template='plotly_white', 
    height=600, 
    showlegend=False, 
    title_font_size=20, 
    title_x=0.5
)

fig_region.show()

# Ranked Bar Chart by City 
city_rank = df_success.groupby('city').size().reset_index(name='Successful Projects')
city_rank = city_rank.sort_values('Successful Projects', ascending=True).tail(20)

fig_city = px.bar(
    city_rank,
    x='Successful Projects',
    y='city',
    orientation='h',
    title='Top 20 Successful Cities (Ranked)',
    labels={'Successful Projects': 'Count of Successes', 'city': 'City'},
    color='Successful Projects',
    color_continuous_scale='viridis',
    text_auto=True
)

fig_city.update_layout(template='plotly_white', height=600, showlegend=False, title_font_size=20, title_x=0.5)
fig_city.show()

## Success Rate
city_stats = df.groupby('city')['project_success'].agg(
    total_projects='count',
    successful_projects=lambda x: (x == True).sum() # Count only the True values
).reset_index()

# 3. Perform the division for the Success Rate
city_stats['success_rate'] = city_stats['successful_projects'] / city_stats['total_projects']

# 4. Filter and Sort
# We take the Top 10 cities by success rate, sorted descending (highest at the top)
top_cities = city_stats.sort_values(by='success_rate', ascending=False).head(25)

# Sort ascending for the Lollipop plot Y-axis so the highest value appears at the top
top_cities = top_cities.sort_values(by='success_rate', ascending=True)

# 5. Create the Lollipop Chart
fig_lollipop = go.Figure()

# Add the 'sticks'
for i, row in top_cities.iterrows():
    fig_lollipop.add_shape(
        type='line',
        x0=0, y0=row['city'],
        x1=row['success_rate'], y1=row['city'],
        line=dict(color='#636EFA', width=2)
    )

# Add the 'lollipops' (markers)
fig_lollipop.add_trace(go.Scatter(
    x=top_cities['success_rate'],
    y=top_cities['city'],
    mode='markers',
    marker=dict(
        color='#EF553B', 
        size=12,
        line=dict(color='white', width=1)
    ),
    hovertemplate='<b>%{y}</b><br>Success Rate: %{x:.2%}<extra></extra>'
))

# 6. Styling
fig_lollipop.update_layout(
    title='Top Cities: Ranking by Efficiency (Success Rate)',
    title_x=0.5,
    title_font_size=20,
    xaxis_title='Success Rate (%)',
    yaxis_title='City',
    template='plotly_white',
    xaxis=dict(tickformat='.0%', range=[0, 1.1]), # Format as percentage
    height=600
)

fig_lollipop.show()

## Success / Failure comparision
# 2. Identify the Top 25 Cities by total project count
top_cities_vol = df['city'].value_counts().nlargest(25).index.tolist()

# 3. Create two separate dataframes for Success and Failure
# This avoids any "mapping" or "KeyError" issues
success_df = df[(df['city'].isin(top_cities_vol)) & (df['project_success'] == True)]
fail_df = df[(df['city'].isin(top_cities_vol)) & (df['project_success'] == False)]

# 4. Count occurrences per city for both
success_counts = success_df.groupby('city').size().reindex(top_cities_vol, fill_value=0)
fail_counts = fail_df.groupby('city').size().reindex(top_cities_vol, fill_value=0)

# 5. Build the figure manually with two independent traces
fig = go.Figure()

# Success Bar (Green)
fig.add_trace(go.Bar(
    x=top_cities_vol,
    y=success_counts,
    name='Success',
    marker_color='#2ca02c'
))

# Fail Bar (Red)
fig.add_trace(go.Bar(
    x=top_cities_vol,
    y=fail_counts,
    name='Fail',
    marker_color='#d62728'
))

# 6. Set to 'stack' mode and style
fig.update_layout(
    title_font_size=20,
    title='Top Cities: Success vs. Fail Volume Comparison',
    title_x=0.5,
    xaxis_title='City',
    yaxis_title='Number of Projects',
    barmode='stack', # This stacks the Success and Fail traces
    template='plotly_white',
    xaxis_tickangle=-45,
    height=600,
    legend_title_text='Outcome'
)

fig.show()