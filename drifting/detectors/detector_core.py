"""Module implements DetectorCore base class for all drifting detectors."""

import abc
from typing import Any

from mlserver.types import InferenceRequest


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
    def save(self, detector: Any, uri: str):
        """Save the `detector` to `uri`."""

    @abc.abstractmethod
    def fit(self, data):
        """Fit the detector."""

    @abc.abstractmethod
    def decode_training_data(self, payload: InferenceRequest) -> Any:
        """Decode training data from `payload` into detector's format."""
