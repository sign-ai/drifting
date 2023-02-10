import numpy as np
from alibi_detect.cd import MMDDriftOnline
from alibi_detect.utils.saving import load_detector, save_detector
from mlserver import MLModel, types
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.errors import InferenceError, MLServerError
from mlserver.types import InferenceRequest
from pydantic.error_wrappers import ValidationError
from sklearn.decomposition import PCA
from mlserver.codecs import PandasCodec

implementation_path = "drifting.drift_detection_server.tabular.TabularDetector"
saving_function = save_detector


class TabularDetector(MLModel):
    async def load(self) -> bool:
        try:
            self._model = load_detector(model_uri)
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

    async def predict(self, payload: types.InferenceRequest) -> types.InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        try:
            y = self._model.predict(np.array(input_data))
        except (ValueError, IndexError) as e:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {e}"
            ) from e

        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode_output(name=key, payload=np.array([y["data"][key]]))
            )
        return types.InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )

    def decode(self, payload: InferenceRequest):
        return PandasCodec.decode_request(payload)

    def fit(self, data):
        np.random.seed(0)

        pca = PCA(2)
        pca.fit(data)

        ert = 50
        window_size = 10

        detector = MMDDriftOnline(
            data,
            ert,
            window_size,
            backend="tensorflow",
            preprocess_fn=pca.transform,
            n_bootstraps=2500,
        )
        return detector

    def save(detector, path):
        save_detector(detector, path)
