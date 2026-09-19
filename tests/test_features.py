import pandas as pd
import pytest
from src.features import add_features

def test_add_features_service_adoption():
    """Test that the optional service adoption features are calculated correctly."""
    data = {
        "TotalCharges": [100.0, 50.0],
        "tenure": [10, 5],
        "MonthlyCharges": [10.0, 10.0],
        "OnlineSecurity": ["Yes", "No"],
        "OnlineBackup": ["Yes", "No"],
        "DeviceProtection": ["No", "No"],
        "TechSupport": ["No", "No"],
        "StreamingTV": ["No", "No"],
        "StreamingMovies": ["No", "No"],
        "Contract": ["Month-to-month", "Two year"],
        "PaymentMethod": ["Electronic check", "Mailed check"]
    }
    df = pd.DataFrame(data)
    
    df_out = add_features(df)
    
    assert "ServiceAdoptionCount" in df_out.columns
    assert "ServiceAdoptionRate" in df_out.columns
    
    # First customer has 2 services (Security, Backup)
    assert df_out["ServiceAdoptionCount"].iloc[0] == 2
    # Second customer has 0 services
    assert df_out["ServiceAdoptionCount"].iloc[1] == 0


def test_add_features_contract_and_payment():
    """Test engineered boolean contract and payment behavior flags."""
    data = {
        "TotalCharges": [1200.0, 300.0],
        "tenure": [12, 3],
        "MonthlyCharges": [100.0, 100.0],
        "OnlineSecurity": ["Yes", "No"],
        "OnlineBackup": ["No", "No"],
        "DeviceProtection": ["No", "No"],
        "TechSupport": ["No", "No"],
        "StreamingTV": ["No", "No"],
        "StreamingMovies": ["No", "No"],
        "Contract": ["Month-to-month", "Two year"],
        "PaymentMethod": ["Electronic check", "Bank transfer (automatic)"]
    }
    df = pd.DataFrame(data)
    
    df_out = add_features(df)
    
    # Check rolling contract flags
    assert df_out["IsRollingContract"].iloc[0] == 1
    assert df_out["IsRollingContract"].iloc[1] == 0
    
    # Check electronic check detection
    assert df_out["UsesElectronicPayment"].iloc[0] == 1
    assert df_out["UsesElectronicPayment"].iloc[1] == 0
    
    # Check financial exposure calculation
    assert df_out["LifetimeSpendPerTenure"].iloc[0] == 100.0  # 1200 / 12
    assert df_out["LifetimeSpendPerTenure"].iloc[1] == 100.0  # 300 / 3