"""Artifacts Storage for DDS."""

from typing import Callable, List


class DriftDetectionServerStore:
    """Manage the information about the existing and active models.

    DriftDetectionServerStore is operating on two json files with key-value
    pairs.
    """

    def __init__(self, init_storage_func: Callable):
        """Initialize store with the info about available Drift Detectors."""
        self.active_db, self.store_db = init_storage_func()

    def add_drift_detector(self):
        """Add Drift Detector."""
        pass

    def remove_drift_detector(self):
        """Remove Drift Detector."""
        pass

    def load_drift_detector(self, project_id: str):
        """Load Drift Detector."""
        pass

    def unload_drift_detectors(self, project_id: str):
        """Unload Drift Detector."""
        pass

    def get_drift_detector(self, project_id: str) -> str:
        """Get Drift Detector path from project_id."""
        pass

    def get_drift_detectors(self, only_active: bool = True) -> List[str]:
        """Get all Drift Detectors paths."""
        pass
