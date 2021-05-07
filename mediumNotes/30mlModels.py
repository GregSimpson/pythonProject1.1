
# https://github.com/ismael-araujo/Testing-Libraries

import numpy as np
import pyforest
import warnings
import pandas as pd

import lazypredict
from lazypredict.Supervised import LazyClassifier


from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

warnings.filterwarnings("ignore")
from sklearn import metrics
from sklearn.metrics import accuracy_score



# https://towardsdatascience.com/how-to-import-all-python-libraries-with-one-line-of-code-2b9e66a5879f
# !pip install pyforest
# lazy_imports()


#--------------------


# importing .csv files using Pandas
train = pd.read_csv("/home/gsimpson/PycharmProjects/pythonProject1/mediumNotes/data/titanic/train.csv")
test = pd.read_csv("/home/gsimpson/PycharmProjects/pythonProject1/mediumNotes/data/titanic/test.csv")

# we need to convert the column Sex into numeric. We can easily do that with a lambda function.
train['Sex'] = train['Sex'].apply(lambda x: 1 if x == 'male' else 2)

# We can also drop a few categorical columns that we will not be used for this micro project.
# For homework, I recommend you trying to play around with these features when you finish this article.
train.drop(columns=["Name","Ticket","Cabin", "PassengerId", "Parch", "Embarked"], inplace=True)

#--------

df_train = DataFrame(train)
df_train.fillna((df_train.mean().round(0)), inplace=True)

#%%
df_test = DataFrame(test)
df_test.fillna((df_test.mean().round(0)), inplace=True)
df_test.replace(np.nan, 'xyz', regex=True, inplace=True)

# importing .csv files using Pandas
train = pd.read_csv("/home/gsimpson/PycharmProjects/pythonProject1/mediumNotes/data/titanic/train.csv")
test = pd.read_csv("/home/gsimpson/PycharmProjects/pythonProject1/mediumNotes/data/titanic/test.csv")

# we need to convert the column Sex into numeric. We can easily do that with a lambda function.
train['Sex'] = train['Sex'].apply(lambda x: 1 if x == 'male' else 2)

# We can also drop a few categorical columns that we will not be used for this micro project.
# For homework, I recommend you trying to play around with these features when you finish this article.
train.drop(columns=["Name","Ticket","Cabin", "PassengerId", "Parch", "Embarked"], inplace=True)
#train
df_train = DataFrame(train)
df_train.fillna((df_train.mean().round(0)), inplace=True)

df_test = DataFrame(test)
df_test.fillna((df_test.mean().round(0)), inplace=True)
df_test.replace(np.nan, 'xyz', regex=True, inplace=True)
train2 = pd.DataFrame(df_train)
train2.isnull().any()



test2 = pd.DataFrame(df_test)
test2.isnull().any()
# Let's now split our train set into the variables X and y.
# I will address all the features to X, except Survived, which is our target label.
X = train2.drop(["Survived"], axis=1)
y = train2.Survived

# split the variable into train and test sets. I will go with the default 0.25 for the test size
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, random_state=42)

# run some models
#  iterate over 30 models in less than 2 seconds.
clf = LazyClassifier(verbose=0,ignore_warnings=True)
models, predictions = clf.fit(X_train2, X_test2, y_train2, y_test2)
print (models)

# check the results by running a few models and comparing them
rf = RandomForestClassifier()
rf.fit(X_train2, y_train2)
y_pred = rf.predict(X_test2)

print('Evaluation Metrics - Random Forest:')
print('Accuracy: ' + str(metrics.accuracy_score(y_test2, y_pred)))
print('F1 Score: ' + str(metrics.f1_score(y_test2, y_pred, average='macro')))
print('\n\n')

rf = LogisticRegression()
rf.fit(X_train2, y_train2)
y_pred_lr = rf.predict(X_test2)

print('Evaluation Metrics - Logistic Regression:')
print('Accuracy: ' + str(metrics.accuracy_score(y_test2, y_pred)))
print('F1 Score: ' + str(metrics.f1_score(y_test2, y_pred, average='macro')))
print('\n\n')

