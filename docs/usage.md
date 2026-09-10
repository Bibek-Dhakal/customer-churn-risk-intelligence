## How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
cd customer-churn-risk-intelligence
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.min.txt
```

### 4. Add the dataset

Place the required training and test datasets in:

```text
data/
└── raw/
    ├── train.csv
    └── test.csv
```

The dataset is not included in this repository.

### 5. Run the notebooks

Open the notebooks in Jupyter Notebook, JupyterLab, or VS Code:

```text
notebooks/
├── 01_customer_retention_eda.ipynb
└── 02_customer_retention_modeling.ipynb
```

Run the notebooks from top to bottom.

The modeling notebook trains the candidate models, evaluates them using stratified cross-validation, compares validation
performance, selects the strongest model under the chosen metric, and generates churn probability predictions.

### 6. Generated outputs

Modeling outputs are written to the project's artifact/output locations defined by the implementation.

Because evaluation metrics and model selection are calculated during execution, results shown in the notebooks reflect
the actual run rather than predetermined values.
