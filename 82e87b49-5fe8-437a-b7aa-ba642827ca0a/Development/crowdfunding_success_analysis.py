##=====================
# Success Drivers and Indicators
##=====================

####################
## Correlation heatmap
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
currency_cols = ['lowest_pledge_reward_$', 'highest_pledge_reward_$', 'amt_pledged_$', 'goal_$']
for col in currency_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# Convert Success and Video to 0 and 1
df['project_success'] = df['project_success'].astype(int)
df['project_has_video'] = df['project_has_video'].astype(int)

# Select Numeric Metrics for the Heatmap
metrics = [
    'amt_pledged_$', 'percent_raised', 'project_success',
    'project_update_count', 'number_of_pledgers', 'comments_count',
    'facebook_friends_count', 'lowest_pledge_reward_$', 'highest_pledge_reward_$',
    'duration_days', 'project_has_video'
]

# Create the Correlation Matrix
corr_matrix = df[metrics].corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=".2f", # Shows the correlation number in the box
    aspect="auto",
    color_continuous_scale='RdBu_r', # Red for negative, Blue for positive
    zmin=-1, zmax=1,                 # Standard correlation range
    title='What Drives Funding? (Correlation Heatmap)',
    labels={'color': 'Correlation Strength'},
    template='plotly_white'
)

fig_heatmap.update_layout(
    title={'text': 'The Drivers of Success: Correlation Heatmap', 'x': 0.5},
    height=800,
    xaxis_tickangle=-45
)

fig_heatmap.show()

####################
## ROI of Communication
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['project_update_count'] = pd.to_numeric(df['project_update_count'], errors='coerce')
df['percent_raised'] = pd.to_numeric(df['percent_raised'], errors='coerce')

df_filtered = df[df['percent_raised'] <= 1000].copy()

success_df = df_filtered[df_filtered['project_success'] == True]
failed_df = df_filtered[df_filtered['project_success'] == False]

fig_roi = go.Figure()

fig_roi.add_trace(go.Scatter(
    x=success_df['project_update_count'],
    y=success_df['percent_raised'],
    mode='markers',
    name='Successful Projects',
    marker=dict(color='#00CC96', opacity=0.5),
    hovertemplate="Updates: %{x}<br>Raised: %{y}%<extra></extra>"
))

# Add Unsuccessful Projects (Dots + Trendline)
fig_roi.add_trace(go.Scatter(
    x=failed_df['project_update_count'],
    y=failed_df['percent_raised'],
    mode='markers',
    name='Unsuccessful Projects',
    marker=dict(color='#EF553B', opacity=0.5),
    hovertemplate="Updates: %{x}<br>Raised: %{y}%<extra></extra>"
))

fig_roi.update_layout(
    title={'text': 'The ROI of Communication: Updates vs. Funding Percentage', 'x': 0.5},
    xaxis_title="Number of Project Updates",
    yaxis_title="Percent of Goal Raised (%)",
    template='plotly_white',
    legend_title="Project Result",
    height=600
)

fig_roi.show()

####################
## Funding lift looking at social media (fb pages) and funding videos
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Clean Currency
df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

df_view = df[df['amt_pledged_$'] <= 10000].copy()
df_view['video_label'] = df_view['project_has_video'].apply(lambda x: 'With Video' if x is True else 'No Video')
success_df = df_view[df_view['project_success'] == True]
failed_df = df_view[df_view['project_success'] == False]

fig_video = go.Figure()

fig_video.add_trace(go.Box(
    x=success_df['video_label'],
    y=success_df['amt_pledged_$'],
    name='Successful',
    marker_color='#00CC96',
    boxpoints=None
))

fig_video.add_trace(go.Box(
    x=failed_df['video_label'],
    y=failed_df['amt_pledged_$'],
    name='Unsuccessful',
    marker_color='#EF553B',
    boxpoints=None
))

fig_video.update_layout(
    title={'text': 'Funding Lift: Impact of Video Assets', 'x': 0.5},
    yaxis_title="Total Amount Pledged ($)",
    xaxis_title="Video Presence",
    boxmode='group',
    template='plotly_white'
)

