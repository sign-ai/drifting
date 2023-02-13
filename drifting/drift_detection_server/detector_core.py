"""Module implements DetectorCore base class for all drifting detectors."""

import abc
from typing import Any

from mlserver.types import InferenceRequest, InferenceResponse


class DetectorCore(abc.ABC):
    """Base class for all the drifting detectors.

    In addition to basic statistical methods it implements the conversion
    to mlservers inference response and requests.
    """

    def load(self, uri: str):
        """Load model to the object field."""

    def save(self, detector: Any, uri: str):
        """Save the `detector` to `uri`."""

    def predict(self, input_data: InferenceRequest) -> InferenceResponse:
        """Predict drift, update the model state."""

    def fit(self, data):
        """Fit the detector."""

    def decode(self, payload: InferenceRequest):
        """Decode `payload` into format understood by detector."""

    def encode(self, drift_detected: bool, estimation: float) -> InferenceResponse:
        """Encode detector prediction into MLServer's InferenceResponse."""
