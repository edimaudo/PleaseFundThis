####################
## Parallel Categories Diagram
####################
df['Video?'] = df['project_has_video'].map({True: 'Has Video', False: 'No Video'})
df['FB Page?'] = df['project_has_facebook_page'].map({True: 'Has FB Page', False: 'No FB Page'})
df['Outcome'] = df['project_success'].map({True: 'Successful', False: 'Failed'})

fig_parallel = px.parallel_categories(
    df, 
    dimensions=['Video?', 'FB Page?', 'Outcome'],
    color='project_success', # Colors the paths based on the final result
    color_continuous_scale=['#EF553B', '#00CC96'], # Red (Fail) to Green (Success)
    title='Multi-Factor Success Paths: Video & Facebook Influence',
    labels={'Video?': 'Video Presence', 'FB Page?': 'Facebook Presence', 'Outcome': 'Project Outcome'},
    template='plotly_white'
)

fig_parallel.update_layout(
    title_x=0.5,
    margin=dict(l=100, r=100, t=100, b=100),
    coloraxis_showscale=False, # Hide the color scale bar for a cleaner look
    height=600
)

fig_parallel.show()