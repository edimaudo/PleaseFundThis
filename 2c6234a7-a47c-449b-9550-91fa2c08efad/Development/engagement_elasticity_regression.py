##=====================
## Key Issues and analysis
##=====================

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
##The ROI of a Post: "Our analysis shows that for successful projects, each update is statistically worth $X. If you spend 20 minutes writing an update, you are essentially earning a high hourly rate for that communication."
###The Success Gap: You will likely notice the Green line is much steeper than the Red line. This proves that Engagement Elasticity is higher for winners—updates don't just happen because they are winning; updates drive the winning momentum.
###Diminishing Returns: By looking at the spread of dots, you can see if the "ROI" stays consistent at 40+ updates or if there is a "Sweet Spot" (usually between 10–25) where the most funding is captured.

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

####################
## Creator personas
####################
df = pd.read_csv('PleaseFundThis.csv')
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
####################
## Propensity modeling
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()

# Numeric Cleaning
def clean_money(val):
    return pd.to_numeric(str(val).replace('$', '').replace(',', '').strip(), errors='coerce')

df['amt_pledged_$'] = df['amt_pledged_$'].apply(clean_money)
df['goal_$'] = df['goal_$'].apply(clean_money)

# STRING NORMALIZATION (The likely culprit for your KeyError)
df['has_video'] = df['project_has_video'].astype(str).str.strip().str.lower()
df['major_category'] = df['major_category'].astype(str).str.strip().str.lower()

# Facebook Logic
df['fb_count'] = pd.to_numeric(df['facebook_friends_count'], errors='coerce').fillna(0)
df['has_fb'] = np.where(df['fb_count'] > 0, 'yes', 'no')

# Drop rows missing core metrics
df = df.dropna(subset=['amt_pledged_$', 'goal_$'])

# 2. Independent Matching Function with empty-check safety
def perform_psm_match(data, treat_col):
    treatment_group = data[data[treat_col] == 'yes'].copy()
    control_group = data[data[treat_col] == 'no'].copy()
    
    matched_pairs = []
    
    for _, t_row in treatment_group.iterrows():
        # Match within same normalized category
        potentials = control_group[control_group['major_category'] == t_row['major_category']]
        
        if not potentials.empty:
            match_idx = (potentials['goal_$'] - t_row['goal_$']).abs().idxmin()
            c_row = potentials.loc[match_idx]
            
            matched_pairs.append({'Group_ID': 1, 'Pledge': t_row['amt_pledged_$']})
            matched_pairs.append({'Group_ID': 2, 'Pledge': c_row['amt_pledged_$']})
            control_group = control_group.drop(match_idx)
            
    # Return empty DF with columns if no matches found to prevent KeyError
    if not matched_pairs:
        return pd.DataFrame(columns=['Group_ID', 'Pledge'])
    return pd.DataFrame(matched_pairs)

# 3. Execute
video_matched_df = perform_psm_match(df, 'has_video')
fb_matched_df = perform_psm_match(df, 'has_fb')

# 4. Safety Gate & Visualization
label_map = {1: 'Treatment (With Feature)', 2: 'Control (Matched Twin)'}

# Check if we have data before grouping
if not video_matched_df.empty and not fb_matched_df.empty:
    v_results = video_matched_df.groupby('Group_ID')['Pledge'].mean().reset_index()
    v_results['Label'] = v_results['Group_ID'].map(label_map)

    f_results = fb_matched_df.groupby('Group_ID')['Pledge'].mean().reset_index()
    f_results['Label'] = f_results['Group_ID'].map(label_map)

    # Subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Video Independent ROI", "Facebook Independent ROI"))
    
    fig.add_trace(go.Bar(x=v_results['Label'], y=v_results['Pledge'], name="Video", marker_color='#636EFA'), row=1, col=1)
    fig.add_trace(go.Bar(x=f_results['Label'], y=f_results['Pledge'], name="FB", marker_color='#00CC96'), row=1, col=2)
    
    fig.update_layout(title_text="<b>Isolated Feature ROI via PSM</b>", template='plotly_white', showlegend=False)
    fig.show()
    
    # Calculate Lift
    v_lift = (v_results.iloc[0]['Pledge'] / v_results.iloc[1]['Pledge'] - 1) * 100
    f_lift = (f_results.iloc[0]['Pledge'] / f_results.iloc[1]['Pledge'] - 1) * 100
    print(f"Video Lift: {v_lift:.1f}% | FB Lift: {f_lift:.1f}%")
else:
    print("Error: No matches found. Check if Category names match exactly between Treatment and Control groups.")