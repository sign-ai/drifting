"""Useful utils."""

import uuid


def generate_project_id() -> str:
    """Generate Project ID.

    Default project ID in `drifting` is UUID.
    """
    return str(uuid.uuid4())
