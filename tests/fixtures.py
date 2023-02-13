"""Fixtures for the tests."""
import os

import pytest
from mlserver.settings import ModelSettings

from drifting.utils import PACKAGE_ROOT

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")

@pytest.fixture
def model_settings() -> ModelSettings:
    """Mock the settings for MLModel."""
    settings_path = os.path.join(PACKAGE_ROOT, "drift_detection_server", "model-settings.json")
    settings = ModelSettings.parse_file(settings_path)

    return settings
