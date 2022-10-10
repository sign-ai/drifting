# Other assumptions

## Drift detectors are lightweight

This is a strong assumption of Drift Detection Server. It should never be an
issue in the cases where server handles a few models. However, in cases where
the server is responsible for detection of thousands models' drifts, things
start to complicate.

## Drift detectors can be made lightweight

Prior drift and concept drift are operating in targets space so the calculations
are lightweight by nature.

Otherwise, covariate shift is calculated on features. In practice, covariate
shift can be calculated on raw data, sometimes fed directly to the learning
algorithm, or on the features that are derived from the raw data.

### Tabular data

In case of tabular data, every data processing step can be shared and run only
once for both model and drift detector.
Thanks to API-first approach, features distributions can be sent asynchronously
after they are derived and before they are fed to learning algorithm.

In practice, monitoring drift for features is complicated. It is experimental
work that requires crafting in a similar way machine learning models do.

That's way we assume covariate shift is monitored for single columns and the
detectors are added for the next features gradually.

### Images/Speech/Text

Even though it is not always true, we believe drift detection can be done
in the feature space. That means it is possible to share calculations between
model inference graphs and drift detection graphs and make drift detection
lighter. API-first approach works well with this optimization.

## Comparison to other packages

For many cases the solution we advice is Seldon Alibi Detect Server. Seldon
Core is great technology that covers with the best principles MLOps in mind.
The only arguable disadvantage is that setting up Seldon Alibi Detect Server
requires a lot of DevOps expertise in order to keep the architecture clear.

Seldon Alibi Detect Server doesn't implement `train/` endpoint. However,
considering most use-cases, managing artifacts next to the model weights
should not be too complex.
