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

####################
#### Category Bar Charts #####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
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

####################
#### Shows the largest platform communities by Category ####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
if df['number_of_pledgers'].dtype == 'object':
    df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'].str.replace(',', ''), errors='coerce')

# The hierarchy goes from the whole platform -> Major Category -> Minor Category
fig_treemap_pledge_count = px.treemap(
    df,
    path=[px.Constant("All Projects"), 'major_category', 'minor_category'], 
    values='number_of_pledgers',
    color='number_of_pledgers',
    color_continuous_scale='Viridis',
    title='Platform Community Size: Pledgers by Category'
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
#### Shows goal $ distribution by major category ####
####################
df = pd.read_csv('PleaseFundThis.csv')
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
    xaxis_title="Goal Amount (Log Scale)",
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
#### Goal $ Histogram ####
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df_filtered = df[(df['goal_$'] > 0) & (df['goal_$'] <= 100000)].copy()

fig_anchors = px.histogram(
    df_filtered, 
    x="goal_$", 
    nbins=500, # High bin count is CRITICAL to see the narrow spikes
    title='Psychological Anchoring: The "Round Number" Effect in Project Goals',
    labels={'goal_$': 'Funding Goal ($)'},
    template='plotly_white',
    color_discrete_sequence=['#636EFA']
)


fig_anchors.update_layout(
    title_x=0.5,
    xaxis_title="Funding Goal Amount ($)",
    yaxis_title="Frequency (Number of Projects)",
    bargap=0.1,
    xaxis=dict(
        tickvals=[0, 1000, 5000, 10000, 20000, 25000, 50000, 75000, 100000],
        tickformat='$,.0f',
        range=[0, 100000]
    )
)


fig_anchors.add_annotation(x=10000, yref='paper', y=0.9, text="The $10k Anchor", showarrow=True, arrowhead=1)
fig_anchors.add_annotation(x=5000, yref='paper', y=0.7, text="$5k Peak", showarrow=True, arrowhead=1)

fig_anchors.show()

####################
#### Word cloud ####
####################
from collections import Counter
import re
df = pd.read_csv('PleaseFundThis.csv')
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
    showlegend=False,
    height=700
)

fig_keywords.show()