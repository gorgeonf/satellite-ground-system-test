from pathlib import Path

import pytest

from src.telemetry import get_data, get_requirements

TEST_DATA_DIR = Path(__file__).resolve().parent.parent
TEST_TELEMETRY_DATA = TEST_DATA_DIR / "tests/data/telemetry_test_data.json"
TEST_REQ_DATA = TEST_DATA_DIR / "tests/data/requirements_test_data.json"
MISSING_FILE = TEST_DATA_DIR / "tests/data/missing_file.json"
INVALID_JSON = TEST_DATA_DIR / "tests/data/invalid_json.json"


def test_get_data():
    assert get_data(TEST_TELEMETRY_DATA) == [
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 24.5,
            "battery_voltage": 28.1,
            "signal_strength": -72,
            "packet_sequence": 1042,
            "communication_status": "OK"
        },
        {
            "timestamp": "2026-10-05T10:16:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 25.1,
            "battery_voltage": 27.9,
            "signal_strength": -74,
            "packet_sequence": 1043,
            "communication_status": "OK"
        }
    ]


def test_get_data_missing_file():
    with pytest.raises(FileNotFoundError, match="missing_file.json does not exist."):
        get_data(MISSING_FILE)


def test_get_data_invalid_json():
    with pytest.raises(ValueError, match="invalid_json.json is not a valid JSON format."):
        get_data(INVALID_JSON)


def test_get_requirements():
    assert get_requirements(TEST_REQ_DATA) == {
        "REQ-TEMP-001": {"description": "Description of the requirement.", "type": "range", "parameter": "temp",
                         "min": -20, "max": 60},
        "REQ-TEMP-002": {"description": "Description of another requirement.", },
        "REQ-BATTERY-001": {"description": "Description of the last requirement.", "type": "range",
                            "parameter": "voltage", }
    }


def test_get_requirements_missing_file():
    with pytest.raises(FileNotFoundError, match="missing_file.json does not exist"):
        get_requirements(MISSING_FILE)


def test_get_requirements_invalid_json():
    with pytest.raises(ValueError, match="invalid_json.json is not a valid JSON format"):
        get_requirements(INVALID_JSON)
