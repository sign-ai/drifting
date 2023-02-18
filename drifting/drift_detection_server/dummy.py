"""Dummy drift detection.

Used for testing purposes, may be used as placeholder.
"""

import numpy as np
from mlserver import MLModel, types
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.types import InferenceRequest

from drifting.drift_detection_server.detector_core import DetectorCore


class DummyDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._implementation_path = "label.DummyDriftDetectorCore"

    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def load(self, uri) -> bool:
        """See base class."""
        return True

    def save(self, detector, uri):
        """See base class."""

    def predict(self, input_data):
        return True, 1.0

    def fit(self, data):
        """Fit dummy detector."""
        return None

    def decode(self, payload: InferenceRequest):
        """See base class."""
        return NumpyRequestCodec.decode_request(payload)

    def encode(self, drift_detected, estimation):
        """See base class."""
        return [
            NumpyCodec.encode_output(name="drift", payload=np.array([drift_detected])),
            NumpyCodec.encode_output(name="stat_val", payload=np.array([estimation])),
        ]


class DummyDetector(MLModel):
    """Class used during inference."""

    async def load(self) -> bool:
        # pylint: disable=attribute-defined-outside-init
        self.uri = self.settings.parameters.uri
        self.model = DummyDriftDetectorCore()
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.model.decode(payload)
        drift_detected, estimation = self.model.predict(input_data)
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters={"content_type": "drift"},
            outputs=self.model.encode(drift_detected, estimation),
        )
