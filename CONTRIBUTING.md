# Contributing Guidelines

First off, thank you for considering contributing to the **Customer Churn Risk Intelligence** pipeline! 

## Code Style & Linting
This project enforces a strict code quality standard using [Ruff](https://docs.astral.sh/ruff/).
All code changes must pass linting and formatting before being merged. 
Please refer to the [CODE_QUALITY.md](CODE_QUALITY.md) document for detailed instructions on how to run checks locally and set up pre-commit hooks.

## Testing
We use `pytest` for all unit and integration testing. 
- Ensure that you add or update tests in the `tests/` directory for any new features or bug fixes.
- Run the full test suite locally before pushing your changes:
  ```bash
  pytest
  ```

## Pull Request Process
1. **Branching:** Create a feature branch from `main` (e.g., `feat/add-new-model` or `fix/schema-validation`).
2. **Commit Messages:** Follow the Conventional Commits format (e.g., `feat: integrate SHAP explainability` or `fix: resolve data drift calculation`).
3. **Environment Variables:** If your PR introduces new environment variables, update `.env.example`. Do NOT commit actual `.env` files.
4. **Dependencies:** Since we use `pyproject.toml`, add any new required packages to the `dependencies` or `optional-dependencies` lists.
5. **Review:** Open your PR against `main`. Ensure CI workflows pass, and request a review from the repository maintainers.