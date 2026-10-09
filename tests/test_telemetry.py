from pathlib import Path

import pytest

from src.telemetry import check_temperature


def test_check_temperature(temperature_dataset, temperature_specifications):
    assert check_temperature(temperature_dataset["input"], temperature_specifications) == temperature_dataset[
        "expected"]


@pytest.mark.parametrize("input_telemetry, input_requirement, expected_result", [
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_temperature"}},
        "REQ-TEMP-001 is not present in the specifications file.", id="requirement_missing"),
    pytest.param(
        [],
        {"REQ-TEMP-001": {"description": "", "type": "range",
                          "parameter": "temperature", "max": 60}},
        "REQ-TEMP-001 is missing the 'min' limit in the specifications file.", id="min_missing"),
    pytest.param(
        [],
        {"REQ-TEMP-001": {"description": "", "type": "range",
                          "parameter": "temperature", "min": -20}},
        "REQ-TEMP-001 is missing the 'max' limit in the specifications file.", id="max_missing"),

])
def test_check_temperature_wrong_requirements(input_telemetry, input_requirement, expected_result):
    with pytest.raises(KeyError, match=expected_result):
        check_temperature(input_telemetry, input_requirement)


def test_check_temperature_missing_temperature(temperature_specifications):
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1000,
        }, ]
    expected_result = "Telemetry record 1000 does not contain temperature info."
    with pytest.raises(ValueError, match=expected_result):
        check_temperature(input_telemetry, temperature_specifications)
