# %% [markdown]
# Most of this study is thanks to this tutorial : https://kapernikov.com/tutorial-image-classification-with-scikit-learn/

# %%
import os

import h5py
import matplotlib.pyplot as plt
import numpy as np

h5_file = h5py.File(os.path.join("img", "ML_dataset", "dataset.h5"), "r")
X = np.array(h5_file.get("dataset"))
y = np.array(h5_file.get("labels"))
h5_file.close()


# %%
# use np.unique to get all unique values in the list of labels
labels = np.unique(y)

# set up the matplotlib figure and axes, based on the number of labels
fig, axes = plt.subplots(1, len(labels))
fig.set_size_inches(15, 4)
fig.tight_layout()

# make a plot for every label (equipment) type. The index method returns the
# index of the first item corresponding to its search string, label in this case
for ax, label in zip(axes, labels):
    idx = list(y).index(label)

    ax.imshow(X[idx])
    ax.axis("off")
    ax.set_title(label)

# %%
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=True,
    random_state=42,
)

# %%
def plot_bar(y, loc="left", relative=True):
    width = 0.35
    if loc == "left":
        n = -0.5
    elif loc == "right":
        n = 0.5

    # calculate counts per type and sort, to ensure their order
    unique, counts = np.unique(y, return_counts=True)
    sorted_index = np.argsort(unique)
    unique = unique[sorted_index]

    if relative:
        # plot as a percentage
        counts = 100 * counts[sorted_index] / len(y)
        ylabel_text = "% count"
    else:
        # plot counts
        counts = counts[sorted_index]
        ylabel_text = "count"

    xtemp = np.arange(len(unique))

    plt.bar(xtemp + n * width, counts, align="center", alpha=0.7, width=width)
    plt.xticks(xtemp, unique, rotation=45)
    plt.xlabel("equipment type")
    plt.ylabel(ylabel_text)


plt.suptitle("relative amount of photos per type")
plot_bar(y_train, loc="left")
plot_bar(y_test, loc="right")
plt.legend([f"train ({len(y_train)} photos)", f"test ({len(y_test)} photos)"])


# %%
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from utils import RGB2Gray2ShapeTransformer

pipe = Pipeline(
    [
        ("grayify", RGB2Gray2ShapeTransformer()),
        ("scalify", StandardScaler()),
        ("classify", SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)),
    ]
)
clf = pipe.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Percentage correct: ", 100 * np.sum(y_pred == y_test) / len(y_test))

# %%
from sklearn.metrics import confusion_matrix

cmx = confusion_matrix(y_test, y_pred)
cmx


# %%
# Grid search
from sklearn import svm
from sklearn.model_selection import GridSearchCV

param_grid = {
    "classify": [
        SGDClassifier(loss="log", random_state=42, max_iter=1000, tol=1e-3),
        # SGDClassifier(random_state=42, max_iter=10000, tol=1e-4),
        # svm.SVC(kernel="linear"),
        # svm.SVC(kernel="rbf"),
    ]
}

grid_search = GridSearchCV(
    pipe, param_grid, cv=3, n_jobs=None, scoring="accuracy", verbose=1, return_train_score=True
)

grid_res = grid_search.fit(X_train, y_train)
print(grid_res.best_estimator_)

# %%
y_pred = grid_res.predict(X_test)
print("Percentage correct: ", 100 * np.sum(y_pred == y_test) / len(y_test))

# %%
import joblib

with open("trained_model.pkl", "wb") as f:
    joblib.dump(grid_res.best_estimator_, f)

# %%
