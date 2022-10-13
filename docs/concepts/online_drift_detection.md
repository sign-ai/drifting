# Online Drift Detection

One of the most important assumptions is that the drift can be detected
in parallel with prediction. That means the drift detection happens on the fly,
online, during a regular work of predictive algorithm.

This assumption, though simple, has many implications. The most important idea
is that thanks to online drift, no additional jobs nor feedback loops have to
be implemented.

Imagine the following workflow:

- model is trained
- model makes predictions
- predictions are loaded

Another job is:

- collecting data from the train period
- training drift detection
- collecting predictions from the test period
- making drift detection

This solution is hard to implement. It requires to repeat the model training
steps, it has to download the data from different sources (training data,
predictions) and integrate everything. Also, it doesn't provide the
immediate drift detection, depending on the frequency of the runs.
