# Drift Detection Server

The most flexible Drift Detection framework.

Learn about the concepts in
[Docs](https://smolendawid.github.io/drift-detection-server/)

## Quickstart

Developer Experience first.

You communicate with Drift Detection Server via API, both for fitting
and predicting the drift. In your training pipeline, use the `fit/` endpoint:

```
TODO
```

where _labels_ are the `y` targets.

Then, next to your prediction call:

```
TODO
```

where `_y` are the predicted targets.

Note that this makes the usage of the server **as easy as possible**.

1. It's not required to manage any artifacts,
1. No need to implement any feedback loops,
1. No need to leave your python environment, fetch any logs,
1. You only call API twice.

## Local installation and running

To install dependencies, use poetry:

```
poetry install
```

And run server locally:

```
python drift_detection_server/app.py
```

## Production usage

To use Drift Detection Server in your organization,
build and deploy the Docker image, or use the pre-built version from _TODO_.

### Docker on a custom server

To deploy the on cloud instance using docker, you can easily pull the image
and run it:

```python
TODO
```

### Kubernetes and Helm

For more demanding use-cases, it's facilitated to deploy Drift Detection Server
on kubernetes. DDS is packaged with bitnami. You can include the chart by

```python
TODO
```

## Real-world scenarios

Even though Drift Detection Server makes the task incredibly easy,
it still follows the MLOps culture, assuring reproducibility,
observability and scalability postulates are fulfilled.

Please read the [Docs](https://smolendawid.github.io/drift-detection-server/)
to learn about real-world usage.
