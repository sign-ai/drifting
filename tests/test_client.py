"""Testing DriftingClient and client-related functions."""

import json

import numpy as np

from drifting.drift_detection_server.server import DriftType
from drifting.drifting_client import DriftingClient, encode_infer_data, get_params_dict


def test_client_flow(requests_mock):
    """Test client methods with casual flow."""
    data = np.array((0,))

    requests_mock.get("http://localhost:8080/v2/health/ready", text="data")
    client = DriftingClient()
    requests_mock.post(
        "http://localhost:8080/v2/models/fit/?detector_name=test&drift_type=dummy",
        text="data",
    )
    client.fit(data, drift_type=DriftType.DUMMY, detector_name="test")

    requests_mock.post(
        "http://localhost:8080/v2/repository/models/test/load", text="data"
    )
    client.load(detector_name="test")

    output_mock = {"outputs": [{"data": [False]}, {"data": [0.0]}]}
    requests_mock.post(
        "http://localhost:8080/v2/models/test/infer?detector_name=test&drift_type=dummy",
        text=json.dumps(output_mock),
    )
    client.predict(data, drift_type=DriftType.DUMMY, detector_name="test")


def test_get_params_dict():
    """Test get_params_dict function."""


def test_encode_fit_data():
    """Test client encoding functions."""
