"""Drift Detection Server."""

from typing import Union, List, Any

import numpy as np
import prometheus_fastapi_instrumentator as pfi
import pydantic
from fastapi import FastAPI

import drifting.drift_detector.drift_detector as dd
import drifting.utils

app = FastAPI()

pfi.Instrumentator().instrument(app).expose(app)


class Body(pydantic.BaseModel):
    """The data to Drift Detection Server is send in body and always
    consist of vector."""

    data: List[Union[str, float]]


@app.get("/")
def read_root():
    """Get health check response."""
    return {"Hello": "World"}


@app.post("/fit")
def fit(body: Body, project_id: Union[str, None] = None):
    """Fit Drift Detector."""
    if project_id is None:
        project_id = drifting.utils.generate_project_id()

    drift_detector = dd.get_by_id(project_id)
    drift_detector.fit(body.vector)

    return 200


@app.post("/predict")
def predict(body: Body, project_id: str):
    """Predict drift."""

    drift_detector = dd.get_by_id(project_id)
    prediction = drift_detector.predict(body.vector)

    return 200
