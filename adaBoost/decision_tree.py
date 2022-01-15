import numpy as np
import pandas as pd
from csvfiledata import *
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

training = pd.read_csv('result_train.csv')

numerical = [
    'Age', 'Number of Dependents', 'Population', 'Latitude', 'Longitude', 'Satisfaction Score',
    'Number of Referrals', 'Tenure in Months', 'Avg Monthly Long Distance Charges',
    'Avg Monthly GB Download', 'Monthly Charge', 'Total Charges', 'Total Refunds', 
    'Total Extra Data Charges', 'Total Long Distance Charges', 'Total Revenue']

for feature in numerical:
    median = np.nanmedian(training[feature])
    new_col = np.where(training[feature].isnull(), median, training[feature])
    training[feature] = new_col

X = pd.DataFrame([training[key] for key in training.keys() if key != 'Churn Category']).T

y = training["Churn Category"]
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.20, random_state=1)

dtclf = DecisionTreeClassifier(max_depth=2, criterion='gini', random_state=1)
dtclf.fit(X_train, y_train)

dtclf_train_sc = accuracy_score(y_train, dtclf.predict(X_train))
dtclf_test_sc = accuracy_score(y_validate, dtclf.predict(X_validate))
print('Decision tree train/test accuracies %.3f/%.3f' % (dtclf_train_sc, dtclf_test_sc))

"""==========train above===test below=========="""

header, content = get_file('../sample_submission.csv')

testing = pd.read_csv('result_test.csv')

for feature in numerical:
    median = np.nanmedian(testing[feature])
    new_col = np.where(testing[feature].isnull(), median, testing[feature])
    testing[feature] = new_col

X_test = pd.DataFrame([testing[key] for key in testing.keys() if key != 'Churn Category']).T

prediction =  dtclf.predict(X_test)
for i in range(len(content)): content[i][1] = prediction[i]

write_file('guess.csv', header, content)