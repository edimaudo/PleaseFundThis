# Performance Trends and Comparisons

## Trend over time Month
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['date_launched'] = pd.to_datetime(df['date_launched'], errors='coerce')
df['Month'] = df['date_launched'].dt.month_name()
df['success_numeric'] = df['project_success'].astype(int)

# Group and calculate percent
seasonal_df = df.groupby('Month')['success_numeric'].mean().reset_index()
seasonal_df['Success_Rate_Pct'] = seasonal_df['success_numeric'] * 100

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# 2. Plotly Bar Chart
fig_monthly_bar = px.bar(
    seasonal_df, 
    x='Month', 
    y='Success_Rate_Pct',
    title='Seasonal Success: Which Months Win?',
    category_orders={'Month': month_order},
    color='Success_Rate_Pct',  # Colors bars by performance
    text_auto='.1f',           # Shows the % on top of the bars
    template='plotly_white',
    labels={'Success_Rate_Pct': 'Success Rate (%)'}
)

fig_monthly_bar.update_layout(title_x=0.5, showlegend=False,title_font_size=20,template='plotly_white')
fig_monthly_bar.show()

## Launch window bar chart day of week
# 3. Extract Day of Week
df['Day_of_Week'] = df['date_launched'].dt.day_name()

# 4. Aggregate
# We calculate the mean (success rate) for each day
day_df = df.groupby('Day_of_Week')['success_numeric'].mean().reset_index()
day_df['Success_Rate_Pct'] = day_df['success_numeric'] * 100

# Define standard week order
week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 5. Create Plotly Bar Chart
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

# 6. Styling
fig_daily.update_layout(
    title_font_size=20,
    title_x=0.5,
    showlegend=False,
    yaxis_range=[0, max(day_df['Success_Rate_Pct']) + 10]
)

fig_daily.show()

## Comparison between goal $ and amount pledged
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Clean currency columns
for col in ['goal_$', 'amt_pledged_$']:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[$,]', '', regex=True), errors='coerce')

# 2. Aggregate by Major Category
# We use MEDIAN to find the 'typical' experience for each category
df_cat = df.groupby('major_category').agg({
    'goal_$': 'median',
    'amt_pledged_$': 'median'
}).reset_index()

# Sort by Pledged amount for a cleaner "ladder" visual
df_cat = df_cat.sort_values('amt_pledged_$')

# 3. Build the Figure
fig_cat_dumbbell = go.Figure()

# Add the "Connector Lines"
for i, row in df_cat.iterrows():
    fig_cat_dumbbell.add_trace(go.Scatter(
        x=[row['goal_$'], row['amt_pledged_$']],
        y=[row['major_category'], row['major_category']],
        mode='lines',
        line=dict(color='lightgrey', width=4),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add the "Median Goal" dots (Red)
fig_cat_dumbbell.add_trace(go.Scatter(
    x=df_cat['goal_$'],
    y=df_cat['major_category'],
    mode='markers',
    name='Median Goal',
    marker=dict(color='#EF553B', size=14),
    hovertemplate="Typical Goal: $%{x:,.0f}<extra></extra>"
))

# Add the "Median Pledged" dots (Green)
fig_cat_dumbbell.add_trace(go.Scatter(
    x=df_cat['amt_pledged_$'],
    y=df_cat['major_category'],
    mode='markers',
    name='Median Pledged',
    marker=dict(color='#00CC96', size=14),
    hovertemplate="Typical Pledged: $%{x:,.0f}<extra></extra>"
))

# 4. Styling
fig_cat_dumbbell.update_layout(
    title='The "Funding Gap" by Category',
    xaxis_title='Amount ($) - Log Scale',
    yaxis_title=None,
    template='plotly_white',
      title_font_size=20,
    xaxis_type='log',
    height=700,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Set the log-scale ticks
fig_cat_dumbbell.update_xaxes(
    tickvals=[100, 1000, 10000, 100000],
    ticktext=['$100', '$1k', '$10k', '$100k']
)

fig_cat_dumbbell.show()

## analyze top 20 projects in a similar way
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
# Calculate the 'overfunding' amount and select Top 20 for readability
df['overfunding_gap'] = df['amt_pledged_$'] - df['goal_$']
top_20 = df.sort_values(by='overfunding_gap', ascending=False).head(20).copy()

# 2. Build the Figure
fig_dumbbell = go.Figure()

# Loop through each project to draw the "bar" part of the dumbbell
for i, row in top_20.iterrows():
    fig_dumbbell.add_shape(
        type='line',
        x0=row['goal_$'], y0=row['project_name'],
        x1=row['amt_pledged_$'], y1=row['project_name'],
        line=dict(color='lightgrey', width=3)
    )

# 3. Add the "Goal" dots (Red)
fig_dumbbell.add_trace(go.Scatter(
    x=top_20['goal_$'],
    y=top_20['project_name'],
    mode='markers',
    name='Goal',
    marker=dict(color='#EF553B', size=12, symbol='circle'),
    hovertemplate="<b>%{y}</b><br>Goal: $%{x:,.0f}<extra></extra>"
))

# 4. Add the "Pledged" dots (Green)
fig_dumbbell.add_trace(go.Scatter(
    x=top_20['amt_pledged_$'],
    y=top_20['project_name'],
    mode='markers',
    name='Pledged Amount',
    marker=dict(color='#00CC96', size=12, symbol='circle'),
    hovertemplate="<b>%{y}</b><br>Pledged: $%{x:,.0f}<extra></extra>"
))

# 5. Styling
fig_dumbbell.update_layout(
    title='Magnitude of Overfunding: Top 20 Most Successful Projects',
    title_x=0.5,
    xaxis_title='Funding Amount ($) - Log Scale',
    yaxis_title=None,
    template='plotly_white',
    xaxis_type='log', # Log scale allows us to see different orders of magnitude
    height=800,
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Optional: Add clear log-scale ticks
fig_dumbbell.update_xaxes(
    tickvals=[10, 100, 1000, 10000, 100000, 1000000],
    ticktext=['$10', '$100', '$1k', '$10k', '$100k', '$1M']
)

fig_dumbbell.show()
