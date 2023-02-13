"""Drifting logging utins."""
import logging
import sys
from logging import Formatter, StreamHandler

logger = logging.getLogger("drifting")


def configure_logger():
    """Configure logger."""
    logger.setLevel(logging.INFO)
    stream_handler = StreamHandler(sys.stdout)
    formatter = Formatter("%(asctime)s [%(name)s] %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger
