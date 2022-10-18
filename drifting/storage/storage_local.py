"""Artifacts Storage for DDS."""

import os

import pickledb

from drifting.drifting_logging import logger

DEFAULT_ARTIFACT_PATH = "./drifting_store"


def connect_storage():
    """Connect storage."""
    pass


def init_local_store():
    """Initialize store.db with the info about available Drift Detectors."""
    if os.path.exists(DEFAULT_ARTIFACT_PATH):
        logger.info(
            "%s exists, loading Drift Detectors", DEFAULT_ARTIFACT_PATH
        )
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
