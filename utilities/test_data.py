import json
from functools import cache
from pathlib import Path
from typing import Any

# Define the path to the test data JSON file relative to this script's location.
# __file__ gives the current file path, resolve() makes it absolute, parent.parent goes up two directories,
# and then we append "test_data/test_data.json" to get the full path to the test data file.
_TEST_DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "test_data.json"

@cache
def load_test_data() -> dict[str, Any]:
    with _TEST_DATA_FILE.open(encoding="utf-8") as data_file:
        return json.load(data_file)