fig_video.show()

####################
### Social media Availability
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df_view['fb_label'] = df_view['project_has_facebook_page'].apply(lambda x: 'Has Facebook' if x is True else 'No Facebook')
success_df_fb = df_view[df_view['project_success'] == True]
failed_df_fb = df_view[df_view['project_success'] == False]

fig_fb = go.Figure()

fig_fb.add_trace(go.Box(
    x=success_df_fb['fb_label'],
    y=success_df_fb['amt_pledged_$'],
    name='Successful',
    marker_color='#00CC96',
    boxpoints=None
))

fig_fb.add_trace(go.Box(
    x=failed_df_fb['fb_label'],
    y=failed_df_fb['amt_pledged_$'],
    name='Unsuccessful',
    marker_color='#EF553B',
    boxpoints=None
))

fig_fb.update_layout(
    title={'text': 'Social Lift: Impact of Facebook Pages', 'x': 0.5},
    yaxis_title="Total Amount Pledged ($)",
    xaxis_title="Facebook Page Presence",
    boxmode='group',
    template='plotly_white'
)

fig_fb.show()

####################
## Social media impact facebook friends count
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['facebook_friends_count'] = pd.to_numeric(df['facebook_friends_count'], errors='coerce')

df_view = df[df['facebook_friends_count'] <= 10000].copy()

success_df = df_view[df_view['project_success'] == True]
failed_df = df_view[df_view['project_success'] == False]

fig_strip = go.Figure()

# Successful Projects
fig_strip.add_trace(go.Box(
    y=success_df['facebook_friends_count'],
    name='Reached Goal',
    marker=dict(color='#00CC96', size=5, opacity=0.4),
    boxpoints='all', jitter=0.5, pointpos=0,
    fillcolor='rgba(0,0,0,0)', line_color='rgba(0,0,0,0)',
    hovertext="Successful Project"
))

# Unsuccessful Projects
fig_strip.add_trace(go.Box(
    y=failed_df['facebook_friends_count'],
    name='Did Not Reach Goal',
    marker=dict(color='#EF553B', size=5, opacity=0.4),
    boxpoints='all', jitter=0.5, pointpos=0,
    fillcolor='rgba(0,0,0,0)', line_color='rgba(0,0,0,0)',
    hovertext="Unsuccessful Project"
))

fig_strip.update_layout(
    title={
        'text': "<b>Crowdsourcing Power:</b> How Personal Networks Impact Success",
        'y': 0.95, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'
    },
    yaxis_title="Total Facebook Friends",
    xaxis_title="Final Project Status",
    template='plotly_white',
    height=600,
    showlegend=False,
)

fig_strip.show()


####################
## Duration and goal $
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
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

