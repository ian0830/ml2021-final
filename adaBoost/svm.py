from sklearn import svm
from sklearn import metrics
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd

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

X = pd.DataFrame([training[key]
                  for key in training.keys() if key != 'Churn Category']).T
y = training["Churn Category"]

X_train, X_validate, y_train, y_validate = train_test_split(
    X, y, test_size=0.2, random_state=3)

# svm classification
clf = svm.SVC(kernel='rbf', gamma=0.000001, C=4096).fit(X_train, y_train)
y_predicted = clf.predict(X_validate)

accuracy = accuracy_score(y_validate, y_predicted)
print('Accuracy', accuracy)
# performance

print(metrics.classification_report(y_validate, y_predicted))
print("Confusion matrix")
print(metrics.confusion_matrix(y_validate, y_predicted))
