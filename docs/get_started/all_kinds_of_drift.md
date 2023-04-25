# All kinds of drift explained

The definitions of all kinds of drift may be unclear in the community.
Unfortunately names are confused over internet and it's hard to discuss
the specifics when they will not be clarified. Below we describe the most
important phenomena that can occur in the data.

The `drifting` package greatly facilitates the work with Covariate Shift,
Prior Drift, and Label Drift. Concept Drift doesn't fit the proposed framework,
as it requires labeled data, which is not available on the inference time.

We recommend watching the excellent [Drift Detection Overview by Seldon](https://www.youtube.com/watch?v=JaPMFf0cKlM).


## Covariate shift

_Also called Data Drift, Covariate Drift, Features Drift_

Covariate Shift is the difference between the features from training data,
and inference data. It can be also the difference between the raw data from 
training time, and inference time.

## Prior Drift

_Also called Label Drift_

This is the difference between the **predictions** on data training data, and on
the inference data. Please note it's not using the labels directly, as the 
original label distribution is often different that the predictions for the same 
data! In order to make fair comparison using labels directly, it would be 
necessary to first collect the real labels for the inference data.

## Concept Drift

Concept Drift doesn't fit the proposed framework. Concept Drift is defined as
the shift in the relationship between the independent and the target variable.
That means `X` training data changes in relation to `y` data.

The intuitive way of thinking about Concept Drift is just the accuracy
(understood as any specific metric) drop without any observable drift
in `X` or `y` itself.

In a nutshell, when the model is 90% accurate in the training environment, and
90% accurate in the production environment, but then the accuracy starts to drop
(or goes higher!), it means the Concept Drift may occur.
If no Covariate Shift and Prior Drift are not observed, that may mean the
relationship between `X` and `y` changes.

Unfortunately, the real `y` is not known during the inference. Depending on the
domain, sometimes labels are known after some time, after the inference. However
usually obtaining the real labels requires human-in-the-loop and is very
expensive.

Unlike the Covariate Shift and Prior Drift, we don't have the real labels for
Concept Drift, and we can't use it during inference. That means the advised
framework doesn't fit in the detection of Concept Drift.

## Concept Drift with `drifting`

Naturally, Concept Drift Detector can be created for a model during the training
in the same way other Detectors are prepared, but the Concept Drift detection
has to happen outside the inference. In this sense, `drifting` package can
be used as any other tool for detecting Concept Drift. Serving the Detector in
Drift Detection Server still facilitates much work, as during the offline
Concept Drift detection job, data fetching is simpler.

The architecture below is the example of Concept Drift detection outside
inference server. It requires implementing a feedback loop, and scheduled job to
run the detection process.

``` mermaid
graph TD
  A[Data] --> B[Model];
  B --> C[Predictions];
  C --> D[Database]
  A --> E[Drift Detection Job]
  D --> E[Drift Detection Job]
```
