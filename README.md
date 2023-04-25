# Drifting

[![CI/CD](https://github.com/smolendawid/cacha/actions/workflows/cicd.yaml/badge.svg)](https://github.com/sign-ai/drifting/actions/workflows/precommit.yaml)
[![PyPi](https://img.shields.io/pypi/v/cacha?label=PyPI&logo=pypi)](https://pypi.org/project/cacha/)
[![License](https://img.shields.io/pypi/l/cacha.svg)](https://github.com/sign-ai/drifting/blob/main/LICENSE)

The most flexible Drift Detection Server.

Learn about the concepts in
[Docs](https://sign-ai.github.io/drifting/)

---

Main features:

:+1: surprisingly easy to use

:+1: production-ready server

:+1: created with real use-cases in mind

:+1: not just a math library

:+1: Python-first, API-first

## Quickstart

`drifting` is built with Developer Experience in mind.

You communicate with Drift Detection Server via `DriftingClient` or API,
both for fitting the Drift Detector and detecting the drift. In your training
pipeline, use the `fit` method:

```python
from drifting import DriftingClient, DriftType
from sklearn import datasets

iris = datasets.load_iris()
client = DriftingClient()

client.fit(white, drift_type=DriftType.TABULAR, detector_name="IrisDriftDetector")

```

Then, next to your prediction call:

```python
for row in iris.data:
    prediction = clf.predict(row)
    is_drift, test_stat = client.predict(row, drift_type=DriftType.TABULAR, detector_name="IrisDriftDetector")

```

Note that this makes the usage of the server **as easy as possible**.

1. You only make a request to the server once per prediction, alongside with prediction.
1. It's not required to manage any artifacts,
1. No need to implement any feedback loops,
1. No need to collect test data,
1. No need to leave your python environment, fetch any logs,

## Local installation and running

To install dependencies:

```
pip install -r requirements.txt
```

And run server locally (uses 'drift_detectors/' path for artifacts):

```
drifting start drift_detectors/
```

## Production usage

To use Drift Detection Server in your organization,
build and deploy the Docker image, or use the pre-built version from _TODO_.

### Docker on a custom server

To deploy the on cloud instance using docker, you can easily pull the image
and run it:

```python
docker run -it sign-ai/drifting
```

### Kubernetes and Helm

For more demanding use-cases, it's facilitated to deploy Drift Detection Server
on kubernetes. DDS is packaged with bitnami. Example Helm charts are not 
implemented yet.

## Real-world scenarios

Even though Drift Detection Server makes the task incredibly easy,
it still follows the MLOps culture, assuring reproducibility,
observability and scalability postulates are fulfilled.

Please read the [Docs](https://sign-ai.github.io/drifting/)
to learn about real-world usage.
