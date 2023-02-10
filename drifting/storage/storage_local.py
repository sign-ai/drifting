"""Artifacts Storage for DDS."""

import os
from typing import Callable, List

# import pickledb

from drifting.drifting_logging import logger
import drifting.storage.store

DEFAULT_ARTIFACT_PATH = "./drifting_store"


class LocalStorage(drifting.storage.store.DriftDetectionServerStore):
    """Manage the information about the existing and active models.

    DriftDetectionServerStore is operating on two json files with key-value
    pairs.
    """

    def __init__(self, path):
        """Initialize store with the info about available Drift Detectors."""
        self.active_db, self.store_db = self._init_storage()

    def _init_storage(self):
        """Initialize storage with the info about available Drift Detectors."""
        if os.path.exists(DEFAULT_ARTIFACT_PATH):
            logger.info("%s exists, loading Drift Detectors", DEFAULT_ARTIFACT_PATH)
            store_path = os.path.join(DEFAULT_ARTIFACT_PATH, "store.db")
            if not os.path.exists(store_path):
                raise NotADirectoryError("store.db doesn't exist.")

            active_path = os.path.join(DEFAULT_ARTIFACT_PATH, "active.db")
            if not os.path.exists(active_path):
                raise NotADirectoryError("active.db doesn't exist.")

        else:
            logger.info("%s doesn't exists, creating a new directory")
            os.mkdir(DEFAULT_ARTIFACT_PATH, exist_ok=True)

        active_db = pickledb.load(active_path, False)
        store_db = pickledb.load(store_path, False)

        return store_db, active_db

    def add_drift_detector(self, project_id: str):
        """Add Drift Detector."""
        self.store_db.set(project_id, project_id)
        self.store_db.dump()

        self.active_db.set(project_id, True)
        self.active_db.dump()

    def remove_drift_detector(self, project_id: str):
        """Remove Drift Detector."""
        self.store_db.rem(project_id)
        self.active_db.rem(project_id)
        logger.info("%s removed", project_id)

    def load_drift_detector(self, project_id: str):
        """Load Drift Detector."""
        self.active_db.set(project_id, True)
        self.active_db.dump()

    def unload_drift_detectors(self, project_id: str):
        """Unload Drift Detector."""
        self.active_db.set(project_id, False)
        self.active_db.dump()

    def get_drift_detector(self, project_id: str) -> str:
        """Get Drift Detector path from project_id."""
        return None

    def get_drift_detectors(self, only_active: bool = True) -> List[str]:
        """Get all Drift Detectors paths."""
        return None
