####################
## Goal $ distribution by major category 
####################
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