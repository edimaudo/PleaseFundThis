####################
## Launch window day of week
####################
df['Day_of_Week'] = df['date_launched'].dt.day_name()
day_df = df.groupby('Day_of_Week')['success_numeric'].mean().reset_index()
day_df['Success_Rate_Pct'] = day_df['success_numeric'] * 100
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
fig_daily = px.bar(
    day_df, 
    x='Day_of_Week', 
    y='Success_Rate_Pct',
    title='Launch Strategy: Success Rate by Day of Week',
    category_orders={'Day_of_Week': week_order},
    color='Success_Rate_Pct',
    text_auto='.1f',
    template='plotly_white',
    labels={'Success_Rate_Pct': 'Success Rate (%)', 'Day_of_Week': 'Day of Launch'}
)
fig_daily.update_layout(
    title_font_size=20,
    title_x=0.5,
    showlegend=False,
    yaxis_range=[0, max(day_df['Success_Rate_Pct']) + 10]
)

fig_daily.show()