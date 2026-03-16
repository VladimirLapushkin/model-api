import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.model import create_spark, load_model, predict_one
from app.schemas import PredictRequest, PredictResponse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Fraud Detection API", version="1.0.0")

spark = None
model = None


@app.on_event("startup")
def startup_event():
    global spark, model

    model_path = os.getenv("YC_CLEAN_BUCKET_PATH")
    s3_endpoint = os.getenv("S3_ENDPOINT_URL")
    access_key = os.getenv("YC_CLEAN_BUCKET_AK")
    secret_key = os.getenv("YC_CLEAN_BUCKET_SK")

    if not all([model_path, s3_endpoint, access_key, secret_key]):
        raise RuntimeError(
            "Missing env vars: S3_ENDPOINT_URL, YC_CLEAN_BUCKET_AK, YC_CLEAN_BUCKET_SK, YC_CLEAN_BUCKET_PATH"
        )

    spark = create_spark(s3_endpoint, access_key, secret_key)
    model = load_model(spark, model_path)
    logger.info("Model loaded from %s", model_path)


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded succesful": model is not None}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None or spark is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    try:
        result = predict_one(spark, model, request)
        return PredictResponse(**result)
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e))
