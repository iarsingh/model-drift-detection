from fastapi import FastAPI
from drift.detect import detect

app = FastAPI()

@app.post("/drift")
def post_drift(body: dict):
    return detect(body["reference"], body["current"])
