##=====================
## Category and Markets
##=====================

####################
## Category Treemap
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
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

####################
## Major Category Ranking
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
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

####################
## Minor Category Ranking
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
minor_ranked = df.groupby('minor_category')['amt_pledged_$'].sum().reset_index()
minor_ranked = minor_ranked.sort_values('amt_pledged_$', ascending=False)

fig_minor = px.bar(
    minor_ranked,
    x='amt_pledged_$',
    y='minor_category',
    orientation='h',
    title='Pledge Amount by Minor Category',
    labels={'amt_pledged_$': 'Pledged Amount ($)', 'minor_category': 'Minor Category'},
    color='amt_pledged_$',
    color_continuous_scale='viridis',
    text_auto='.2s'
)

fig_minor.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False,template='plotly_white', margin=dict(l=10, r=10, t=40, b=10),
        title_font_size=20, title_x=0.5, height=400)
fig_minor.show()

####################
## Pledgers by Category 
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
if df['number_of_pledgers'].dtype == 'object':
    df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'].str.replace(',', ''), errors='coerce')

fig_treemap_pledge_count = px.treemap(
    df,
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='number_of_pledgers',
    color='number_of_pledgers',
    color_continuous_scale='Viridis',
    title='Pledgers by Category'
)

fig_treemap_pledge_count.update_traces(
    textinfo="label+value",
    hovertemplate='<b>%{label}</b><br>Total Pledgers: %{value:,.0f}<extra></extra>'
)

fig_treemap_pledge_count.update_layout(
    margin=dict(t=80, l=10, r=10, b=10),
    title_x=0.5,
    title_font_size=20,
    coloraxis_colorbar=dict(title="Pledgers")
)

fig_treemap_pledge_count.show()

####################
## Goal $ distribution by major category 
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
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
    xaxis_title="Funding Goal Amount ($)",
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

####################
## Goal $ Histogram 
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
df_filtered = df[(df['goal_$'] > 0) & (df['goal_$'] <= 100000)].copy()

fig_anchors = px.histogram(
    df_filtered, 
    x="goal_$", 
    nbins=500, # High bin count is CRITICAL to see the narrow spikes
    title='Funding Goal Target Amount Distribution',
    labels={'goal_$': 'Funding Goal ($)'},
    template='plotly_white',
    color_discrete_sequence=['#636EFA']
)


fig_anchors.update_layout(
    title_x=0.5,
    xaxis_title="Funding Goal Amount ($)",
    yaxis_title="Number of Projects",
    bargap=0.1,
    xaxis=dict(
        tickvals=[0, 1000, 5000, 10000, 20000, 25000, 50000, 75000, 100000],
        tickformat='$,.0f',
        range=[0, 100000]
    )
)


fig_anchors.add_annotation(x=10000, yref='paper', y=0.9, text="The $10k Peak", showarrow=True, arrowhead=1)
fig_anchors.add_annotation(x=5000, yref='paper', y=0.7, text="$5k Peak", showarrow=True, arrowhead=1)

fig_anchors.show()

####################
## Word cloud 
####################
from collections import Counter
import re
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
successful_titles = df[df['project_success'] == True]['project_name'].astype(str).str.lower()
# Define common "Stopwords" to filter out (the, and, for, etc.)
stopwords = {'the', 'and', 'for', 'your', 'with', 'from', 'this', 'that', 'project', 'new', 'help', 'make'}

all_words = []
for title in successful_titles:
    # Remove special characters and split into words
    words = re.findall(r'\w+', title)
    all_words.extend([w for w in words if w not in stopwords and len(w) > 2])
word_counts = Counter(all_words).most_common(25)
df_words = pd.DataFrame(word_counts, columns=['Keyword', 'Frequency'])
fig_keywords = px.bar(
    df_words, 
    x='Frequency', 
    y='Keyword', 
    orientation='h',
    title='Keywords of Success: Top Terms in Funded Project Titles',
    color='Frequency',
    color_continuous_scale='Viridis',
    template='plotly_white'
)

fig_keywords.update_layout(
    yaxis={'categoryorder':'total ascending'}, 
    title_x=0.5,
    xaxis_title="Keyword Count",
    height=700
)



fig_keywords.show()

####################
## City Success
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
df['city'] = df['city'].astype(str).str.strip().str.title()
df['is_success'] = pd.to_numeric(df['project_success'], errors='coerce').fillna(0).astype(bool)
if df['is_success'].sum() == 0:
    df['is_success'] = df['project_success'].astype(str).str.strip().str.upper() == 'TRUE'

# Calculate metrics
city_stats = df.groupby('city')['is_success'].agg(['sum', 'count']).reset_index()
city_stats.columns = ['City', 'Successes', 'Total_Outcomes']
city_stats['Success Rate'] = (city_stats['Successes'] / city_stats['Total_Outcomes']) * 100
top_cities = city_stats[city_stats['Total_Outcomes'] >= 10].sort_values('Success Rate', ascending=False)

fig_geo = px.bar(
    top_cities.head(20), 
    x='Success Rate',      # Move numeric value to x
    y='City',              # Move category to y
    color='Success Rate',
    orientation='h',       # Explicitly set horizontal orientation
    text_auto='.1f',
    title='<b>Cities by Success Rate</b>',
    labels={'Success Rate': 'Success Rate (%)', 'City': 'Location'},
    color_continuous_scale='viridis',
    template='plotly_white'
)

fig_geo.update_layout(
    title_x=0.5,
    yaxis={'categoryorder':'total ascending'} # Keeps the highest rate at the top
)

fig_geo.show()

####################
## Creator personas
####################
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
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
    title='<b>Creator Persona</b> Value vs. Volume',
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