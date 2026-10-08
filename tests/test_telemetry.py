from pathlib import Path

import pytest

from src.telemetry import check_temperature, get_requirements

REQ_PATH = Path(__file__).resolve().parent.parent / "specifications" / "requirements.json"
SPEC = get_requirements(REQ_PATH)


def test_check_temperature(temperature_dataset):
    assert check_temperature(temperature_dataset["input"], SPEC) == temperature_dataset["expected"]


@pytest.mark.parametrize("input_telemetry, input_requirement, expected_result", [
    (
            [{
                "timestamp": "2026-10-05T10:15:00",
                "satellite_id": "TESTSAT-1",
            }], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_temperature"}},
            "REQ-TEMP-001 is not present in the specifications file."),
    (
            [{
                "timestamp": "2026-10-05T10:15:00",
                "satellite_id": "TESTSAT-1",
            }],
            {"REQ-TEMP-001": {"description": "", "type": "range",
                              "parameter": "temperature", "max": 60}},
            "REQ-TEMP-001 is missing the 'min' limit in the specifications file."),
    (
            [{
                "timestamp": "2026-10-05T10:15:00",
                "satellite_id": "TESTSAT-1",
            }],
            {"REQ-TEMP-001": {"description": "", "type": "range",
                              "parameter": "temperature", "min": -20}},
            "REQ-TEMP-001 is missing the 'max' limit in the specifications file."),

])
def test_check_temperature_wrong_requirements(input_telemetry, input_requirement, expected_result):
    with pytest.raises(KeyError, match=expected_result):
        check_temperature(input_telemetry, input_requirement)


