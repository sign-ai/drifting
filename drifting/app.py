"""Drift Detection Server."""

import prometheus_fastapi_instrumentator as pfi
from fastapi import FastAPI

app = FastAPI()

pfi.Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    """Get health check response."""
    return {"Hello": "World"}
