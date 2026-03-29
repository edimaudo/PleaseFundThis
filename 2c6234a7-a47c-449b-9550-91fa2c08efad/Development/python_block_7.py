####################
## Branding and anchor effect 
####################
from collections import Counter
import re
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