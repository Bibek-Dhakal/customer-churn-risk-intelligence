# Usage Guide

This guide explains how to set up, validate, run, track, and serve the **Customer Churn Risk Intelligence** project using its enterprise-grade MLOps stack.

## 1. Prerequisites

Recommended environment:

* Python 3.10+
* Git
* Docker (for containerization)

The project is designed to run on Windows, macOS, and Linux.

## 2. Clone the Repository

Clone the repository and move into the project directory:

```bash
git clone <your-repository-url>
cd customer-churn-risk-intelligence
```

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, your terminal should indicate that the virtual environment is active.

## 4. Install Dependencies

Install the core data science and enterprise MLOps packages (Pandera, MLflow, FastAPI, Pytest, Skops):

```bash
pip install -r requirements.min.txt
```

## 5. Dataset

The project requires the source Telco Customer Churn CSV.
Place the downloaded dataset at:

```text
data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
```

## 6. Validate the Data Contract

From the project root, run:

```bash
python -m src.validate_data
```

The validation process utilizes **Pandera** to guarantee the incoming CSV aligns with the explicit schema contract defined in `src/schema.py`, preventing silent failures in the pipeline.

## 7. Run Unit Tests (CI/CD Safety)

Validate that domain feature engineering (`src/features.py`) is working correctly by running the automated `pytest` suite:

```bash
pytest tests/
```

## 8. Run the Modeling Pipeline & Track with MLflow

Execute the training pipeline:

```bash
python -m src.train
```

This workflow now automatically tracks executions using **MLflow**. The model is serialized securely using **Skops**, ensuring protection against arbitrary code execution vulnerabilities common in standard Pickle files.

You can view hyperparameter configurations, validation metrics, and registered models through the local tracking UI:

```bash
mlflow ui
```
Navigate to `http://localhost:5000` in your browser.

## 9. Serve the Model (Real-Time FastAPI Endpoint)

Once the model is trained and saved to `artifacts/selected_model.skops`, you can launch the live REST API:

```bash
uvicorn src.serve:app --reload --host 0.0.0.0 --port 8000
```

* **Health Check:** `http://localhost:8000/health`
* **Interactive API Docs:** Navigate to `http://localhost:8000/docs` to test the `/predict` endpoint via Swagger UI. The endpoint accepts a JSON payload corresponding to the Pydantic schema and returns the predicted churn probability and risk segment.

## 10. Run in Docker (Containerization)

Package the serving API into an immutable, deployment-ready Docker image:

```bash
# Build the container
docker build -t customer-churn-api .

# Run the container
docker run -p 8000:8000 customer-churn-api
```

The containerized API will now be securely hosted and exposed on port `8000`.

## 11. Jupyter Notebooks

For exploratory data analysis and visual walkthroughs, refer to the notebooks located in the repository:

**[Browse Notebooks Folder](../notebooks/)**

* `01_customer_retention_eda.ipynb`
* `02_customer_retention_modeling.ipynb`

The notebooks are intended for exploration and presentation. Because the project is modularized, the notebooks seamlessly utilize the `src/` modules, meaning the underlying Pandera data contracts and feature pipelines are applied automatically during your interactive sessions.

## 12. Troubleshooting

### MLflow "Artifact Path Deprecated" Warning
You may see a warning indicating `artifact_path is deprecated. Please use name instead.` This is a harmless warning originating internally from the MLflow library itself and can be ignored.

### Untrusted Types / Numpy Exception
If you see an error regarding `skops.io.exceptions.UntrustedTypesFoundException`, ensure you are using the provided `src.train` script. We explicitly whitelist safe types like `numpy.dtype` during Skops serialization.

### Dataset not found
If you receive an error indicating that the dataset cannot be found, confirm that the file exists at `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`.