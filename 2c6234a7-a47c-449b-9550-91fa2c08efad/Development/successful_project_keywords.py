####################
## Word cloud 
####################
from collections import Counter
import re
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