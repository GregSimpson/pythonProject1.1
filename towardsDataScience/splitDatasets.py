
import pandas as pd
from sklearn.datasets import load_iris

iris_data = load_iris()
df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
print(df)
