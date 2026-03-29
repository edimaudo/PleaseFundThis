####################
## Major Category Ranking
####################

major_ranked = df.groupby('major_category')['amt_pledged_$'].sum().reset_index()
major_ranked = major_ranked.sort_values('amt_pledged_$', ascending=False)

fig_major = px.bar(
    major_ranked,
    x='amt_pledged_$',
    y='major_category',
    orientation='h',
    title='Pledge Amount by Major Category',
    labels={'amt_pledged_$': 'Pledged Amount ($)', 'major_category': 'Major Category'},
    color='amt_pledged_$',
    color_continuous_scale='viridis',
    text_auto='.2s' # Displays formatted values on bars
)

fig_major.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_major.show()
