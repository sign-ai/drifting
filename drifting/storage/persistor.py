"""Tools for creating the detector package."""
import os
import shutil
from pathlib import Path


import tempfile
from typing import Callable
from drifting.utils import PACKAGE_ROOT


def create_detector_package(
    tmp_dirname,
    detector,
    implementation_path: str,
    saving_function: Callable,
    detector_name: str,
) -> str:
    """Construct model package in tmp directory."""
    # copy this file to the new model location
    # create "model-settings.json" in the new model location
    #
    # Copy implementation to the new detector package
    implementation_file = "/".join(implementation_path.split(".")[:-1]) + ".py"
    source_path = os.path.join(PACKAGE_ROOT, "detectors", implementation_file)
    destination_path = os.path.join(
        tmp_dirname, implementation_file.rsplit("/", maxsplit=1)[-1]
    )
    shutil.copyfile(source_path, destination_path)

    # Add model-settings.json
    with open(
        os.path.join(tmp_dirname, "model-settings.json"), "w", encoding="utf-8"
    ) as setting_file:
        with open(
            os.path.join(PACKAGE_ROOT, "storage", "model-settings-example.json"),
            encoding="utf-8",
        ) as template_file:
            content = template_file.read()

        content = content.replace("__IMPLEMENTATION__", implementation_path)
        content = content.replace("__NAME__", detector_name)
        setting_file.write(content)

    # Save the detector parameters
    saving_function(detector, os.path.join(tmp_dirname))

    return tmp_dirname


def persist(
    destination_uri,
    detector,
    implementation_path,
    saving_function,
    detector_name,
):
    """Construct detector package and move it to desired location."""
    destination_uri = Path(destination_uri)

    with tempfile.TemporaryDirectory() as tmp_dirname:
        create_detector_package(
            tmp_dirname=tmp_dirname,
            detector=detector,
            implementation_path=implementation_path,
            saving_function=saving_function,
            detector_name=detector_name,
        )

        # Move package path to target location
        if destination_uri.is_dir():
            shutil.copytree(tmp_dirname, os.path.join(destination_uri, detector_name))
