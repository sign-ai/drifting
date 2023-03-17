"""Dummy drift detection.

Used for testing purposes, may be used as placeholder.
"""

from mlserver import MLModel, types
from mlserver.types import InferenceRequest

from drifting.detectors.detector_core import DetectorCore


class DummyDetector(MLModel):
    """Class used during inference."""

    async def load(self) -> bool:
        # pylint: disable=attribute-defined-outside-init
        self.uri = self.settings.parameters.uri
        self.model = DummyDriftDetectorCore()
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        drift_detected, estimation = 0, 0
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters={"content_type": "drift"},
            outputs=(drift_detected, estimation),
        )


class DummyDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._implementation_path = "label.DummyDriftDetectorCore"

    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def save(self, detector, uri):
        """See base class."""

    def fit(self, data):
        """Fit dummy detector."""
        return None

    def decode_training_data(self, payload: InferenceRequest):
        """See base class."""
        return payload
