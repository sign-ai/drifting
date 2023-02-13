import os
from typing import List

from mlserver.settings import ModelSettings
from drifting.utils import PACKAGE_ROOT


async def overwrite_mlserver_settings(settings, models_settings):
    return settings, models_settings


async def drift_detection_server_settings(folder) -> List[ModelSettings]:
    """Add DriftDetectionServer to the individual models."""
    drift_detection_settings = ModelSettings.parse_file(
        os.path.join(PACKAGE_ROOT, "drift_detection_server", "model-settings.json")
    )
    drift_detection_settings.parameters.uri = folder
    return [drift_detection_settings]
