##=====================
# Performance Trends and Comparisons
##=====================

####################
## Trend over time Month
####################
df = pd.read_csv('PleaseFundThis.csv')
df.columns = df.columns.str.strip()
df['date_launched'] = pd.to_datetime(df['date_launched'], errors='coerce')
df['Month'] = df['date_launched'].dt.month_name()
df['success_numeric'] = df['project_success'].astype(int)

seasonal_df = df.groupby('Month')['success_numeric'].mean().reset_index()
seasonal_df['Success_Rate_Pct'] = seasonal_df['success_numeric'] * 100

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

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