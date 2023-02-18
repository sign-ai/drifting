"""Module implements DetectorCore base class for all drifting detectors."""

import abc
from typing import Any

from mlserver.types import InferenceRequest, InferenceResponse


class DetectorCore(abc.ABC):
    """Base class for all the drifting detectors.

    In addition to basic statistical methods it implements the conversion
    to mlservers inference response and requests.
    """

    @property
    @abc.abstractmethod
    def implementation_path(self):
        """Get path to implementation of a detector."""

    @abc.abstractmethod
    def load(self, uri: str):
        """Load model to the object field."""

    @abc.abstractmethod
    def save(self, detector: Any, uri: str):
        """Save the `detector` to `uri`."""

    @abc.abstractmethod
    def predict(self, input_data: InferenceRequest) -> InferenceResponse:
        """Predict drift, update the model state."""

    @abc.abstractmethod
    def fit(self, data):
        """Fit the detector."""

    @abc.abstractmethod
    def decode(self, payload: InferenceRequest):
        """Decode `payload` into format understood by detector."""

    @abc.abstractmethod
    def encode(self, drift_detected: bool, estimation: float) -> InferenceResponse:
        """Encode detector prediction into MLServer's InferenceResponse."""
