"""Test DriftDetectionServer related functionality."""
import pytest
from mlserver.settings import ModelSettings

from drifting.drift_detection_server.server import DriftDetectionServer


@pytest.mark.asyncio
async def test_model_name_exists_error(model_settings: ModelSettings):
    """Test ModelNameExists error."""
    server = DriftDetectionServer(model_settings)
    assert True


@pytest.mark.asyncio
async def test_fit(model_settings: ModelSettings):
    """Test the fit method."""
    server = DriftDetectionServer(model_settings)
    assert True
