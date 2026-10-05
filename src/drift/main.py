from drift.ops import router as ops_router
from fastapi import FastAPI
from drift.detect import detect

app = FastAPI()
app.include_router(ops_router, prefix="/v1")

@app.post("/drift")
def post_drift(body: dict):
    return detect(body["reference"], body["current"])
