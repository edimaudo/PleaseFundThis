####################
## Social Proof signal
####################
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