
# https://betterprogramming.pub/7-must-try-data-visualization-libraries-in-python-fd0fe76e08a0

# pip install seaborn

import seaborn as sns
from sklearn.datasets import load_iris
iris = load_iris()


#train = pd.read_csv("/home/gsimpson/PycharmProjects/pythonProject1/mediumNotes/data/titanic/train.csv")

#iris = sns.load_dataset('iris')

#iris = sns.load_dataset("/home/gsimpson/PycharmProjects/pythonProject1/mediumGUIs/data/iris.data")
#iris = sns.load_dataset("iris")

sns.pairplot(iris,hue='species')

'''
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
target_names = iris.target_names
print("Feature names:", feature_names)
print("Target names:", target_names)
print("\nFirst 10 rows of X:\n", X[:10])
'''
