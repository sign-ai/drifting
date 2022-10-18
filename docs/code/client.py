"""Example request to the Drift Detection Server.

In order to run this example, you must run Drift Detection Server
using `drifting serve`.

We follow https://github.com/SeldonIO/alibi-detect/blob/master/doc/source/examples/cd_spot_the_diff_mnist_wine.ipynb
"""

"""To provide an example on tabular data we consider the Wine Quality Data Set consisting of 4898 and 1599 samples of white and red wine respectively. Each sample has an associated quality (as determined by experts) and 11 numeric features indicating its acidity, density, pH etc. To represent the problem of a model being trained on one distribution and deployed on a subtly different one, we take as a reference set the samples of white wine and consider the red wine samples to form a 'corrupted' deployment set.

"""
import json

import requests

import pandas as pd
import numpy as np


red_df = pd.read_csv(
    "https://storage.googleapis.com/seldon-datasets/wine_quality/winequality-red.csv",
    sep=";",
)
white_df = pd.read_csv(
    "https://storage.googleapis.com/seldon-datasets/wine_quality/winequality-white.csv",
    sep=";",
)
white_df.describe()

white, red = (
    np.asarray(white_df, np.float32)[:, :-1],
    np.asarray(red_df, np.float32)[:, :-1],
)
n_white, n_red = white.shape[0], red.shape[0]

col_maxes = white.max(axis=0)
white, red = white / col_maxes, red / col_maxes
white, red = (
    white[np.random.permutation(n_white)],
    red[np.random.permutation(n_red)],
)
x, x_corr = white, red

x_ref = x[: len(x) // 2]
x_h0 = x[len(x) // 2 :]

payload = {"data": [1.0, 1.0, 1.0]}
data = json.dumps(payload)

preds_h0 = requests.post(
    "http://localhost:5005/fit", data=data, params={"project_id": "A"}
)
preds_corr = requests.post()

print(f"Drift on h0? {'Yes' if preds_h0['data']['is_drift'] else 'No'}")
print(f"p-value on h0: {preds_h0['data']['p_val']}")
print(
    f"Drift on corrupted? {'Yes' if preds_corr['data']['is_drift'] else 'No'}"
)
print(f"p-value on corrupted:: {preds_corr['data']['p_val']}")

requests.post()
