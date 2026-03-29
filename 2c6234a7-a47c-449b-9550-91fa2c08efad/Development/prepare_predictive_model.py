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
df_cat.reset_index(drop=True, inplace=True)
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
df_cts.reset_index(drop=True, inplace=True)

df['project_success'].reset_index(drop=True, inplace=True)

# combine
df = pd.concat([df_cts, df_cat,df['project_success']], axis=1)
print(df.shape)
train=df.sample(frac=0.8,random_state=200) # random state is a seed value
test=df.drop(train.index)
# train
features=train.iloc[:,0:166]
target = train['project_success']
Name=[]
Accuracy=[]
model1=LogisticRegression(random_state=22,C=0.000000001,solver='liblinear',max_iter=200)
model2=GaussianNB()
model3=RandomForestClassifier(n_estimators=200,random_state=22)
model4=GradientBoostingClassifier(n_estimators=200)
model5=KNeighborsClassifier()
model6=DecisionTreeClassifier()
model7=LinearDiscriminantAnalysis()
model8=BaggingClassifier()
Ensembled_model=VotingClassifier(estimators=[('lr', model1), ('gn', model2), ('rf', model3),('gb',model4),('kn',model5),('dt',model6),('lda',model7), ('bc',model8)], voting='hard')
for model, label in zip([model1, model2, model3, model4,model5,model6,model7,model8,Ensembled_model], ['Logistic Regression','Naive Bayes','Random Forest', 'Gradient Boosting','KNN','Decision Tree','LDA', 'Bagging Classifier', 'Ensemble']):
     scores = cross_val_score(model, features, target, cv=5, scoring='accuracy')
     Accuracy.append(scores.mean())
     Name.append(model.__class__.__name__)
     print("Accuracy: %f of model %s" % (scores.mean(),label))


# #apply on test
# from sklearn.metrics import accuracy_score
# classifers=[model3,model4,model6,model8]
# out_sample_accuracy=[]
# Name_2=[]
# for each in classifers:
#     fit=each.fit(features,target)
#     pred=fit.predict(test.iloc[:,0:166])
#     accuracy=accuracy_score(test['project_success'],pred)
#     Name_2.append(each.__class__.__name__)
#     out_sample_accuracy.append(accuracy)

