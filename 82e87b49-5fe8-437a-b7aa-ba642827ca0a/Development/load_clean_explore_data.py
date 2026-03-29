## Load data
# ## Load data
df = pd.read_csv('PleaseFundThis.csv')
# # Clean column names immediately 
df.columns = df.columns.str.strip()
#check data
print(df.head())
print(" ")
#summary
print(df.describe())
# Get column Names
print(" ")
print(df.columns.tolist())
# Remove unames columns
df = df.drop(['Unnamed: 23','Unnamed: 24','Unnamed: 25','Unnamed: 26','Unnamed: 27','Unnamed: 28','Unnamed: 29'], axis=1) #drop unnamed columns
print(" ")
# Check data types
print(df.dtypes)
print(" ")
# # Remove rows with missing values
# df = df.dropna()
print(" ")
# Display basic statistics
print(df.info())
# Check for missing values
print(df.isnull().sum())
print(" ")
# Display missing values as percentage
print((df.isnull().sum() / len(df) * 100).round(2))
# # Date update
# df['date_launched'] = pd.to_datetime(df['date_launched'], dayfirst=True)
# # Use the correct method to get the day name
# df['week_name'] = df['date_launched'].dt.day_name()
# df['year'] = df['date_launched'].dt.year
# df['month_name'] = df['date_launched'].dt.month_name()