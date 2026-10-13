import pytest

from src.telemetry import check_range
from tests.conftest import TEST_RANGE_PARAMETERS_DATASET


@pytest.mark.parametrize("range_parameters_dataset", TEST_RANGE_PARAMETERS_DATASET)
def test_check_range_values(specifications_range_test_data, range_parameters_dataset):
    req_id = range_parameters_dataset.req_id
    input_dataset = range_parameters_dataset.input
    expected_result = range_parameters_dataset.expected
    assert check_range(input_dataset, specifications_range_test_data, req_id) == expected_result


@pytest.mark.parametrize("input_telemetry, input_requirement, req_id, expected_result", [
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_temperature."}}, "REQ-TEMP-001",
        "REQ-TEMP-001 is not present in the specifications file.",
        id="requirement_missing_temperature"),
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_temperature."}}, "REQ-BATTERY-001",
        "REQ-BATTERY-001 is not present in the specifications file.",
        id="requirement_missing_battery_voltage"),
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_temperature."}},
        "REQ-SIGNAL-STRENGTH-001", "REQ-SIGNAL-STRENGTH-001 is not present in the specifications file.",
        id="requirement_missing_signal_strength"),

    pytest.param(
        [],
        {"REQ-TEMP-001": {"description": "", "type": "range",
                          "parameter": "temperature", "max": 60}}, "REQ-TEMP-001",
        "REQ-TEMP-001 is missing the 'min' limit in the specifications file.",
        id="min_missing_temperature"),
    pytest.param(
        [],
        {"REQ-BATTERY-001": {"description": "", "type": "range",
                             "parameter": "battery_voltage", "max": 32}}, "REQ-BATTERY-001",
        "REQ-BATTERY-001 is missing the 'min' limit in the specifications file.",
        id="min_missing_battery_voltage"),
    pytest.param(
        [],
        {"REQ-SIGNAL-STRENGTH-001": {"description": "", "type": "range",
                                     "parameter": "signal_strength", "max": 0}}, "REQ-SIGNAL-STRENGTH-001",
        "REQ-SIGNAL-STRENGTH-001 is missing the 'min' limit in the specifications file.",
        id="min_missing_signal_strength"),

    pytest.param(
        [],
        {"REQ-TEMP-001": {"description": "", "type": "range",
                          "parameter": "temperature", "min": -20}}, "REQ-TEMP-001",
        "REQ-TEMP-001 is missing the 'max' limit in the specifications file.",
        id="max_missing_min_missing_temperature"),
    pytest.param(
        [],
        {"REQ-BATTERY-001": {"description": "", "type": "range",
                             "parameter": "battery_voltage", "min": 24}}, "REQ-BATTERY-001",
        "REQ-BATTERY-001 is missing the 'max' limit in the specifications file.",
        id="max_missing_battery_voltage"),
    pytest.param(
        [],
        {"REQ-SIGNAL-STRENGTH-001": {"description": "", "type": "range",
                                     "parameter": "signal_strength", "min": -90}}, "REQ-SIGNAL-STRENGTH-001",
        "REQ-SIGNAL-STRENGTH-001 is missing the 'max' limit in the specifications file.",
        id="max_missing_signal_strength"),

    pytest.param(
        [],
        {"REQ-TEMP-001": {"description": "", "type": "range",
                          "min": -20, "max": 60}}, "REQ-TEMP-001",
        "REQ-TEMP-001 is missing the parameter attribute in the specifications file.",
        id="parameter_missing_temperature"),
    pytest.param(
        [],
        {"REQ-BATTERY-001": {"description": "", "type": "range",
                             "min": 24, "max": 32}}, "REQ-BATTERY-001",
        "REQ-BATTERY-001 is missing the parameter attribute in the specifications file.",
        id="parameter_missing_battery_voltage"),
    pytest.param(
        [],
        {"REQ-SIGNAL-STRENGTH-001": {"description": "", "type": "range",
                                     "min": -90, "max": 0}}, "REQ-SIGNAL-STRENGTH-001",
        "REQ-SIGNAL-STRENGTH-001 is missing the parameter attribute in the specifications file.",
        id="parameter_missing_signal_strength"),

])
def test_check_range_wrong_requirements(input_telemetry, input_requirement, req_id, expected_result):
    with pytest.raises(KeyError, match=expected_result):
        check_range(input_telemetry, input_requirement, req_id)


@pytest.mark.parametrize("req_id, parameter, expected_result", [
    ("REQ-TEMP-001", "temperature", "Telemetry record 1000 does not contain temperature info."),
    ("REQ-BATTERY-001", "battery_voltage", "Telemetry record 1000 does not contain battery_voltage info."),
    ("REQ-SIGNAL-STRENGTH-001", "signal_strength", "Telemetry record 1000 does not contain signal_strength info.")
])
def test_check_range_missing_parameter(specifications_range_test_data, req_id, parameter, expected_result):
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1000,
        }, ]
    with pytest.raises(ValueError, match=expected_result):
        check_range(input_telemetry, specifications_range_test_data, req_id)
