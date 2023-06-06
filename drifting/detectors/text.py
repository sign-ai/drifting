"""Tabular drift detector."""

import numpy as np
from alibi_detect.cd import MMDDriftOnline
from alibi_detect.utils.saving import save_detector
from mlserver import types
from mlserver.codecs.string import StringRequestCodec
from mlserver.codecs import NumpyCodec
from mlserver.errors import InferenceError

from drifting.detectors.alibi_detector import AlibiDetector
from drifting.detectors.detector_core import DetectorCore
from mlserver.settings import ModelSettings

import numpy as np
from alibi_detect.utils.saving import load_detector
from mlserver import MLModel, types
from mlserver.errors import InferenceError, MLServerError
from mlserver.codecs import NumpyCodec

# pylint: disable=no-name-in-module
from pydantic.error_wrappers import ValidationError
from alibi_detect.models.pytorch import TransformerEmbedding

from transformers import AutoTokenizer


def prepare_embedding():
    emb_type = "hidden_state"
    n_layers = 6
    layers = [-_ for _ in range(1, n_layers + 1)]
    model_name = "bert-base-cased"
    return TransformerEmbedding(model_name, emb_type, layers)


def process_text(tokenizer, embedding, data):
    max_len = 60
    tokens = tokenizer(
        data, pad_to_max_length=True, max_length=max_len, return_tensors="pt"
    )

    return embedding(tokens)


class TextDriftDetector(AlibiDetector):
    def __init__(self, settings: ModelSettings):
        super().__init__(settings)

        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.embedding = prepare_embedding()

    # pylint: disable=missing-class-docstring
    def decode_drift_request(self, inference_request: types.InferenceRequest):
        return super().decode_request(
            inference_request, default_codec=StringRequestCodec
        )

    def forward(self, data):
        x_emb = process_text(tokenizer=self.tokenizer, embedding=self.embedding, data=data)
        return self._model.predict(x_emb.squeeze().detach().numpy())

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


class TextDriftDetectorCore(DetectorCore):
    """See base class."""

    def __init__(self):
        """See base class."""
        self._model: MMDDriftOnline = None
        self._implementation_path = "text.TextDriftDetector"
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        self.embedding = prepare_embedding()
        
    @property
    def implementation_path(self) -> str:
        """See base class."""
        return self._implementation_path

    def save(self, detector, uri):
        """See base class."""
        save_detector(detector, uri)

    def fit(self, data):
        """Fit"""
        x_emb = process_text(tokenizer=self.tokenizer, embedding=self.embedding, data=data)

        ert = 400
        window_size = 40

        detector = MMDDriftOnline(
            x_emb.detach().numpy(),
            ert,
            window_size,
            backend="pytorch",
            n_bootstraps=7000,
        )
        return detector

    def decode_training_data(self, payload: types.InferenceRequest):
        """See base class."""
        return StringRequestCodec.decode_request(payload)
