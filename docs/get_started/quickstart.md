# Quick start

## Running the server

Drift-detection-server can be easily installed using pip:

```
pip install drifting
```

Running the server is easy:

```
drifting serve
```

After that, you should see the following output:

```
Starting the server

Server listening on localhost:5005
```

Also there should be `.drifting/` directory created, that will be used to
store Projects metadata.

## Preparing Drift Detector

```python
import drifting
from sklearn import datasets
from sklearn.svm import SVC

iris = datasets.load_iris()
clf = SVC()

# Train model and drift detector
clf.fit(iris.data, iris.target)
drifting.fit(data=iris.data, project="my_iris_model")
```

This example trained the model to predict Iris labels. Also, we fitted
Drift Detector called `my_iris_model`.

## Drift Detection

Now we want to receive examples to predict the label and check if the drift
occurs.

```python
# Gradually receive data to predict and detect drift
for example in iris.data:
    prediction = clf.predict(example)
    response = drifting.detect(data=example, project="my_iris_model")

print(response)
```

The response shows current status

```python
DriftResponse(is_drift=False, drift_value=0.03, window=100)
```

## Customized Drift Detector

Above example is the fastest way to start using drift detection in your ML
solution.

In practice, tuning Drift Detection is complicated and requires experiments in
the same way preparing predictive model. Drift can't be detected when it doesn't
occur and should be detected when it impacts model quality. Considering various
domains - images, speech, tabular data, different tasks - classification,
regression, usage frequency, the universal recipe for Drift Detector doesn't
exist.

The algorithms can be chosen among all the algorithms
