"""Drift Detection Server."""

from fastapi import HTTPException  # pylint: disable=no-name-in-module
from mlserver import MLModel
from mlserver.handlers.custom import custom_handler
from mlserver.types import InferenceRequest

from drifting.storage.persistor import persist


FIT_REST_PATH = "/v2/models/fit/"

ALLOWED_ALGORITHMS = ["MMDDriftOnline"]


class DriftDetectionServer(MLModel):
    """Drift Detection Server - main drifting package entrypoint.

    Drift Detection Serveris in fact a separate `MLModel` with additional
    fit method that allows to fit the new detectors.
    """

    async def load(self) -> bool:
        """See base class."""
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> float:
        raise ValueError(
            "DriftDetectionServer is used only for adding the new models and "
            f"versions using {FIT_REST_PATH} endpoint"
        )

    def _provide_trainer(self, data_type: str):
        """Provide drift detection object."""
        # pylint: disable=import-outside-toplevel

        if data_type == "sequential":
            pass
        elif data_type == "image":
            pass
        elif data_type == "tabular":
            pass
        elif data_type == "label":
            from drifting.drift_detection_server.label import (
                LabelDriftDetectorCore,
            )

            trainer = LabelDriftDetectorCore()
        else:
            raise HTTPException(
                status_code=404,
                detail="data_type has to be one of "
                '["sequential", "image", "tabular", "label"]',
            )
        return trainer

    @custom_handler(rest_path=FIT_REST_PATH)
    async def fit(
        self,
        payload: InferenceRequest,
        data_type: str = "tabular",
        detector_name: str = "detector_name",
    ) -> str:
        """Fit the detector.

        Based on data_type, the appropriate detector is provided, fitted, and
        persisted.
        After fitting, algorithm is not automatically loaded.
        """
        trainer = self._provide_trainer(data_type)

        data = trainer.decode(payload)
        detector = trainer.fit(data)

        persist(
            destination_uri=self.settings.parameters.uri,
            implementation_path=trainer.implementation_path,
            detector=detector,
            saving_function=trainer.save,
            detector_name=detector_name,
        )

        return "Successfully fitted model."