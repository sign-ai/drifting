"""Label drift detection.

Label drift detection works both for classification and regression labels.
"""

import numpy as np
from alibi_detect.utils.saving import load_detector
from mlserver import MLModel, types
from mlserver.errors import InferenceError, MLServerError
from mlserver.codecs import NumpyCodec

# pylint: disable=no-name-in-module
from pydantic.error_wrappers import ValidationError


class AlibiDetector(MLModel):
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
        input_data = self.decode_drift_request(payload)
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

    def decode_drift_request(self, inference_request: types.InferenceRequest):
        """Decode the request according to drift codec."""
        raise NotImplementedError
