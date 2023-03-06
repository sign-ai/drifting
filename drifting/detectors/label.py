"""Label drift detection.

Label drift detection works both for classification and regression labels.
"""

import numpy as np
from alibi_detect.cd import CVMDriftOnline
from alibi_detect.utils.saving import load_detector, save_detector
from mlserver import MLModel, types
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.errors import InferenceError, MLServerError

# pylint: disable=no-name-in-module
from pydantic.error_wrappers import ValidationError

from drifting.detectors.detector_core import DetectorCore


class LabelDriftDetector(MLModel):
    """Class used during inference."""

    async def load(self) -> bool:
        # pylint: disable=attribute-defined-outside-init
        try:
            self._model = load_detector(self.settings.parameters.uri)
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
        self.ready = True
        return self.ready

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyCodec)
        try:
            output = self._model.predict(np.array(input_data).flatten())
        except (ValueError, IndexError) as err:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {err}"
            ) from err

        outputs = []
        for key in output["data"]:
            val = output["data"][key]
            if isinstance(val, np.ndarray):
                val = np.nan_to_num(val)
            outputs.append(NumpyCodec.encode_output(name=key, payload=np.array([val])))
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=output["meta"],
            outputs=outputs,
        )


class LabelDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._model: CVMDriftOnline = None
        self._implementation_path = "label.LabelDriftDetector"

    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def save(self, detector, uri):
        """See base class."""
        save_detector(detector, uri)

    def fit(self, data):
        """Fit CVMDriftOnline detector."""
        ert = 150
        window_sizes = [20, 40]
        detector = CVMDriftOnline(data.flatten(), ert, window_sizes)

        return detector

    def decode_training_data(self, payload: types.InferenceRequest):
        """See base class."""
        return NumpyRequestCodec.decode_request(payload)
