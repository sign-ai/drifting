# The workflow with `drifting` package

The standard workflow with `drifting` can be illustrated by the following steps:

## Train the model

Machine Learning Model is trained. Usually the training process outputs
some artifact, eg. models parameters.
At this moment, after the training, we suggest to train Drift Detectors for a
given Model. Usually Drift Detector is trained for a few features, for label
(prior drift), and for concept drift.

Next to your train function, add the drift fitting.

`drifting` _Project_ has to be connected to the given machine learning model.
The `project_id` should be saved next to the Model artifact or any other place
so that it can be referenced correctly during inference.

```python
todo code example
```

## Use the model (inference)

Machine Learning model is loaded on the inference server. At this point, the
inference server should be able to call the correct Project in
Drift Detection Server. Each time model makes prediction, the data point
should be sent to Drift Detector. Thanks to that event, no feedback loops are
needed and drift is monitored 'automatically'.

Note that the request can be made asynchronously so that drift detection doesn't
impact the speed of prediction of a model. It can be also done 'after request'
depending on the functionality you model server provides.

```python
todo code example
```

## Re-train the model

Depending on the implementation, the models can be retrained 'on the fly', or
retrained, stopped, and re-deployed as a new version/on a new Pod etc. In case
of Drift Detector, it should be always re-fitted together with the training of
a new ML model. After that, it is referenced correctly during the inference of
a model.

## Manage many Drift Detectors

The workflow described above doesn't change with the number of models deployed.
Each model can be managed separately and each drift detector should be managed
together with the corresponding model.
