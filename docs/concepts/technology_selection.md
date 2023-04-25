# Technology selection

Based on many observations, drifting is built based on the best packages, that
give it the easy start but also assure the best quality for the server and 
the used methods.

## mlserver
[mlserver](https://github.com/SeldonIO/MLServer) is a modern, top-tier, 
feature-rich package for serving Machine Learning models. Building 
drifting on the top lets drifting use all the best design patterns.

## Alibi Detect

Alibi detect implements online algorithms, uses methods proven to work by
the research, and is very configurable.

# Comparison to other packages

## Alibi-detect-server from seldon-core

It is possible to build the solution in accordance with the framework proposed
by **drifting** using seldon-core and 
[alibi-detect-runtime](https://github.com/SeldonIO/MLServer/tree/master/runtimes/alibi-detect). 

The example of a similar project can be found [here](https://docs.seldon.io/projects/seldon-core/en/latest/analytics/drift_detection.html?highlight=drift%20detection#drift-detection-in-seldon-core), where the 
drift detector can be chained to a model and 
can make the predictions always after the regular model prediction. However,
this solution requires a lot of DevOps expertise, while in drifting, all the 
necessary steps can be easily done in Python, next to the regular model 
deployment. 

## Evidently

[Evidently](https://github.com/evidentlyai/evidently) focuses on providing 
the tools for mathematical computation and visualization of drift. It's not
a solution to detect the drift in production in the framework proposed by
**drifting**.
