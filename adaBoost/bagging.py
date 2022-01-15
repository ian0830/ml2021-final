import numpy as np
import pandas as pd
from csvfiledata import *
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

training = pd.read_csv('result_train.csv')

numerical = [
    'Age', 'Number of Dependents', 'Population', 'Latitude', 'Longitude', 'Satisfaction Score',
    'Number of Referrals', 'Tenure in Months', 'Avg Monthly Long Distance Charges',
    'Avg Monthly GB Download', 'Monthly Charge', 'Total Charges', 'Total Refunds', 
    'Total Extra Data Charges', 'Total Long Distance Charges', 'Total Revenue']

for feature in numerical:
    median = np.nanmedian(training[feature])
    new_col = np.where(training[feature].isnull(),
                    median, training[feature])
    training[feature] = new_col

X = pd.DataFrame([training[key] for key in training.keys() if key != 'Churn Category']).T
y = training["Churn Category"]
X_train, X_validate, y_train, y_validate = train_test_split(X, y, test_size=0.20, random_state=1)

bag = BaggingClassifier(n_estimators = 100)
bag_fit = bag.fit(X_train, y_train)

# predict and accuracy
test_y_predicted = bag.predict(X_validate)
accuracy = accuracy_score(y_validate, test_y_predicted)
print(accuracy)

"""==========train above===test below=========="""

header, content = get_file('../sample_submission.csv')

testing = pd.read_csv('result_test.csv')

for feature in numerical:
    median = np.nanmedian(testing[feature])
    new_col = np.where(testing[feature].isnull(),
                    median, testing[feature])
    testing[feature] = new_col

X_test = pd.DataFrame([testing[key] for key in testing.keys() if key != 'Churn Category']).T

prediction =  bag.predict(X_test)
for i in range(len(content)): content[i][1] = prediction[i]

write_file('guess_bagging.csv', header, content)
