"""CLI for Drift Detection Server."""

import logging

import click


@click.command(name="serve")
@click.option(
    "--test",
    required=False,
    type=bool,
    default=False,
)
def serve(test):
    """Serve Drift Detection Server."""
    print(test)
    logging.basicConfig()