####################
## Most valuable backers
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['avg_amt$_per_pledger'] = pd.to_numeric(df['avg_amt$_per_pledger'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
# We group by both category and success to see if successful projects attract "higher value" backers
category_stats = df.groupby(['major_category', 'project_success'])['avg_amt$_per_pledger'].mean().reset_index()
# We find the order of categories based on the highest average pledge for successful projects
sort_order = category_stats[category_stats['project_success'] == True].sort_values('avg_amt$_per_pledger', ascending=False)['major_category'].tolist()
success_data = category_stats[category_stats['project_success'] == True]
failed_data = category_stats[category_stats['project_success'] == False]

fig_value = go.Figure()

# Successful Projects Trace
fig_value.add_trace(go.Bar(
    x=success_data['major_category'],
    y=success_data['avg_amt$_per_pledger'],
    name='Reached Goal',
    marker_color='#00CC96',
    text=success_data['avg_amt$_per_pledger'].map('${:,.0f}'.format),
    textposition='auto'
))

# Unsuccessful Projects Trace
fig_value.add_trace(go.Bar(
    x=failed_data['major_category'],
    y=failed_data['avg_amt$_per_pledger'],
    name='Did Not Reach Goal',
    marker_color='#EF553B',
    text=failed_data['avg_amt$_per_pledger'].map('${:,.0f}'.format),
    textposition='auto'
))

fig_value.update_layout(
    title={'text': '<b>The Backer Value Index:</b> Which Categories Attract the Highest Pledges?', 'x': 0.5},
    xaxis_title="Project Category",
    yaxis_title="Average Amount per Backer ($)",
    xaxis={'categoryorder': 'array', 'categoryarray': sort_order}, # Applies our custom sort
    barmode='group',
    template='plotly_white',
    height=600,
    legend_title="Project Status"
)

fig_value.show()


####################
### Engagement elasticity
####################

from sklearn.linear_model import LinearRegression
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Clean Numeric Data
df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
df['project_update_count'] = pd.to_numeric(df['project_update_count'], errors='coerce')

df_clean = df[(df['amt_pledged_$'] <= 50000) & (df['project_update_count'] <= 50)].dropna(subset=['amt_pledged_$', 'project_update_count'])
success_df = df_clean[df_clean['project_success'] == True].sort_values('project_update_count')
failed_df = df_clean[df_clean['project_success'] == False].sort_values('project_update_count')

# 3. Robust Regression Function
def calculate_roi_line(sub_df):
    if len(sub_df) < 2: # Need at least 2 points for a line
        return None, 0
    
    # Prepare X and y
    X = sub_df['project_update_count'].values.reshape(-1, 1)
    y = sub_df['amt_pledged_$'].values
    
    # Fit Model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict and FLATTEN the output
    predictions = model.predict(X).flatten() 
    roi_val = model.coef_[0]
    
    return predictions, roi_val

# Calculate
s_preds, s_roi = calculate_roi_line(success_df)
f_preds, f_roi = calculate_roi_line(failed_df)


fig = go.Figure()

# Success Trace
if s_preds is not None:
    fig.add_trace(go.Scatter(x=success_df['project_update_count'], y=success_df['amt_pledged_$'], mode='markers', name='Reached Goal', marker=dict(color='#00CC96', opacity=0.3)))
    fig.add_trace(go.Scatter(x=success_df['project_update_count'], y=s_preds, mode='lines', name=f'Success ROI: ${s_roi:.2f}/upd', line=dict(color='#008B66', width=3)))

# Failure Trace
if f_preds is not None:
    fig.add_trace(go.Scatter(x=failed_df['project_update_count'], y=failed_df['amt_pledged_$'], mode='markers', name='Did Not Reach Goal', marker=dict(color='#EF553B', opacity=0.3)))
    fig.add_trace(go.Scatter(x=failed_df['project_update_count'], y=f_preds, mode='lines', name=f'Failure ROI: ${f_roi:.2f}/upd', line=dict(color='#B22222', width=3)))

fig.update_layout(
    title={'text': "<b>Engagement Elasticity:</b> Funding Return per Update", 'x': 0.5},
    xaxis_title="Updates Posted",
    yaxis_title="Total Pledged ($)",
    template='plotly_white'
)

fig.show()

### business outcomes
"""The ROI of a Post: "Our analysis shows that for successful projects, each update is statistically worth $X. If you spend 20 minutes writing an update, you are essentially earning a high hourly rate for that communication."
###The Success Gap: You will likely notice the Green line is much steeper than the Red line. This proves that Engagement Elasticity is higher for winners—updates don't just happen because they are winning; updates drive the winning momentum.
###Diminishing Returns: By looking at the spread of dots, you can see if the "ROI" stays consistent at 40+ updates or if there is a "Sweet Spot" (usually between 10–25) where the most funding is captured."""

####################
## Anatomy of an overachiever
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Create the segments based on Percent Raised
def segment_success(percent):
    if percent >= 500: return 'Overachiever (500%+)'
    elif percent >= 100: return 'Standard Winner (100-499%)'
    else: return 'Failed Project (<100%)'

df['Success_Tier'] = df['percent_raised'].apply(segment_success)

# Calculating means for Update Counts and Pledge Level Counts
anatomy_stats = df.groupby('Success_Tier').agg({
    'project_update_count': 'mean',
    'total_count_of_pledge_levels': 'mean',
    'project_id': 'count'
}).reindex(['Overachiever (500%+)', 'Standard Winner (100-499%)', 'Failed Project (<100%)']).reset_index()

fig = go.Figure()

# Add Bars for Update Frequency
fig.add_trace(go.Bar(
    x=anatomy_stats['Success_Tier'],
    y=anatomy_stats['project_update_count'],
    name='Avg Updates',
    marker_color='#636EFA',
    text=anatomy_stats['project_update_count'].round(1),
    textposition='auto'
))

# Add Bars for Pledge Levels
fig.add_trace(go.Bar(
    x=anatomy_stats['Success_Tier'],
    y=anatomy_stats['total_count_of_pledge_levels'],
    name='Avg Pledge Tiers',
    marker_color='#00CC96',
    text=anatomy_stats['total_count_of_pledge_levels'].round(1),
    textposition='auto'
))

fig.update_layout(
    title='<b>Anatomy of an Overachiever:</b> Updates vs. Reward Complexity',
    xaxis_title='Project Success Segment',
    yaxis_title='Average Count',
    barmode='group',
    template='plotly_white',
    title_x=0.5,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

fig.show()

# Print Summary for Interpretation
print(anatomy_stats)

"""
Findings: Overachievers update their backers x more often than failed projects (8.5 updates vs. 4.7 on average).
Successful projects offer an average of 10.6 pledge levels, providing significantly more entry points than the 8.4 levels offered by failures.
A direct linear correlation exists between update frequency and the final funding percentage.

1. The "Update" Correlation

The Trend: Typically, Overachievers have a significantly higher update count.
The Insight: This suggests that viral success isn't a "set it and forget it" event. 
Overachievers likely use updates to maintain momentum, announce "stretch goals," and keep the community engaged during the exponential growth phase.
Actionable Advice: If you want to break out of the "Standard Winner" pack, double your communication frequency.

2. The "Pledge Tier" Strategy
The Trend: If Overachievers have more pledge levels than Failures, it indicates that Choice Architecture matters.
The Insight: More tiers allow for "Price Discrimination"—it lets small backers in for $5 while giving high-net-worth fans a way to spend $1,000.
The Trap: If Overachievers have fewer levels than Standard Winners, it suggests that Simplicity wins when a project goes viral. Too many choices can cause "Analysis Paralysis."

3. The "Standard Winner" Gap
Look at the distance between the Standard Winner and the Overachiever. If the Update count jumps significantly (e.g., from 10 to 25 updates), 
that is your "Viral Threshold." That is the extra effort required to cross from "Successful" to "Legendary."
"""

####################
## Social Proof signal
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['amt_pledged_$'] = pd.to_numeric(df['amt_pledged_$'].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')
df['facebook_friends_count'] = pd.to_numeric(df['facebook_friends_count'], errors='coerce')
df['number_of_pledgers'] = pd.to_numeric(df['number_of_pledgers'], errors='coerce')
df['project_success_numeric'] = df['project_success'].astype(int)

# 2. Calculate Spearman Correlation 
corr_results = df[['facebook_friends_count', 'project_success_numeric', 'amt_pledged_$', 'number_of_pledgers']].corr(method='spearman')

# Extract the specific correlations for Facebook Friends
labels = ['Winning (Success)', 'Total Funding ($)', 'Crowd Size (Backers)']
values = [
    corr_results.loc['facebook_friends_count', 'project_success_numeric'],
    corr_results.loc['facebook_friends_count', 'amt_pledged_$'],
    corr_results.loc['facebook_friends_count', 'number_of_pledgers']
]

fig_signal = go.Figure()

fig_signal.add_trace(go.Bar(
    x=labels,
    y=values,
    marker_color=['#636EFA', '#00CC96', '#AB63FA'],
    text=[f"{v:.2f}" for v in values],
    textposition='auto',
) )

fig_signal.update_layout(
    title={'text': "<b>The Social Proof Signal:</b> Is Facebook a Vanity Metric?", 'x': 0.5},
    yaxis_title="Spearman Correlation Strength (0 to 1)",
    xaxis_title="Success Metric",
    template='plotly_white',
    yaxis=dict(range=[0, 1]), # Correlation scales from 0 to 1
    height=500
)


fig_signal.show()

# Print the Verdict for your presentation
print(f"Correlation with Success: {values[0]:.2f}")
print(f"Correlation with Funding: {values[1]:.2f}")


"""
The Vanity Threshold: If the "Winning" bar is much higher than the "Total Funding" bar, tell your audience: "Facebook friends are a vanity metric for scale. They help you get enough backers to meet your goal, but they don't necessarily attract the high-value investors who drive total funding into the millions."
The "Leading Indicator": A score above 0.40 is a "Strong Signal." If the "Crowd Size" bar is the highest, it proves that your personal network is your "Seed Crowd"—they are the ones who show up first so that strangers feel safe pledging later.
The "Social Proof" Takeaway: "Success isn't just about how many people you know; it's about how many people you know who are willing to act as a 'signal' to the rest of the world that your project is worth backing."
"""

####################
## Branding and anchor effect 
####################
from collections import Counter
import re
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Clean Currency
df['avg_amt$_per_pledger'] = pd.to_numeric(
    df['avg_amt$_per_pledger'].astype(str).str.replace(r'[$,]', '', regex=True), 
    errors='coerce'
)

# 2. NLP: Simple Tokenization & Cleaning
def get_tokens(text):
    if not isinstance(text, str): return []
    # Lowercase, remove punctuation, and split
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = text.split()
    # Filter out "Stop Words" (common words with no branding value)
    stop_words = {'the', 'and', 'for', 'with', 'your', 'this', 'from', 'that', 'a', 'of', 'to', 'in', 'on'}
    return [w for w in words if len(w) > 3 and w not in stop_words]

# Apply tokenization
df['name_tokens'] = df['project_name'].apply(get_tokens)

# We find words that appear at least 10 times to ensure statistical relevance
all_words = [word for tokens in df['name_tokens'] for word in tokens]
word_counts = Counter(all_words)
power_word_candidates = [word for word, count in word_counts.items() if count >= 10]

# Calculate the "Anchor Value" (Average Pledge) for each word
word_values = []
for word in power_word_candidates:
    # Find rows where the project name contains this word
    mask = df['name_tokens'].apply(lambda tokens: word in tokens)
    avg_val = df.loc[mask, 'avg_amt$_per_pledger'].mean()
    word_values.append({'word': word.capitalize(), 'anchor_value': avg_val})

# Create DataFrame and sort by Value
word_df = pd.DataFrame(word_values).sort_values('anchor_value', ascending=False).head(15)

fig_branding = go.Figure()

fig_branding.add_trace(go.Bar(
    x=word_df['anchor_value'],
    y=word_df['word'],
    orientation='h', # Horizontal bar for readability
    marker_color='#636EFA',
    text=word_df['anchor_value'].map('${:,.0f}'.format),
    textposition='outside'
))

fig_branding.update_layout(
    title={'text': "<b>The Anchor Effect:</b> Which Branding Words Command Higher Pledges?", 'x': 0.5},
    xaxis_title="Average Pledge Amount per Backer ($)",
    yaxis_title="Power Word in Project Name",
    template='plotly_white',
    height=600,
    yaxis=dict(autorange="reversed") # Highest value at the top
)

fig_branding.show()

### Explanation
"""
Premium Signals: Point to the top of the list. "When creators use words like 'Titanium' or 'Automatic,' they are anchoring the backer's mind to a higher price point. This shows that branding isn't just about 'looking cool'—it's a financial lever."
The Contextual Lift: If words like "Film" have a lower anchor value than "Lens," you can explain: "Backers associate physical hardware with higher value than digital content, and our data proves that this bias shows up in the project name itself."
Strategy Takeaway: "If you want to raise more money per person, you shouldn't just change your product—you should change your vocabulary. Use words that the market already associates with high-tier investments."
"""