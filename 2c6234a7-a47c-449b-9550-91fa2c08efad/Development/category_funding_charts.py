
####################
#### Category Bar Charts #####
####################
# df = pd.read_csv('PleaseFundThis.csv')
# df.columns = df.columns.str.strip()
major_ranked = df.groupby('major_category')['amt_pledged_$'].sum().reset_index()
major_ranked = major_ranked.sort_values('amt_pledged_$', ascending=False)
minor_ranked = df.groupby('minor_category')['amt_pledged_$'].sum().reset_index()
minor_ranked = minor_ranked.sort_values('amt_pledged_$', ascending=False)

# Create Major Cateogry Bar Chart
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

# Create Minor Category Bar Chart
fig_minor = px.bar(
    minor_ranked,
    x='amt_pledged_$',
    y='minor_category',
    orientation='h',
    title='Top Ranked Minor Categories by Funding',
    labels={'amt_pledged_$': 'Total Pledged ($)', 'minor_category': 'Sub-Category'},
    color='amt_pledged_$',
    color_continuous_scale='Reds',
    text_auto='.2s'
)

fig_minor.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_minor.show()