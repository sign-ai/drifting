"""Test DriftDetectionServer related functionality."""
import os
import tempfile

import numpy as np
import pytest
from mlserver.codecs import NumpyRequestCodec
from mlserver.settings import ModelSettings

from drifting.drift_detection_server.server import DriftDetectionServer, ModelNameExists


@pytest.mark.asyncio
async def test_model_name_exists_error(model_settings: ModelSettings):
    """Test ModelNameExists error."""
    payload = NumpyRequestCodec.encode_request(np.zeros((10,)))

    with tempfile.TemporaryDirectory() as tmp_dirname:
        server = DriftDetectionServer(model_settings)
        server.settings.parameters.uri = tmp_dirname
        os.makedirs(os.path.join(tmp_dirname, "test"))
        with pytest.raises(ModelNameExists):
            await server.fit(payload=payload, data_type="label", detector_name="test")


@pytest.mark.asyncio
async def test_fit(model_settings: ModelSettings):
    """Test the fit method."""
    payload = NumpyRequestCodec.encode_request(np.zeros((10,)))

    with tempfile.TemporaryDirectory() as tmp_dirname:
        server = DriftDetectionServer(model_settings)
        server.settings.parameters.uri = tmp_dirname

        await server.fit(payload=payload, data_type="label", detector_name="test")

        assert os.path.exists(os.path.join(tmp_dirname, "test"))
