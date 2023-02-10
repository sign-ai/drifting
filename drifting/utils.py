"""Useful utils."""

import os
import uuid

PACKAGE_ROOT = os.path.join(os.path.dirname(__file__))


def generate_project_id() -> str:
    """Generate Project ID.

    Default project ID in `drifting` is UUID.
    """
    return str(uuid.uuid4())
