import pytest

from drifting.cli.cli import load_all_settings


@pytest.mark.asyncio
async def test_load_server():
    # Point to a folder with no models
    _, models_settings = await load_all_settings("./")

    assert len(models_settings) == 1
