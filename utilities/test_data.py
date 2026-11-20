import csv
import json
from functools import cache
from pathlib import Path
from typing import Any

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
# Define the path to the test data JSON file relative to this script's location.
# __file__ gives the current file path, resolve() makes it absolute, parent.parent goes up two directories,
# and then we append "test_data/test_data.json" to get the full path to the test data file.
_TEST_DATA_FILE = _PROJECT_ROOT / "test_data" / "test_data.json"

@cache
def load_test_data() -> dict[str, Any]:
    with _TEST_DATA_FILE.open(encoding="utf-8") as data_file:
        return json.load(data_file)


def load_csv_rows(relative_path: str) -> list[dict[str, str]]:
    """Read a CSV (path relative to the project root); empty cells stay as empty strings."""
    with (_PROJECT_ROOT / relative_path).open(encoding="utf-8", newline="") as csv_file:
        return [
            {column: (value or "").strip() for column, value in row.items()}
            for row in csv.DictReader(csv_file)
        ]


def load_csv_params(relative_path: str, id_column: str = "test_id") -> list[Any]:
    """Turn each CSV row into a pytest.param so every row is an independent, readably named test."""
    return [pytest.param(row, id=row[id_column]) for row in load_csv_rows(relative_path)]
