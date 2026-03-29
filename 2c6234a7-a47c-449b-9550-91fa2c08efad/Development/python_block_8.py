####################
## Creator personas
####################

# Clean Numeric Data
df['avg_amt$_per_pledger'] = pd.to_numeric(df['avg_amt$_per_pledger'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'], errors='coerce')

df = df.dropna(subset=['avg_amt$_per_pledger', 'number_of_pledgers'])

# Thresholds (Medians)
x_mid = df['number_of_pledgers'].median()
y_mid = df['avg_amt$_per_pledger'].median()

# Numeric Quadrant Assignment
def assign_num(row):
    if row['avg_amt$_per_pledger'] >= y_mid and row['number_of_pledgers'] >= x_mid: return 1
    if row['avg_amt$_per_pledger'] >= y_mid and row['number_of_pledgers'] < x_mid:  return 2
    if row['avg_amt$_per_pledger'] < y_mid and row['number_of_pledgers'] >= x_mid:  return 3
    return 4

df['Quad_Num'] = df.apply(assign_num, axis=1)

fig_menu = px.scatter(
    df,
    x='number_of_pledgers',
    y='avg_amt$_per_pledger',
    color='Quad_Num',
    log_x=True, log_y=True,
    hover_data=['project_name'],
    title='<b>Creator Persona Quadrant:</b> Value vs. Volume',
    labels={'number_of_pledgers': 'Backer Volume', 'avg_amt$_per_pledger': 'Avg Pledge ($)'},
    template='plotly_white',
    color_continuous_scale=[(0, '#00CC96'), (0.33, '#636EFA'), (0.66, '#AB63FA'), (1, '#EF553B')]
)

fig_menu.add_vline(x=x_mid, line_width=3, line_color="RoyalBlue", opacity=1)
fig_menu.add_hline(y=y_mid, line_width=3, line_color="RoyalBlue", opacity=1)

fig_menu.update_layout(
    annotations=[
        dict(x=0.95, y=0.95, xref="paper", yref="paper", text="<b>STARS</b><br>High Value / High Volume", showarrow=False, font=dict(color="#00CC96", size=14)),
        dict(x=0.05, y=0.95, xref="paper", yref="paper", text="<b>BOUTIQUES</b><br>High Value / Low Volume", showarrow=False, font=dict(color="#636EFA", size=14)),
        dict(x=0.95, y=0.05, xref="paper", yref="paper", text="<b>PLOWHORSES</b><br>Low Value / High Volume", showarrow=False, font=dict(color="#AB63FA", size=14)),
        dict(x=0.05, y=0.05, xref="paper", yref="paper", text="<b>STRUGGLES</b><br>Low Value / Low Volume", showarrow=False, font=dict(color="#EF553B", size=14))
    ]
)

fig_menu.update_layout(coloraxis_showscale=False, title_x=0.5, height=700)
fig_menu.show()
"""
By using Average Pledge (Price) and Number of Pledgers (Popularity), you are showing the group exactly where the "profitability" lies.
Plowhorses (Bottom Right) are popular but cheap. They need to raise their "menu prices" (add higher reward tiers).
Boutiques (Top Left) are expensive but niche. They need better "marketing" (more backers) to become Stars.
"""