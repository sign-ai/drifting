"""Test cli-related utils."""
import tempfile

import pytest

from drifting.cli.cli import load_all_settings


@pytest.mark.asyncio
async def test_load_server():
    """Point to a folder with no models and create only DriftDetectionServer."""

    with tempfile.TemporaryDirectory() as tmp_dirname:
        _, models_settings = await load_all_settings(tmp_dirname)

    assert len(models_settings) == 1
