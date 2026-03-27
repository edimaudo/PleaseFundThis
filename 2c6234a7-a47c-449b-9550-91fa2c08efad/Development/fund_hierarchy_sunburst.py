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


## Shows the largest platform communities by Category
if df['number_of_pledgers'].dtype == 'object':
    df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'].str.replace(',', ''), errors='coerce')

# 3. Create the Treemap
# The hierarchy goes from the whole platform -> Major Category -> Minor Category
fig_treemap_pledge_count = px.treemap(
    df,
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='number_of_pledgers',
    color='number_of_pledgers',
    color_continuous_scale='Viridis',
    title='Platform Community Size: Pledgers by Category'
)

# 4. Styling and Interactivity
fig_treemap_pledge_count.update_traces(
    textinfo="label+value",
    hovertemplate='<b>%{label}</b><br>Total Pledgers: %{value:,.0f}<extra></extra>'
)

fig_treemap_pledge_count.update_layout(
    margin=dict(t=80, l=10, r=10, b=10),
    title_x=0.5,
    title_font_size=20,
    coloraxis_colorbar=dict(title="Pledgers")
)

fig_treemap_pledge_count.show()

## Shows goal $ distribution by major category
df['goal_$'] = pd.to_numeric(df['goal_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# 2. Preparation (Log Scale)
df['log_goal'] = np.log10(df['goal_$'].replace(0, 1))
categories = sorted(df['major_category'].unique())

# Generate a color palette based on the number of categories
colors = px.colors.sequential.Viridis

# 3. Build the Figure
fig_ridge = go.Figure()

for i, cat in enumerate(categories):
    df_cat = df[df['major_category'] == cat]
    
    # Pick a color from the scale based on the index
    color_idx = i % len(colors)
    
    fig_ridge.add_trace(go.Violin(
        x=df_cat['log_goal'],
        line_color='black',       # Darker lines for contrast on white background
        line_width=1,
        fillcolor=colors[color_idx], 
        name=cat,
        orientation='h',
        side='positive', 
        width=4,                 # Increased width to ensure nice overlapping
        points=False
    ))

# 4. Styling (Light Theme)
fig_ridge.update_layout(
    title='The "Mountain Range" of Goal Distributions',
    title_x=0.5,
    xaxis_title="Goal Amount (Log Scale)",
    yaxis_title="Major Category",
    template='plotly_white',    # Switched to light template
    showlegend=False,
    height=800,
    violingap=0, 
    violingroupgap=0
)

# 5. X-Axis Formatting
fig_ridge.update_xaxes(
    tickvals=[1, 2, 3, 4, 5, 6],
    ticktext=['$10', '$100', '$1k', '$10k', '$100k', '$1M'],
    gridcolor='lightgrey',      # Subtle grid lines for better readability
    zerolinecolor='grey'
)

fig_ridge.show()

## Goal $ Histogram
df_filtered = df[(df['goal_$'] > 0) & (df['goal_$'] <= 100000)].copy()

# 3. Create the Histogram
fig_anchors = px.histogram(
    df_filtered, 
    x="goal_$", 
    nbins=500, # High bin count is CRITICAL to see the narrow spikes
    title='Psychological Anchoring: The "Round Number" Effect in Project Goals',
    labels={'goal_$': 'Funding Goal ($)'},
    template='plotly_white',
    color_discrete_sequence=['#636EFA']
)

# 4. Styling for Clarity
fig_anchors.update_layout(
    title_x=0.5,
    xaxis_title="Funding Goal Amount ($)",
    yaxis_title="Frequency (Number of Projects)",
    bargap=0.1,
    xaxis=dict(
        tickvals=[0, 1000, 5000, 10000, 20000, 25000, 50000, 75000, 100000],
        tickformat='$,.0f',
        range=[0, 100000]
    )
)

# Add annotations for the biggest peaks
fig_anchors.add_annotation(x=10000, yref='paper', y=0.9, text="The $10k Anchor", showarrow=True, arrowhead=1)
fig_anchors.add_annotation(x=5000, yref='paper', y=0.7, text="$5k Peak", showarrow=True, arrowhead=1)

fig_anchors.show()

## Word cloud