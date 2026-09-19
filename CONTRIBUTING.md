# Contributing Guidelines

First off, thank you for considering contributing to the **Customer Churn Risk Intelligence** pipeline!

## Code Style & Linting

This project enforces a strict code quality standard using [Ruff](https://docs.astral.sh/ruff/).
All code changes must pass linting and formatting before being merged.
Please refer to the [CODE_QUALITY.md](CODE_QUALITY.md) document for detailed instructions on how to run checks locally
and set up pre-commit hooks.

## Testing

We use `pytest` for all unit and integration testing.

- Ensure that you add or update tests in the `tests/` directory for any new features or bug fixes.
- Run the full test suite locally before pushing your changes:
  ```bash
  pytest
  ```

## Pull Request Process & Commit Messages

This project uses **[Google Release Please](https://github.com/googleapis/release-please)** to automatically generate
`CHANGELOG.md` files and bump Semantic Versioning numbers. **Therefore, all commits MUST adhere to
the [Conventional Commits](https://www.conventionalcommits.org/) specification.**

When creating a Pull Request, ensure your commits or your Squash-and-Merge title follows this format:
`<type>(<optional scope>): <description>`

### Allowed Types:

| Type       | Purpose                                                 | Triggers Release?       |
|------------|---------------------------------------------------------|-------------------------|
| `feat`     | A new feature                                           | **Yes (Minor / 0.1.0)** |
| `fix`      | A bug fix                                               | **Yes (Patch / 0.0.1)** |
| `docs`     | Documentation only changes                              | No                      |
| `style`    | Formatting, missing semi-colons, etc.                   | No                      |
| `refactor` | Code change that neither fixes a bug nor adds a feature | No                      |
| `perf`     | A code change that improves performance                 | No                      |
| `test`     | Adding missing tests or correcting existing tests       | No                      |
| `chore`    | Changes to the build process or auxiliary tools         | No                      |
| `ci`       | CI/CD configuration updates                             | No                      |

**Breaking Changes:** If your commit introduces a breaking API change, include `!` after the type/scope (e.g.,
`feat!: rewrite API endpoints`), or add `BREAKING CHANGE:` in the footer of the commit message. This will trigger a *
*Major (1.0.0)** release.

### Workflow Example:

1. **Branching:** Create a feature branch from `main` (e.g., `feat/add-new-model` or `fix/schema-validation`).
2. **Commit:** `git commit -m "feat(api): integrate SHAP explainability into predictions"`
3. **Environment Variables:** If your PR introduces new environment variables, update `.env.example`. Do NOT commit
   actual `.env` files.
4. **Dependencies:** Since we use `pyproject.toml`, add any new required packages to the `dependencies` or
   `optional-dependencies` lists.
5. **Review:** Open your PR against `main`. Ensure CI workflows pass, and request a review from the repository
   maintainers.