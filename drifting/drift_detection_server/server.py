"""Drift Detection Server."""

import os
from dataclasses import dataclass
from enum import Enum

from fastapi import HTTPException, status  # pylint: disable=no-name-in-module
from fastapi.responses import JSONResponse
from mlserver import MLModel
from mlserver.handlers.custom import custom_handler
from mlserver.types import InferenceRequest

from drifting.detectors.detector_core import DetectorCore
from drifting.storage.persistor import persist

FIT_REST_PATH = "/v2/models/fit/"

ALLOWED_ALGORITHMS = ["MMDDriftOnline"]


class ModelNameExists(HTTPException):
    """Raise when trying to train a model that already exists."""

    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code, detail)


class DriftType(Enum):
    """Drift types implemented by DriftDetectionServer."""

    LABEL = "label"
    TABULAR = "tabular"
    SEQUENTIAL = "sequential"
    IMAGE = "image"
    DUMMY = "dummy"


@dataclass
class Params:
    """Request parameters."""

    drift_type: DriftType
    detector_name: str

    def dict(self):
        """Represent params as string."""
        return {
            "detector_name": self.detector_name,
            "drift_type": self.drift_type.value,
        }


class DriftDetectionServer(MLModel):
    """Drift Detection Server - main drifting package entrypoint.

    Drift Detection Server is in fact a separate `MLModel` with additional
    fit method that allows to fit the new detectors.
    """

    async def load(self) -> bool:
        """See base class."""
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> float:
        """Predict function is not used in DriftDetectionServer.

        The function is necessary as `DriftDetectionServer` inherits from
        MLModel. mlserver manages all the model repository and all regular
        detectors and at the same time it exposes fit method that allows to fit
        new detectors."""
        raise ValueError(
            "DriftDetectionServer is used only for adding the new models and "
            f"versions using {FIT_REST_PATH} endpoint"
        )

    def _provide_trainer(self, drift_type: str) -> DetectorCore:
        """Provide drift detection object."""
        # pylint: disable=import-outside-toplevel,no-else-raise

        if drift_type == DriftType.SEQUENTIAL.value:
            raise NotImplementedError(f"drift_type {drift_type} is not implemented yet")
        elif drift_type == DriftType.IMAGE.value:
            raise NotImplementedError(f"drift_type {drift_type} is not implemented yet")
        elif drift_type == DriftType.TABULAR.value:
            from drifting.detectors.tabular import TabularDriftDetectorCore

            trainer = TabularDriftDetectorCore()  # type: ignore
        elif drift_type == DriftType.LABEL.value:
            from drifting.detectors.label import LabelDriftDetectorCore

            trainer = LabelDriftDetectorCore()  # type: ignore
        elif drift_type == DriftType.DUMMY.value:
            from drifting.detectors.dummy import DummyDriftDetectorCore

            trainer = DummyDriftDetectorCore()  # type: ignore

        else:
            raise HTTPException(
                status_code=404,
                detail="drift_type has to be one of "
                '["sequential", "image", "tabular", "label"]',
            )
        return trainer

    @custom_handler(rest_path=FIT_REST_PATH)
    async def fit(
        self,
        payload: InferenceRequest,
        drift_type: str,
        detector_name: str,
    ) -> JSONResponse:
        """Fit the detector.

        Based on drift_type, the appropriate detector is provided, fitted, and
        persisted.
        After fitting, algorithm is not automatically loaded.
        """
        if os.path.exists(os.path.join(self.settings.parameters.uri, detector_name)):
            return JSONResponse(
                status_code=409,
                content={
                    "message": f"Model with name '{detector_name}' already exists."
                },
            )

        trainer = self._provide_trainer(drift_type)

        data = trainer.decode_training_data(payload)
        detector = trainer.fit(data)

        persist(
            destination_uri=self.settings.parameters.uri,
            implementation_path=trainer.implementation_path,
            detector=detector,
            saving_function=trainer.save,
            detector_name=detector_name,
        )

        return JSONResponse(
            status_code=200,
            content={"message": f"Successfully fitted model '{detector_name}'"},
        )
