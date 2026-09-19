# Code Quality & Formatting Guidelines

This project utilizes **Ruff** for unified linting and formatting, replacing legacy tools like Black, isort, and Flake8.

**Note on Automation:**
Automated quality checks are enforced locally on `git commit` via pre-commit hooks, and globally within the CI pipeline.
You can also run manual fallback commands at any time.

## 1. Environment Setup

To ensure code quality tools run automatically when you commit changes, you must install and activate the pre-commit
hooks in your local environment.

```bash
# 1. Ensure you have installed the project's development dependencies
pip install -e ".[dev]"

# 2. Install the pre-commit hooks into your local git repository
pre-commit install
```

Once installed, Ruff will automatically check and format your staged files every time you run `git commit`.

## 2. Manual Execution Commands

You can trigger the quality checks manually using `pre-commit` or `ruff` directly.

**Run checks repository-wide on ALL files:**

```bash
pre-commit run --all-files
```

**Run checks ONLY on staged or modified files:**

```bash
pre-commit run
```

**Run checks against specific files or directories:**

```bash
pre-commit run --files src/serve.py tests/
```

## 3. Isolated Tool Commands

If you prefer to run Ruff independently without invoking the full pre-commit pipeline:

**Run the Linter only:**

```bash
ruff check .
# To automatically fix safe linting errors:
ruff check . --fix
```

**Run the Formatter only:**

```bash
ruff format .
```

## 4. Maintenance & Cache

Over time, you may need to update the pre-commit hooks to their latest versions or clear the cache if the tool behaves
unexpectedly.

**Update pre-commit dependencies to latest versions:**

```bash
pre-commit autoupdate
```

**Clear local tool caches:**

```bash
pre-commit clean
ruff clean
```

## 5. Emergency Bypassing

*Warning: Bypassing quality checks should only be done in absolute emergencies, such as critical hotfixes where a linter
rule is incorrectly blocking a deploy.*

To bypass the pre-commit hooks during a commit, use the `--no-verify` flag:

```bash
git commit -m "fix(urgent): bypass hooks for hotfix" --no-verify
```