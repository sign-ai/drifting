"""
The ``drifting`` module provides DriftingClient for communicating with 
DriftDetectionServer.
For example:
.. code:: python
    from drifting import DriftingClient
    dc = DriftingClient(host="http://localhost:8080/")
"""

from drifting.drifting_client import DriftingClient
from drifting.drift_detection_server.server import DriftType
