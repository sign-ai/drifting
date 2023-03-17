"""Implementation of client-side tools for `drifting` package."""
from typing import Tuple

import numpy as np
import pandas as pd
import requests
from mlserver import types
from mlserver.codecs import NumpyRequestCodec, PandasCodec

from drifting.drift_detection_server.server import DriftType, Params

DATA_PLANE_VERSION = "v2"


def encode_fitting_data(data, drift_type: DriftType) -> types.InferenceRequest:
    """Encode fitting data to InferenceRequest."""
    if drift_type == DriftType.LABEL:
        assert isinstance(
            data, np.ndarray
        ), "Label drift detection requires input data being np.ndarray"
        assert len(data.shape) == 1, "Label drift detection requires 2d data"
        payload = NumpyRequestCodec.encode_request(data)

    elif drift_type == DriftType.TABULAR:
        assert isinstance(
            data, pd.DataFrame
        ), "Tabular drift detection requires input data being pd.DataFrame"
        assert len(data.shape) == 2, "Tabular drift detection requires 2d data"
        payload = PandasCodec.encode_request(data)

    elif drift_type == DriftType.DUMMY:
        payload = NumpyRequestCodec.encode_request(data)

    else:
        raise NotImplementedError(
            "Only DriftType.TABULAR, DriftType.LABEL, DriftType.DUMMY implemented so far."
        )

    return payload


def encode_infer_data(data, drift_type: DriftType) -> types.InferenceRequest:
    """Encode infer data to InferenceRequest."""
    if drift_type == DriftType.LABEL:
        assert isinstance(
            data, np.ndarray
        ), "Label drift detection requires an array of shape (1,)"
        assert (
            len(data.shape) == 1 and data.shape[0] == 1
        ), "Label drift detection requires an array of shape (1,)"
        payload = NumpyRequestCodec.encode_request(data)

    elif drift_type == DriftType.TABULAR:
        if isinstance(data, pd.DataFrame):
            assert (
                len(data.shape) == 2
            ), "Tabular drift detection requires 2d data with shape (1, N)"
        elif isinstance(data, pd.Series):
            raise ValueError(
                "Pandas data has to be passed as DataFrame with shape (1, N), not a Series"
            )
        else:
            raise ValueError(
                "Tabular drift detection requires input data being pd.DataFrame"
            )
        payload = PandasCodec.encode_request(data)

    elif drift_type == DriftType.DUMMY:
        payload = NumpyRequestCodec.encode_request(data)

    else:
        raise NotImplementedError(
            "Only DriftType.TABULAR, DriftType.LABEL, DriftType.DUMMY implemented so far."
        )

    return payload


def get_params_dict(drift_type: DriftType, detector_name: str) -> str:
    """Return parameters as dictionary."""
    return Params(drift_type=drift_type, detector_name=detector_name).dict()


class DriftingClient:
    """REST client for drifting package."""

    def __init__(
        self,
        host: str = "http://localhost:8080/",
        fit_timeout: int = 300,
        regular_timeout: int = 10,
    ):
        """Init client, check connection."""
        if host.endswith("/"):
            self.host: str = host[:-1]
        self.fit_timeout = fit_timeout
        self.regular_timeout = regular_timeout
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/health/ready"
        requests.get(endpoint, timeout=self.regular_timeout).raise_for_status()

    def fit(
        self,
        train_data,
        drift_type: DriftType,
        detector_name: str,
    ) -> requests.Response:
        """Call fit method."""
        params = get_params_dict(detector_name=detector_name, drift_type=drift_type)
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/models/fit/"
        payload = encode_fitting_data(train_data, drift_type)
        response = requests.post(
            endpoint, json=payload.dict(), params=params, timeout=self.fit_timeout
        )
        # if response.status_code != 200:
        #     raise requests.HTTPError(
        #         f"Request failed with code {response.status_code} and {response.text}"
        #     )

        return response

    def load(self, detector_name: str) -> requests.Response:
        """Call load method."""
        endpoint = (
            f"{self.host}/{DATA_PLANE_VERSION}/repository/models/{detector_name}/load"
        )
        response = requests.post(endpoint, timeout=self.fit_timeout)
        response.raise_for_status()
        return response

    def predict(
        self, data, drift_type: DriftType, detector_name: str
    ) -> Tuple[bool, float]:
        """Call predict method."""
        params = get_params_dict(detector_name=detector_name, drift_type=drift_type)
        endpoint = f"{self.host}/{DATA_PLANE_VERSION}/models/{detector_name}/infer"
        payload = encode_infer_data(data, drift_type)

        response = requests.post(
            endpoint, json=payload.dict(), params=params, timeout=self.regular_timeout
        )
        response.raise_for_status()

        response_dict = response.json()
        is_drift = response_dict["outputs"][0]["data"][0]
        test_stat = response_dict["outputs"][6]["data"][0]

        return is_drift, test_stat
