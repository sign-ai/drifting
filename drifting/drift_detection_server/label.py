"""Label drift detection.

Label drift detection works both for classification and regression labels.
"""

import os
import pickle

import numpy as np
import river.drift
from mlserver import MLModel, types
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.errors import InferenceError, MLServerError
from mlserver.types import InferenceRequest

from drifting.drift_detection_server.detector_core import DetectorCore


class LabelDriftDetector(MLModel):
    """Class used during inference."""

    async def load(self) -> bool:
        # pylint: disable=attribute-defined-outside-init
        try:
            with open(
                os.path.join(self.settings.parameters.uri, "label_detector.pkl"), "rb"
            ) as file:
                self._model: river.drift.ADWIN = pickle.load(file)
            self.ready = True
        except Exception as err:
            raise MLServerError(
                f"Invalid configuration for model {self._settings.name}: {err}"
            ) from err

        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        try:
            self._model.update(input_data)
        except (ValueError, IndexError) as err:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {err}"
            ) from err

        outputs = self._encode(self._model.drift_detected, self._model.estimation)

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters={"content_type": "drift"},
            outputs=outputs,
        )

    def _encode(self, drift_detected, estimation):
        """See base class."""
        outputs = []
        outputs.append(
            NumpyCodec.encode_output(name="drift", payload=np.array([drift_detected]))
        )
        outputs.append(
            NumpyCodec.encode_output(name="stat_val", payload=np.array([estimation]))
        )
        return outputs


class LabelDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._model: river.drift.ADWIN = None
        self._implementation_path = "label.LabelDriftDetector"

    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def save(self, detector, uri):
        """See base class."""
        with open(os.path.join(uri, "label_detector.pkl"), "wb") as file:
            pickle.dump(detector, file)

    def fit(self, data):
        """Fit ADWIN detector.

        The example usage:
        https://riverml.xyz/0.11.1/examples/concept-drift-detection/
        """
        detector = river.drift.ADWIN()

        return detector

    def decode_training_data(self, payload: InferenceRequest):
        """See base class."""
        return NumpyRequestCodec.decode_request(payload)
