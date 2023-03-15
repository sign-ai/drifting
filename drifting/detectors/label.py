"""Label drift detection.

Label drift detection works both for classification and regression labels.
"""

from alibi_detect.cd import CVMDriftOnline
from alibi_detect.utils.saving import save_detector
from mlserver import types
from mlserver.codecs import NumpyRequestCodec

from drifting.detectors.alibi_detector import AlibiDetector
from drifting.detectors.detector_core import DetectorCore


class LabelDriftDetector(AlibiDetector):
    # pylint: disable=missing-class-docstring
    def decode_drift_request(self, inference_request: types.InferenceRequest):
        return super().decode_request(
            inference_request, default_codec=NumpyRequestCodec
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
        ert = 300
        window_sizes = [80, 120]
        detector = CVMDriftOnline(data.flatten(), ert, window_sizes)

        return detector

    def decode_training_data(self, payload: types.InferenceRequest):
        """See base class."""
        return NumpyRequestCodec.decode_request(payload)
