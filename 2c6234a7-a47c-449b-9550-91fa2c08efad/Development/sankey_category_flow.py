##=====================
## Flow and Distribution
##=====================

####################
## Sankey chart major category 
####################

top_minors = df['minor_category'].value_counts().nlargest(30).index
df_filtered = df[df['minor_category'].isin(top_minors)].copy()
# Map outcomes to strings
df_filtered['outcome'] = df_filtered['project_success'].map({True: 'Successful', False: 'Failed'})
# Create Node List and Mapping
majors = sorted(df_filtered['major_category'].unique().tolist())
minors = sorted(df_filtered['minor_category'].unique().tolist())
outcomes = ['Successful', 'Failed']
label_list = majors + minors + outcomes
label_map = {label: i for i, label in enumerate(label_list)}

source_list = []
target_list = []
value_list = []
link_colors = []

# --- Layer 1: Major -> Minor ---
flow1 = df_filtered.groupby(['major_category', 'minor_category']).size().reset_index(name='count')
for _, row in flow1.iterrows():
    source_list.append(label_map[row['major_category']])
    target_list.append(label_map[row['minor_category']])
    value_list.append(row['count'])
    link_colors.append("rgba(200, 200, 200, 0.3)") # Neutral grey for the middle

# --- Layer 2: Minor -> Outcome ---
flow2 = df_filtered.groupby(['minor_category', 'outcome']).size().reset_index(name='count')
for _, row in flow2.iterrows():
    source_list.append(label_map[row['minor_category']])
    target_list.append(label_map[row['outcome']])
    value_list.append(row['count'])
    # Color the final path: Green for Success, Red for Failure
    if row['outcome'] == 'Successful':
        link_colors.append("rgba(0, 204, 150, 0.5)")
    else:
        link_colors.append("rgba(239, 85, 59, 0.5)")

fig_sankey = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 30,         # Increased padding makes nodes easier to click/hover
      thickness = 15,
      line = dict(color = "white", width = 2),
      label = label_list,
      color = "#333333" # Dark nodes for a professional "light mode" look
    ),
    link = dict(
      source = source_list,
      target = target_list,
      value = value_list,
      color = link_colors
    )
)])

fig_sankey.update_layout(
    title_text="<b>Project Flow: From Category to Success</b>",
    title_x=0.5,
    font=dict(size=12, color="black"),
    height=700,
    margin=dict(l=20, r=20, t=60, b=20), # Tight margins to maximize use of space
    template='plotly_white'
)

fig_sankey.show()