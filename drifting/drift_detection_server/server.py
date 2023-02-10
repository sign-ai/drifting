from fastapi import HTTPException
from mlserver import MLModel
from mlserver.handlers.custom import custom_handler
from mlserver.types import InferenceRequest

from drifting.storage.persistor import persist


fit_rest_path = "/v2/models/fit/"

ALLOWED_ALGORITHMS = ["MMDDriftOnline"]


class DriftDetectionServer(MLModel):
    async def load(self) -> bool:
        self.ready = True
        self.destination_uri = self.settings.parameters.uri
        return self.ready

    async def predict(self) -> float:
        raise ValueError(
            f"DriftDetectionServer is used only for adding the new models and versions using {fit_rest_path} endpoint"
        )

    def _provide_trainer(self, data_type: str):
        """"""

        if data_type == "sequential":
            pass
        elif data_type == "image":
            pass
        elif data_type == "tabular":
            from drifting.drift_detection_server.tabular import TabularDetector

            trainer = TabularDetector()
        elif data_type == "label":
            from drifting.drift_detection_server.label import (
                LabelDriftDetectorTrainer,
            )

            trainer = LabelDriftDetectorTrainer()
        else:
            raise HTTPException(
                status_code=404,
                detail=f'data_type has to be one of ["MMDDriftOnline", ]',
            )
        return trainer

    @custom_handler(rest_path=fit_rest_path)
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
            destination_uri=self.destination_uri,
            implementation_path=trainer.implementation_path,
            detector=detector,
            saving_function=trainer.save,
            detector_name=detector_name,
        )

        return "Successfully fitted model."
