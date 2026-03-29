##=====================
# Predictive Modeling
##=====================
df = pd.read_csv('PleaseFundThis.csv')
# Clean column names immediately 
df.columns = df.columns.str.strip()
# Date update
df['date_launched'] = pd.to_datetime(df['date_launched'], dayfirst=True)
# Use the correct method to get the day name
df['week_name'] = df['date_launched'].dt.day_name()
df['year'] = df['date_launched'].dt.year
df['month'] = df['date_launched'].dt.month
# Remove unames columns
df = df.drop(['Unnamed: 23','Unnamed: 24','Unnamed: 25','Unnamed: 26','Unnamed: 27','Unnamed: 28','Unnamed: 29'], axis=1) #drop unnamed columns
# drop facebook friends count
df = df.drop('facebook_friends_count',axis=1)
# drop city, drop minor category, project id and name, percent raised,
df = df.drop(['minor_category','project_id','project_name','percent_raised'],axis=1)
# drop date launched column
df = df.drop(['date_launched'],axis=1)
# drop city
df = df.drop('city',axis=1)
# check for target ratio
df['project_success'].value_counts().plot.bar()
# recode target variable 'project_has_video','project_has_facebook_page','project_has_pledge_rewards'
df['project_success'] = df['project_success'].replace({False: 0, True: 1, "FALSE": 0, "TRUE": 1})
df['project_has_video'] = df['project_has_video'].replace({False: 0, True: 1, "FALSE": 0, "TRUE": 1})
df['project_has_facebook_page'] = df['project_has_facebook_page'].replace({"No": 0, "Yes": 1})
df['project_has_pledge_rewards'] = df['project_has_pledge_rewards'].replace({"No": 0, "Yes": 1})
# split categorical variables
df_cat = df[['major_category','region','week_name']]
df_cat = pd.get_dummies(df_cat, columns=['major_category','region','week_name'], drop_first=False)
# cts
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


df_cts = df_cts.reset_index(drop=True)
df_cat = df_cat.reset_index(drop=True)
target_col = df['project_success'].astype(int).reset_index(drop=True)
df_final = pd.concat([df_cts, df_cat, target_col], axis=1)
train = df_final.sample(frac=0.8, random_state=200)
test = df_final.drop(train.index)

# 4. Features & Target
features = train.drop('project_success', axis=1)
target = train['project_success']

models = {
    #'Logistic Regression': LogisticRegression(random_state=22, C=1e-9, solver='liblinear', max_iter=200),
    #'Naive Bayes': GaussianNB(),
    'Random Forest': RandomForestClassifier(n_estimators=200, random_state=22),
    'Gradient Boosting': GradientBoostingClassifier(n_estimators=200),
    #'KNN': KNeighborsClassifier(),
    'Decision Tree': DecisionTreeClassifier(),
    #'LDA': LinearDiscriminantAnalysis(),
    'Bagging Classifier': BaggingClassifier()
}

# Create Ensemble
#ensemble_members = [(name.lower()[:2], m) for name, m in models.items()]
#models['Ensemble'] = VotingClassifier(estimators=ensemble_members, voting='hard')

# 6. Execution Loop
print(f"{'Model':<25} | {'Accuracy':<10}")
print("-" * 40)

for label, model in models.items():
    # cv=5 and scoring='accuracy'
    scores = cross_val_score(model, features, target, cv=5, scoring='accuracy')
    mean_score = scores.mean()
    print(f"{label:<25} | {mean_score:.4f}")

## testing
test_features = test.drop('project_success', axis=1)
test_target = test['project_success'].astype(int)
print(" ")
print(f"{'Model':<20} | {'Test Accuracy':<15} | {'Avg Precision':<15}")
print("-" * 55)



for name, model in models.items():
    # Fit the model using the training features and target
    model.fit(features, target)
    
    # Predict on the test set
    pred = model.predict(test_features)
    
    # Calculate Metrics
    acc = accuracy_score(test_target, pred)
    avg_prec = average_precision_score(test_target, pred)
    
    print(f"{name:<20} | {acc:.4f}          | {avg_prec:.4f}")

print(" ")
print("Confusion Matrix:")
print(confusion_matrix(test_target, pred))
print(" ")
print(" ")
print("\nClassification Report:")
print(classification_report(test_target, pred))