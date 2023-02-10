"""Command-line interface to manage drifting server and models."""

import asyncio
from functools import wraps

import click
from mlserver import MLServer
from mlserver.cli.serve import load_settings
from mlserver.utils import install_uvloop_event_loop

from drifting.cli.clli_utils import (
    drift_detection_server_settings,
    overwrite_mlserver_settings,
)
from drifting.drifting_logging import configure_logger
from drifting.storage.storage_local import DEFAULT_ARTIFACT_PATH, LocalStorage

DEFAULT_BACKEND_STORE_URI = "./drifting_store"


def click_async(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


async def load_all_settings(folder: str):
    """Load MLServer settings and all models' settings."""
    all_models_settings = await drift_detection_server_settings(folder)
    settings, models_settings = await load_settings(folder)
    settings, models_settings = await overwrite_mlserver_settings(
        settings, models_settings
    )
    all_models_settings.extend(models_settings)

    return settings, all_models_settings


@click.group()
@click.version_option()
def root():
    """
    Command-line interface to manage MLServer models.
    """
    pass


# @click.option(
#     "--backend-store-uri",
#     envvar="DRIFTING_BACKEND_STORE_URI",
#     metavar="PATH",
#     default=DEFAULT_BACKEND_STORE_URI,
#     help="URI to which to persist drift values "
#     "SQLAlchemy-compatible database connection strings "
#     "(e.g. 'sqlite:///path/to/file.db') or local filesystem URIs "
#     "(e.g. 'file:///absolute/path/to/directory'). Only postgres supported. "
#     "By default, data will be logged to the "
#     f"{DEFAULT_BACKEND_STORE_URI} directory.",
# )
# @click.option(
#     "--default-artifact-root",
#     envvar="DRIFTING_DEFAULT_ARTIFACT_ROOT",
#     metavar="URI",
#     default=DEFAULT_ARTIFACT_PATH,
#     help="Directory in which to store Drift Detectors."
#     f"By default, data will be logged to the {DEFAULT_ARTIFACT_PATH}.",
# )
@click.option(
    "--port",
    required=False,
    type=int,
    default=5005,
)
@root.command("start")
@click.argument("folder")
@click_async
async def start(folder: str, port: int):
    """
    Start serving a machine learning model with MLServer.
    """
    settings, all_models_settings = await load_all_settings(folder)
    server = MLServer(settings)
    await server.start(all_models_settings)


def main():
    configure_logger()
    install_uvloop_event_loop()
    root()


if __name__ == "__main__":
    main()
