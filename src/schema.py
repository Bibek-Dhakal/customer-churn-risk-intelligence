import pandera.pandas as pa
from pydantic import BaseModel, Field

# ------------------------------------------------------------------
# Pandera Schema: Enforces data contract on raw datasets
# ------------------------------------------------------------------
RawDataSchema = pa.DataFrameSchema({
    "customerID": pa.Column(str, required=True),
    "gender": pa.Column(str, checks=pa.Check.isin(["Male", "Female"])),
    "SeniorCitizen": pa.Column(int, checks=pa.Check.isin([0, 1])),
    "Partner": pa.Column(str, checks=pa.Check.isin(["Yes", "No"])),
    "Dependents": pa.Column(str, checks=pa.Check.isin(["Yes", "No"])),
    "tenure": pa.Column(int, checks=pa.Check.ge(0)),
    "PhoneService": pa.Column(str, checks=pa.Check.isin(["Yes", "No"])),
    "MultipleLines": pa.Column(str),
    "InternetService": pa.Column(str),
    "OnlineSecurity": pa.Column(str),
    "OnlineBackup": pa.Column(str),
    "DeviceProtection": pa.Column(str),
    "TechSupport": pa.Column(str),
    "StreamingTV": pa.Column(str),
    "StreamingMovies": pa.Column(str),
    "Contract": pa.Column(str),
    "PaperlessBilling": pa.Column(str, checks=pa.Check.isin(["Yes", "No"])),
    "PaymentMethod": pa.Column(str),
    "MonthlyCharges": pa.Column(float, checks=pa.Check.ge(0)),
    "TotalCharges": pa.Column(str, nullable=True),
    "Churn": pa.Column(str, checks=pa.Check.isin(["Yes", "No"]), required=False)
})

# ------------------------------------------------------------------
# Pydantic Schema: Enforces data contract for real-time API requests
# ------------------------------------------------------------------
class CustomerFeatureInput(BaseModel):
    gender: str = Field(..., description="Customer gender", examples=["Female"])
    SeniorCitizen: int = Field(..., description="Senior citizen indicator (0 or 1)", examples=[0])
    Partner: str = Field(..., description="Partner indicator", examples=["Yes"])
    Dependents: str = Field(..., description="Dependents indicator", examples=["No"])
    tenure: int = Field(..., description="Number of months with the company", examples=[12])
    PhoneService: str = Field(..., description="Phone service indicator", examples=["Yes"])
    MultipleLines: str = Field(..., description="Multiple lines indicator", examples=["No"])
    InternetService: str = Field(..., description="Internet service type", examples=["DSL"])
    OnlineSecurity: str = Field(..., description="Online security indicator", examples=["Yes"])
    OnlineBackup: str = Field(..., description="Online backup indicator", examples=["No"])
    DeviceProtection: str = Field(..., description="Device protection indicator", examples=["No"])
    TechSupport: str = Field(..., description="Tech support indicator", examples=["Yes"])
    StreamingTV: str = Field(..., description="Streaming TV indicator", examples=["No"])
    StreamingMovies: str = Field(..., description="Streaming movies indicator", examples=["No"])
    Contract: str = Field(..., description="Contract term", examples=["Month-to-month"])
    PaperlessBilling: str = Field(..., description="Paperless billing indicator", examples=["Yes"])
    PaymentMethod: str = Field(..., description="Payment method", examples=["Electronic check"])
    MonthlyCharges: float = Field(..., description="Monthly charge amount", examples=[49.95])
    TotalCharges: str = Field(..., description="Total accumulated charge", examples=["599.40"])