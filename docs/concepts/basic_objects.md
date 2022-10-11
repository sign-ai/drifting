# Basic Objects

## Model

In `drifting`, **'Model'** name is used for predictive algorithm used by a user
_outside_ this package. **Model** can be understood as the algorithm, its
weights (parameters), inference graph.

Drift Detection is a process of measuring the **Model** or data drift. Usually,
**Drift Detector** is fitted for each training of a given **Model**

## Drift Detection Server (DDS)

**Drift Detection Server** is an API-first Python server implemented
with FastAPI. DDS serves one or more **Drift Detectors**.
It also exposes the endpoints for fitting the **Drift Detector**,
getting metadata, and managing all the **Projects**.

## Drift Detectors

**Drift Detector** is an algorithm that, based on reference data, estimates
if the statistical difference of newly arrived data is significant.
**Drift Detectors** use
[Alibi Detect](https://github.com/SeldonIO/alibi-detect/)
package for the statistical calculations.

## Project

**Project** consists of 3 elements:

1. **ID** - unique name that allows to distinguish the model and drift detector
   from others
1. **Drift Detector** - algorithm that detects drift and its parameters (in the
   statistical sense)
1. **Configuration** - configuration that allows the Drift Detector to be loaded.

Drift detector for a **Project** should be trained once and is immutable.

The following diagram should explain the dependencies between the objects easily:

TODO
