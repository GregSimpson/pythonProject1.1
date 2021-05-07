# evaluate a weighted average ensemble for regression with rankings for model weights
from numpy import argsort
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.ensemble import VotingRegressor

# get a list of base models
def get_models():
	models = list()
	models.append(('knn', KNeighborsRegressor()))
	models.append(('cart', DecisionTreeRegressor()))
	models.append(('svm', SVR()))
	return models

# evaluate each base model
def evaluate_models(models, X_train, X_val, y_train, y_val):
	# fit and evaluate the models
	scores = list()
	for name, model in models:
		# fit the model
		model.fit(X_train, y_train)
		# evaluate the model
		yhat = model.predict(X_val)
		mae = mean_absolute_error(y_val, yhat)
		# store the performance
		scores.append(-mae)
		# report model performance
	return scores

# define dataset
X, y = make_regression(n_samples=10000, n_features=20, n_informative=10, noise=0.3, random_state=7)
# split dataset into train and test sets
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size=0.50, random_state=1)
# split the full train set into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_train_full, y_train_full, test_size=0.33, random_state=1)
# create the base models
models = get_models()
# fit and evaluate each model
scores = evaluate_models(models, X_train, X_val, y_train, y_val)
print(scores)
ranking = 1 + argsort(argsort(scores))
print(ranking)
# create the ensemble
ensemble = VotingRegressor(estimators=models, weights=ranking)
# fit the ensemble on the training dataset
ensemble.fit(X_train_full, y_train_full)
# make predictions on test set
yhat = ensemble.predict(X_test)
# evaluate predictions
score = mean_absolute_error(y_test, yhat)
print('Weighted Avg MAE: %.3f' % (score))
# evaluate each standalone model
scores = evaluate_models(models, X_train_full, X_test, y_train_full, y_test)
for i in range(len(models)):
	print('>%s: %.3f' % (models[i][0], scores[i]))
# evaluate equal weighting
ensemble = VotingRegressor(estimators=models)
ensemble.fit(X_train_full, y_train_full)
yhat = ensemble.predict(X_test)
score = mean_absolute_error(y_test, yhat)
print('Voting MAE: %.3f' % (score))