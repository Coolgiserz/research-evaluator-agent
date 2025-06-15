# Contributing to Research Evaluator Agent

Thank you for your interest in improving Research Evaluator Agent! We welcome issues, feature requests, documentation updates, and code contributions. This guide will help you get started.

---

## 1. Reporting Issues and Feature Requests

1. Check existing issues to avoid duplicates.
2. To report a bug, open an issue with:
   - A clear, descriptive title.
   - Steps to reproduce the problem.
   - Expected vs. actual behavior.
   - Relevant logs, error messages, or stack traces.
   - Environment details (OS, Python version, dependency versions).
3. To suggest a new feature, open an issue describing:
   - Use case and motivation.
   - Proposed API changes, CLI flags, or configuration.
   - Any backward-compatibility considerations.

---

## 2. Development Setup

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/Coolgiserz/research-evaluator-agent.git
   cd research-evaluator-agent
   ```
3. **Create** and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. **Install** the UV dependency manager (if not already installed):
   ```bash
   pip install uv
   ```
5. **Sync** project dependencies from `pyproject.toml`/`uv.lock`:
   ```bash
   uv sync
   ```
6. **Create** a new branch for your work:
   ```bash
   git checkout -b feat/your-feature-name
   ```

---

## 3. Code Style and Quality

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Format code with **Black**:
  ```bash
  black .
  ```
- Sort imports with **isort**:
  ```bash
  isort .
  ```
- (Optional) Check lint issues with **flake8**:
  ```bash
  flake8 .
  ```

Ensure all code passes formatting and lint checks before committing.

---

## 4. Writing Tests

- The project uses **pytest** and **pytest-asyncio**.
- Add or update tests under the `tests/` directory for new features or bug fixes.
- Run tests locally:
  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```
- Aim for good coverage and cover edge cases.

---

## 5. Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):
```
<type>(<scope>): <short description>

<body> (optional)

<footer> (e.g., Closes #123)
```
Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

---

## 6. Pull Request Process

1. Push your branch to your fork.
2. Open a Pull Request (PR) targeting the `main` branch.
3. In your PR description, include:
   - What changes you made and why.
   - Related issue number(s) (`Closes #123`).
   - Screenshots or examples, if applicable.
4. Ensure all checks pass (formatting, linting, tests).
5. Request reviews from maintainers.
6. Address review feedback and **rebase** or merge upstream changes as needed.

---

## 7. Updating Documentation

- If you introduce new features or change behavior, update `README.md` and `README_zh.md` accordingly.
- Document any new CLI commands, API endpoints, or configuration options.

---

## 8. License and Code of Conduct

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions.

---

Thank you for helping make Research Evaluator Agent better! 🎉 