
####################
#### Shows the largest platform communities by Category ####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
if df['number_of_pledgers'].dtype == 'object':
    df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'].str.replace(',', ''), errors='coerce')

# The hierarchy goes from the whole platform -> Major Category -> Minor Category
fig_treemap_pledge_count = px.treemap(
    df,
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='number_of_pledgers',
    color='number_of_pledgers',
    color_continuous_scale='Viridis',
    title='Platform Community Size: Pledgers by Category'
)

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

####################
#### Shows goal $ distribution by major category ####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['goal_$'] = pd.to_numeric(df['goal_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# (Log Scale)
df['log_goal'] = np.log10(df['goal_$'].replace(0, 1))
categories = sorted(df['major_category'].unique())
colors = px.colors.sequential.Viridis

fig_ridge = go.Figure()

for i, cat in enumerate(categories):
    df_cat = df[df['major_category'] == cat]
    
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


fig_ridge.update_layout(
    title='The "Mountain Range" of Goal Distributions',
    title_x=0.5,
    xaxis_title="Goal Amount (Log Scale)",
    yaxis_title="Major Category",
    template='plotly_white',   
    showlegend=False,
    height=800,
    violingap=0, 
    violingroupgap=0
)


fig_ridge.update_xaxes(
    tickvals=[1, 2, 3, 4, 5, 6],
    ticktext=['$10', '$100', '$1k', '$10k', '$100k', '$1M'],
    gridcolor='lightgrey',     
    zerolinecolor='grey'
)

fig_ridge.show()