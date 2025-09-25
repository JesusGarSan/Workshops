
from mspc_pca.pca import adjust_PCA
from mspc_pca.plot import var_pca, biplot, loadings, scores
from sklearn.preprocessing import StandardScaler
from venues.app.plots import *

import pandas as pd


df = pd.read_csv("venues/data/full_data.csv")

print(df.columns.values)
obs_labels = df["name"].to_list()

df_cat = df.select_dtypes(None, ['float64', 'int64'])
classes = []
class_names = df_cat.columns.values
for class_name in class_names:
    classes.append(df[class_name].to_list())

df_num = df.select_dtypes(['float64', 'int64'])
df_num.drop(['latitude', 'longitude', 'day'], axis=1, inplace=True)
var_labels = df_num.columns.values

data = df_num.to_numpy()

scaler = StandardScaler(with_std=True).fit(data)
X = scaler.fit_transform(data)

fig, ax = var_pca(X, X.shape[1])
# fig.show()
X_pca, pca = adjust_PCA(X, 2, True)

for i, score_class in enumerate(classes):
    pass
    # fig, _ , _ = biplot(X, pca, 1, 2,obs_labels,var_labels, score_classes=score_class, loading_percentile=0)
    # fig.suptitle(class_names[i])
    # fig.show()






fig = scores_plotly(X, pca, 1, 2, obs_labels,2, classes = classes[2])
fig.update_layout(title=class_names[2])
fig.show()

fig = loadings_plotly(pca, 1, 2, var_labels)
fig.show()
input()