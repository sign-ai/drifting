"""CLI for Drift Detection Server."""

import click
import uvicorn

import drifting.app
import drifting.database
import drifting.drifting_logging
import drifting.storage.storage_local
from drifting.version import __version__

DEFAULT_BACKEND_STORE_URI = "./drifting_store"


@click.command(name="serve")
@click.option(
    "--port",
    required=False,
    type=int,
    default=5005,
)
@click.option(
    "--backend-store-uri",
    envvar="DRIFTING_BACKEND_STORE_URI",
    metavar="PATH",
    default=DEFAULT_BACKEND_STORE_URI,
    help="URI to which to persist drift values "
    "SQLAlchemy-compatible database connection strings "
    "(e.g. 'sqlite:///path/to/file.db') or local filesystem URIs "
    "(e.g. 'file:///absolute/path/to/directory'). Only postgres supported. "
    "By default, data will be logged to the ./drifting_store directory.",
)
@click.option(
    "--default-artifact-root",
    envvar="DRIFTING_DEFAULT_ARTIFACT_ROOT",
    metavar="URI",
    default=drifting.storage.storage_local.DEFAULT_ARTIFACT_PATH,
    help="Directory in which to store Drift Detectors."
    "By default, data will be logged to the "
    f"{drifting.storage.storage_local.DEFAULT_ARTIFACT_PATH}.",
)
def serve(port, backend_store_uri, default_artifact_root):
    """Serve Drift Detection Server."""
    drifting.drifting_logging.configure_logger()
    drifting.storage.storage_local.connect_storage()
    drifting.database.connect_database()
    uvicorn.run(drifting.app.app, host="0.0.0.0", port=port)


@click.version_option(version=__version__)
@click.group()
def main():
    """Define main entrypoint for client."""


main.add_command(serve)


if __name__ == "__main__":
    main()
