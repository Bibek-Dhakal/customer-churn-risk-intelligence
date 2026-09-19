import pandas as pd
import skops.io as sio
from fastapi import FastAPI, HTTPException

from src.config import SELECTED_MODEL_PATH
from src.features import add_features
from src.schema import CustomerFeatureInput
from src.validate_data import prepare_numeric_columns

app = FastAPI(
    title="Customer Churn Risk Intelligence API",
    description="Real-time churn risk prediction microservice.",
    version="1.0.0"
)

# Attempt to load the pre-trained model artifact securely using skops
try:
    model = sio.load(SELECTED_MODEL_PATH, trusted=["numpy.dtype"])
except Exception:
    model = None


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint to ensure API and Model are operational."""
    if model is None:
        return {"status": "degraded", "message": "Model artifact not found. Please run training pipeline."}
    return {"status": "ok", "message": "Service is healthy and model is loaded."}


@app.post("/predict", tags=["Inference"])
def predict_churn(customer: CustomerFeatureInput):
    """Predict churn probability and assign a risk segment based on customer features."""
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not loaded. Train the model first."
        )

    try:
        # Convert Pydantic payload to Dictionary (handles both Pydantic v1 & v2 smoothly)
        try:
            customer_dict = customer.model_dump()
        except AttributeError:
            customer_dict = customer.dict()

        # Load into DataFrame
        df = pd.DataFrame([customer_dict])

        # Prepare numeric columns (Transforms TotalCharges string to float if needed)
        df = prepare_numeric_columns(df)

        # Apply feature engineering
        df = add_features(df)

        # Generate prediction
        probability = float(model.predict_proba(df)[:, 1][0])

        # Stratify into business risk segments
        if probability >= 0.75:
            risk_segment = "Very High"
        elif probability >= 0.50:
            risk_segment = "High"
        elif probability >= 0.25:
            risk_segment = "Moderate"
        else:
            risk_segment = "Low"

        return {
            "churn_probability": probability,
            "risk_segment": risk_segment,
            "prediction_binary": int(probability >= 0.5)
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")
