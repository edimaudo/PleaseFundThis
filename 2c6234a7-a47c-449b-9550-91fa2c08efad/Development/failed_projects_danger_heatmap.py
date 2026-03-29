####################
## Duration and goal $
####################

# Clean Goal and Duration
df['goal_$'] = pd.to_numeric(df['goal_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
df['duration_days'] = pd.to_numeric(df['duration_days'], errors='coerce')

# Capping at $100k and 60 days ensures the bins aren't stretched too thin
df_view = df[(df['goal_$'] <= 100000) & (df['duration_days'] <= 60)].copy()

failed_df = df_view[df_view['project_success'] == False]

fig_danger = px.density_heatmap(
    failed_df, 
    x='duration_days', 
    y='goal_$', 
    nbinsx=20, 
    nbinsy=20,
    color_continuous_scale='YlOrRd', # Yellow to Red for "Danger"
    title='<b>The Danger Zone:</b> Where High Goals Meet Short Deadlines',
    labels={'duration_days': 'Campaign Duration (Days)', 'goal_$': 'Funding Goal ($)'},
    template='plotly_white'
)

fig_danger.update_layout(
    title={'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'},
    xaxis_title="Days the Campaign Lasted",
    yaxis_title="Financial Goal ($)",
    coloraxis_colorbar=dict(title="Concentration of Failures"),
    height=600
)

fig_danger.add_annotation(
    x=10, y=85000, # Points to the top-left (Short duration, High goal)
    text="<b>DANGER ZONE</b><br>High goals with very short windows<br>show the highest risk of failure.",
    showarrow=True, arrowhead=2,
    ax=50, ay=0,
    bgcolor="white", bordercolor="#EF553B"
)

fig_danger.show()
