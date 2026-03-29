##=====================
## Category and Markets
##=====================

####################
#### Category Grouping Treemap #####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()

if df['amt_pledged_$'].dtype == 'object':
    df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].str.replace(r'[$,]', '', regex=True), errors='coerce')

fig_treemap = px.treemap(
    df, 
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='amt_pledged_$',
    color='amt_pledged_$',
    color_continuous_scale='Viridis',
    title='Funding Hierarchy: Major to Minor Category Breakdown',
    labels={'amt_pledged_$': 'Total Amount Pledged $'}
)

fig_treemap.update_traces(
    hovertemplate='<b>%{label}</b><br>Total Amount Pledged $: %{value:,.2f}<extra></extra>'
)

fig_treemap.update_layout(
    template='plotly_white', 
    margin=dict(l=10, r=10, t=40, b=10),
    title_font_size=20, 
    title_x=0.5, 
    height=500
)

fig_treemap.show()