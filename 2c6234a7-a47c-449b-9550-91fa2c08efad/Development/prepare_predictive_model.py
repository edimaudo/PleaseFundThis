# Predictive Modeling
#drop facebook friends count
df = df.drop('facebook_friends_count',axis=1)

#drop city, drop minor category, project id and name, percent raised,
df = df.drop(['minor_category','project_id','project_name','percent_raised'],axis=1)

#drop date launched column
df = df.drop(['date_launched','week_name','year','month'],axis=1)

#check for target ratio
pd.value_counts(df['project_success']).plot.bar()

#recode target variable
df["project_success"].replace({False: 0, True: 1}, inplace=True)

#recode 'project_has_video','project_has_facebook_page','project_has_pledge_rewards'
df['project_has_video'].replace({False: 0, True: 1}, inplace=True)
df['project_has_facebook_page'].replace({"No": 0, "Yes": 1}, inplace=True)
df['project_has_pledge_rewards'].replace({"No": 0, "Yes": 1}, inplace=True)

#drop city
df = df.drop('city',axis=1)

#split categorical variables
df_cat = df[['major_category','region','week_name']]
df_cat = pd.get_dummies(df_cat, columns=['major_category','region','week_name'], drop_first=False)
df_cat.reset_index(drop=True, inplace=True)

#cts
scaler = preprocessing.MinMaxScaler()
df_cts = df[['duration_days',
 'goal_$',
 'amt_pledged_$',
 'project_update_count',
 'number_of_pledgers',
 'comments_count',
 'project_has_video',
 'project_has_facebook_page',
 'project_has_pledge_rewards',
 'year',
 'month']] 
df_cts = scaler.fit_transform(df_cts)
df_cts = pd.DataFrame(df_cts, columns=['duration_days',
 'goal_$',
 'amt_pledged_$',
 'project_update_count',
 'number_of_pledgers',
 'comments_count',
 'project_has_video',
 'project_has_facebook_page',
 'project_has_pledge_rewards',
 'year',
 'month'])
df_cts.reset_index(drop=True, inplace=True)

df['project_success'].reset_index(drop=True, inplace=True)

#combine
df = pd.concat([df_cts, df_cat,df['project_success']], axis=1)

train=df.sample(frac=0.8,random_state=200) #random state is a seed value
test=df.drop(train.index)
print("")
print(df.shape)