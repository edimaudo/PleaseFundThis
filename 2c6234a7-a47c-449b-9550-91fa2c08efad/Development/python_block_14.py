####################
## Minor Category Ranking
####################
minor_ranked = df.groupby('minor_category')['amt_pledged_$'].sum().reset_index()
minor_ranked = minor_ranked.sort_values('amt_pledged_$', ascending=False)

fig_minor = px.bar(
    minor_ranked,
    x='amt_pledged_$',
    y='minor_category',
    orientation='h',
    title='Top Ranked Minor Categories by Funding',
    labels={'amt_pledged_$': 'Total Pledged ($)', 'minor_category': 'Sub-Category'},
    color='amt_pledged_$',
    color_continuous_scale='viridis',
    text_auto='.2s'
)

fig_minor.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_minor.show()