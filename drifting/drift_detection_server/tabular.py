import numpy as np
from alibi_detect.cd import MMDDriftOnline
from alibi_detect.utils.saving import load_detector, save_detector
from mlserver import MLModel, types
from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.errors import InferenceError, MLServerError
from mlserver.types import InferenceRequest
from pydantic.error_wrappers import ValidationError
from sklearn.decomposition import PCA

from drifting.drift_detection_server.detector_core import DetectorCore


class TabularDriftDetector(MLModel):
    async def load(self) -> bool:
        try:
            self._model = load_detector(self.settings.parameters.uri)
        except (
            ValueError,
            FileNotFoundError,
            EOFError,
            NotImplementedError,
            ValidationError,
        ) as e:
            raise MLServerError(
                f"Invalid configuration for model {self._settings.name}: {e}"
            ) from e
        self.ready = True
        return self.ready

    async def predict(
        self, payload: types.InferenceRequest
    ) -> types.InferenceResponse:
        input_data = self.decode_request(
            payload, default_codec=PandasCodec
        )
        try:
            y = self._model.predict(np.array(input_data).flatten())
        except (ValueError, IndexError) as e:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {e}"
            ) from e

        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode_output(
                    name=key, payload=np.array([y["data"][key]])
                )
            )
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )


class TabularDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._model: MMDDriftOnline = None
        self._implementation_path = "tabular.TabularDriftDetector"

    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def save(self, detector, uri):
        """See base class."""
        save_detector(detector, uri)

    def fit(self, data):
        """Fit 

        """
        np.random.seed(0)

        pca = PCA(2)
        pca.fit(data)

        ert = 50
        window_size = 10

        detector = MMDDriftOnline(
            data,
            ert,
            window_size,
            backend="pytorch",
            preprocess_fn=pca.transform,
            n_bootstraps=2500,
        )
        return detector

    def decode_training_data(self, payload: InferenceRequest):
        """See base class."""
        return PandasCodec.decode_request(payload)
