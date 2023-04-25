# Quick start

## Running the server

drifting can be easily installed using pip:

```
pip install drifting
```

Running the server is easy:

```
drifting start *models_directory/*
```

After that, you should see the following output:

```
Uvicorn running on http://0.0.0.0:8082 (Press CTRL+C to quit)
```

Also there should be `models_directory/` directory created, that will be used to
store models and metadata.

## Preparing Drift Detector

```python
from drifting import DriftingClient, DriftType
from sklearn import datasets
from sklearn.svm import SVC

iris = datasets.load_iris()

# Train classifier
clf = SVC()
clf.fit(iris.data, iris.target)

# Fit drift detector
client = DriftingClient()

client.fit(white, drift_type=DriftType.TABULAR, detector_name="IrisDriftDetector")
```

This example trained the model to predict Iris labels. After, we fitted
Drift Detector called `IrisDriftDetector`.

## Drift Detection

Now we want to receive examples to predict the label and check if the drift
occurs.

```python
# Gradually receive data to predict and detect drift
for row in iris.data:
    prediction = clf.predict(row)
    is_drift, test_stat = client.predict(row, drift_type=DriftType.TABULAR, detector_name="IrisDriftDetector")

print(is_drift)
```

The response shows current status

```python
is_drift: False
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
