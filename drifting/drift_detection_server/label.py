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
from pydantic.error_wrappers import ValidationError


class LabelDriftDetector(MLModel):
    async def load(self) -> bool:
        self.uri = self.settings.parameters.uri
        try:
            with open(os.path.join(self.uri, "label_detector.pkl"), "rb") as f:
                self._model: river.drift.ADWIN = pickle.load(f)
            self.ready = True
        except (
            ValueError,
            FileNotFoundError,
            EOFError,
            NotImplementedError,
            ValidationError,
        ) as err:
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

        outputs = []
        outputs.append(
            NumpyCodec.encode_output(
                name="drift", payload=np.array([self._model.drift_detected])
            )
        )
        outputs.append(
            NumpyCodec.encode_output(
                name="stat_val", payload=np.array([self._model.estimation])
            )
        )

        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters={"content_type": "drift"},
            outputs=outputs,
        )


class LabelDriftDetectorCore:
    """See base class."""

    implementation_path = "label.LabelDriftDetector"

    def load(self, uri) -> bool:
        with open(
            os.path.join(uri, "label_detector.pkl"),
            "rb",
        ) as f:
            self._model: river.drift.ADWIN = pickle.load(f)
        return self._model

    def save(self, detector, path):
        """See base class."""
        with open(os.path.join(path, "label_detector.pkl"), "wb") as f:
            pickle.dump(detector, f)

    def predict(self, input_data):
        self._model.update(input_data)
        return self._model.drift_detected, self._model.estimation

    def fit(self, data):
        """Fit ADWIN detector.

        The example usage:
        https://riverml.xyz/0.11.1/examples/concept-drift-detection/
        """
        detector = river.drift.ADWIN()

        return detector

    def decode(self, payload: InferenceRequest):
        """See base class."""
        return NumpyRequestCodec.decode_request(payload)

    def encode(self, drift_detected, estimation):
        outputs = []
        outputs.append(
            NumpyCodec.encode_output(name="drift", payload=np.array([drift_detected]))
        )
        outputs.append(NumpyCodec.encode_output(name="stat_val", payload=np.array([])))
        return outputs
