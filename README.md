# Playwright Framework

A beginner-friendly Python test framework scaffold using the Playwright synchronous API, Pytest, and Page Object Model.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Adjust `BASE_URL`, `BROWSER`, or `HEADLESS` in `.env` for your local environment. The `.env` file is ignored by Git.

## Run tests

```powershell
pytest
```


