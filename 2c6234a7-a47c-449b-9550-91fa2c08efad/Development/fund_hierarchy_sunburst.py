## Category and Markets

# Ensure amt_pledged_$ is numeric (handling potential strings/commas)
if df['amt_pledged_$'].dtype == 'object':
    df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].str.replace(r'[$,]', '', regex=True), errors='coerce')

fig_sunburst = px.sunburst(
    df, 
    path=['major_category', 'minor_category'], 
    values='amt_pledged_$',
    color='amt_pledged_$',
    #color_continuous_scale='Viridis',
    title='Funding Hierarchy: Major to Minor Category Breakdown',
    labels={'amt_pledged_$': 'Total Amount Pledged $'}
)


# FIXED: Removed 'valueformat' and strictly used 'hovertemplate' for formatting
fig_sunburst.update_traces(
    hovertemplate='<b>%{label}</b><br>Total Amount Pledged $: %{value:,.2f}<extra></extra>'
)

fig_sunburst.update_layout(
    template='plotly_white', 
    margin=dict(l=10, r=10, t=40, b=10),
    title_font_size=20, 
    title_x=0.5, 
    height=500
)

fig_sunburst.show()

# 3. Update the color bar title specifically (optional but recommended for consistency)
fig_sunburst.update_coloraxes(colorbar_title="Total Amount Pledged $")

fig_sunburst.show()

fig_treemap = px.treemap(
    df, 
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='amt_pledged_$',
    color='amt_pledged_$',
    color_continuous_scale='Viridis',
    title='Funding Hierarchy: Major to Minor Category Breakdown',
    labels={'amt_pledged_$': 'Total Amount Pledged $'}
)

# 5. Apply the specific 2-decimal formatting via hovertemplate
fig_treemap.update_traces(
    hovertemplate='<b>%{label}</b><br>Total Amount Pledged $: %{value:,.2f}<extra></extra>'
)

# 6. Final Layout Adjustments
fig_treemap.update_layout(
    template='plotly_white', 
    margin=dict(l=10, r=10, t=40, b=10),
    title_font_size=20, 
    title_x=0.5, 
    height=500
)

fig_treemap.show()

major_ranked = df.groupby('major_category')['amt_pledged_$'].sum().reset_index()
major_ranked = major_ranked.sort_values('amt_pledged_$', ascending=False)

# Create Bar Chart
fig_major = px.bar(
    major_ranked,
    x='amt_pledged_$',
    y='major_category',
    orientation='h',
    title='Ranked Funding by Major Category',
    labels={'amt_pledged_$': 'Total Pledged ($)', 'major_category': 'Category'},
    color='amt_pledged_$',
    color_continuous_scale='Blues',
    text_auto='.2s' # Displays formatted values on bars
)

fig_major.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_major.show()

minor_ranked = df.groupby('minor_category')['amt_pledged_$'].sum().reset_index()
minor_ranked = minor_ranked.sort_values('amt_pledged_$', ascending=False).head(20) # Showing top 20 for readability

# Create Bar Chart
fig_minor = px.bar(
    minor_ranked,
    x='amt_pledged_$',
    y='minor_category',
    orientation='h',
    title='Top 20 Ranked Minor Categories by Funding',
    labels={'amt_pledged_$': 'Total Pledged ($)', 'minor_category': 'Sub-Category'},
    color='amt_pledged_$',
    color_continuous_scale='Reds',
    text_auto='.2s'
)

fig_minor.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_minor.show()