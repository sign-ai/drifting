"""Testing DriftingClient and client-related functions."""

import json

import numpy as np
import pandas as pd

from drifting.drift_detection_server.server import DriftType
from drifting.drifting_client import (
    DriftingClient,
    encode_infer_data,
    encode_fitting_data,
    get_params_dict,
)


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

    output_mock = {
        "outputs": [{"data": [False]}, {"data": [0.0]}] + [{"data": [0]}] * 5
    }
    requests_mock.post(
        "http://localhost:8080/v2/models/test/infer?detector_name=test&drift_type=dummy",
        text=json.dumps(output_mock),
    )
    is_drift, test_stat = client.predict(
        data, drift_type=DriftType.DUMMY, detector_name="test"
    )
    assert not is_drift
    assert test_stat == 0


def test_get_params_dict():
    """Test get_params_dict function."""
    params = get_params_dict(DriftType.LABEL, detector_name="test")
    assert "drift_type" in params
    assert params["drift_type"] == "label"


def test_encode_infer_data():
    """Test client encoding functions."""
    label_data = np.array([0.0])
    payload = encode_infer_data(label_data, DriftType.LABEL)

    assert len(payload.inputs) == 1
    assert payload.inputs[0].shape[0] == 1
    assert payload.inputs[0].shape[1] == 1

    tabular_data = pd.DataFrame([[0, 0]], columns=["a", "b"])
    payload = encode_infer_data(tabular_data, DriftType.TABULAR)

    assert len(payload.inputs) == 2
    assert payload.inputs[0].shape[0] == 1
    assert payload.inputs[0].shape[1] == 1
    assert payload.inputs[1].shape[0] == 1
    assert payload.inputs[1].shape[1] == 1


def test_encode_fitting_data():
    """Test client encoding functions."""
    label_data = np.zeros((10,))
    payload = encode_fitting_data(label_data, DriftType.LABEL)
    assert len(payload.inputs) == 1
    assert payload.inputs[0].shape[0] == 10
    assert payload.inputs[0].shape[1] == 1

    tabular_data = pd.DataFrame([[0, 0], [0, 0], [0, 0]], columns=["a", "b"])
    payload = encode_fitting_data(tabular_data, DriftType.TABULAR)

    assert len(payload.inputs) == 2
    assert payload.inputs[0].shape[0] == 3
    assert payload.inputs[0].shape[1] == 1
    assert payload.inputs[1].shape[0] == 3
    assert payload.inputs[1].shape[1] == 1
