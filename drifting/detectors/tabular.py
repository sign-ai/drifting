"""Tabular drift detector."""

import numpy as np
from alibi_detect.cd import MMDDriftOnline
from alibi_detect.utils.saving import save_detector
from mlserver import types
from mlserver.codecs import PandasCodec
from sklearn.decomposition import PCA

from drifting.detectors.alibi_detector import AlibiDetector
from drifting.detectors.detector_core import DetectorCore


class TabularDriftDetector(AlibiDetector):
    # pylint: disable=missing-class-docstring
    def decode_drift_request(self, inference_request: types.InferenceRequest):
        return np.array(
            super().decode_request(inference_request, default_codec=PandasCodec)
        ).flatten()

    def forward(self, data):
        return self._model.predict(data)


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

    def fit(self, data, ert: int, window_size: int, n_bootstraps: int):
        """Fit"""
        np.random.seed(0)

        pca = PCA(2)
        pca.fit(data)

        detector = MMDDriftOnline(
            data,
            ert,
            window_size,
            backend="pytorch",
            preprocess_fn=pca.transform,
            n_bootstraps=n_bootstraps,
        )
        return detector

    def decode_training_data(self, payload: types.InferenceRequest):
        """See base class."""
        return PandasCodec.decode_request(payload)
