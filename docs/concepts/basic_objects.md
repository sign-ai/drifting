# Basic Objects

## Drift Detection Server

Drift Detection Server is an API-first Python server implemented in Python
with FastAPI. **Drift Detection Server** serves one or more **Drift Detectors**.
It also exposes the endpoints for fitting the model, getting metadata, and
managing all the **Drift Detectors**.

## Drift Detectors

**Drift Detector** is an algorithm that, based on reference data, estimates
if the statistical difference of newly arrived data is significant.
Drift Detectors use
[Alibi Detect](https://github.com/SeldonIO/alibi-detect/)
package for the statistical calculations.

## Project

**Project** consists of 3 elements:

1. ID - unique name that allows to distinguish the model and drift detector
   from others
1. Drift Detector - algorithm that detects drift and its parameters (in the
   statistical sense)
1. Configuration - configuration that allows the Drift Detector to be loaded.

Drift detector for a **Project** should be trained once and is immutable.
