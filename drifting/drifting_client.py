"""Implementation of client-side tools for `drifting` package."""
import numpy as np
import pandas as pd
import requests
from drifting.drift_detection_server.server import DriftType, get_params
from mlserver import types

DATA_PLANE_VERSION = "v2"


from mlserver.codecs import NumpyRequestCodec, PandasCodec


def encode(train_data, drift_type: DriftType):
    if drift_type == DriftType.LABEL.value:
        assert isinstance(
            train_data, np.ndarray
        ), "Label drift detection requires input data being np.ndarray"
        assert len(train_data.shape) == 1, "Label drift detection requires 2d data"
        payload = NumpyRequestCodec.encode_request(train_data)

    if drift_type == DriftType.TABULAR.value:
        assert isinstance(
            train_data, pd.DataFrame
        ), "Tabular drift detection requires input data being pd.DataFrame"
        assert len(train_data.shape) == 2, "Tabular drift detection requires 2d data"
        payload = PandasCodec.encode_request(train_data)

    return payload


class DriftingClient:
    """REST client for drifting package."""

    def __init__(self, host: str = "http://localhost:8080/"):
        """Init client, check connection."""
        if host.endswith("/"):
            self.host: str = host[:-1]
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/health/ready"
        try:
            requests.get(endpoint).raise_for_status()
        except:
            print("SADSADSA")

    def fit(
        self,
        train_data,
        drift_type: DriftType,
        detector_name: str,
    ) -> requests.Response:
        """Call fit method."""
        params = get_params(detector_name=detector_name, drift_type=drift_type)
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/models/fit/"
        payload = encode(train_data, drift_type)
        response = requests.post(endpoint, json=payload.dict(), params=params)
        # if response.status_code != 200:
        #     raise requests.HTTPError(f"Request failed with code {response.status_code} and {response.text}") 

        return response

    def predict(
        self, data, drift_type: DriftType, detector_name: str
    ) -> types.InferenceResponse:
        """Call predict method."""
        params = get_params(detector_name=detector_name, drift_type=drift_type)
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/models/{detector_name}/infer"
        payload = encode(data, drift_type)

        response = requests.post(endpoint, json=payload.dict(), params=params)
        response.raise_for_status()
        return response

    def load(self, detector_name: str) -> requests.Response:
        """Call load method."""
        endpoint = (
            f"{self.host}/{DATA_PLANE_VERSION}/repository/models/{detector_name}/load"
        )
        response = requests.post(endpoint)
        response.raise_for_status()
        return response
