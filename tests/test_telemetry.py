import pytest

from src.telemetry import check_range, check_status
from tests.conftest import make_records


@pytest.mark.parametrize("telemetry, req_id, expected_result",
                         [
                             pytest.param(make_records("temperature", [24.5, 65, 20]), "REQ-TEMP-001", [1043],
                                          id="temperature_failure_in_middle"),
                             pytest.param(make_records("temperature", [24.5, -30, 5, 70, 65]), "REQ-TEMP-001",
                                          [1043, 1045, 1046],
                                          id="temperature_several_failures"),
                             pytest.param(make_records("temperature", [24.5, 15, 20]), "REQ-TEMP-001", [],
                                          id="temperature_all_valid"),
                             pytest.param(make_records("temperature", [-21, -20, -19]), "REQ-TEMP-001", [1042],
                                          id="temperature_lower_boundary"),
                             pytest.param(make_records("temperature", [59, 60, 61]), "REQ-TEMP-001", [1044],
                                          id="temperature_upper_boundary"),
                             pytest.param([], "REQ-TEMP-001", [], id="temperature_empty_list"),

                             pytest.param(make_records("battery_voltage", [26, 20, 30]), "REQ-BATTERY-001", [1043],
                                          id="battery_voltage_failure_in_middle"),
                             pytest.param(make_records("battery_voltage", [12, 20, 26, 28, 34]), "REQ-BATTERY-001",
                                          [1042, 1043, 1046],
                                          id="battery_voltage_several_failures"),
                             pytest.param(make_records("battery_voltage", [24.5, 28, 30]), "REQ-BATTERY-001", [],
                                          id="battery_voltage_all_valid"),
                             pytest.param(make_records("battery_voltage", [23, 24, 25]), "REQ-BATTERY-001", [1042],
                                          id="battery_voltage_lower_boundary"),
                             pytest.param(make_records("battery_voltage", [31, 32, 33]), "REQ-BATTERY-001", [1044],
                                          id="battery_voltage_upper_boundary"),
                             pytest.param([], "REQ-BATTERY-001", [], id="battery_voltage_empty_list"),

                             pytest.param(make_records("signal_strength", [-70, -100, -15]), "REQ-SIGNAL-STRENGTH-001",
                                          [1043],
                                          id="signal_strength_failure_in_middle"),
                             pytest.param(make_records("signal_strength", [-95, 10, -120, -50, -10]),
                                          "REQ-SIGNAL-STRENGTH-001",
                                          [1042, 1043, 1044],
                                          id="signal_strength_several_failures"),
                             pytest.param(make_records("signal_strength", [-80, -70, -81]), "REQ-SIGNAL-STRENGTH-001",
                                          [],
                                          id="signal_strength_all_valid"),
                             pytest.param(make_records("signal_strength", [-91, -90, -89]), "REQ-SIGNAL-STRENGTH-001",
                                          [1042],
                                          id="signal_strength_lower_boundary"),
                             pytest.param(make_records("signal_strength", [-1, 0, 1]), "REQ-SIGNAL-STRENGTH-001",
                                          [1044],
                                          id="signal_strength_upper_boundary"),
                             pytest.param([], "REQ-SIGNAL-STRENGTH-001", [], id="signal_strength_empty_list"),
                         ])
def test_check_range_values(specifications_range_test_data, telemetry, req_id, expected_result):
    assert check_range(telemetry, specifications_range_test_data, req_id) == expected_result


@pytest.mark.parametrize("input_telemetry, input_requirement, req_id, expected_result", [
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_range."}}, "REQ-TEMP-001",
        "REQ-TEMP-001 is not present in the specifications file.",
        id="requirement_missing_temperature"),
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_range."}}, "REQ-BATTERY-001",
        "REQ-BATTERY-001 is not present in the specifications file.",
        id="requirement_missing_battery_voltage"),
    pytest.param(
        [], {"REQ-PRESSURE-001": {"description": "Wrong requirement for check_range."}},
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


@pytest.mark.parametrize("req_id, expected_result", [
    ("REQ-TEMP-001", "Telemetry record 1000 does not contain temperature info."),
    ("REQ-BATTERY-001", "Telemetry record 1000 does not contain battery_voltage info."),
    ("REQ-SIGNAL-STRENGTH-001", "Telemetry record 1000 does not contain signal_strength info."),
])
def test_check_range_missing_parameter_in_telemetry(specifications_range_test_data, req_id, expected_result):
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1000,
        }, ]
    with pytest.raises(ValueError, match=expected_result):
        check_range(input_telemetry, specifications_range_test_data, req_id)


def test_check_range_wrong_type_in_requirement():
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "temperature": 24.5,
            "packet_sequence": 1042,
        }]
    input_requirement = {
        "REQ-TEMP-001": {
            "type": "status",
            "parameter": "temperature",
            "min": -20,
            "max": 60
        }}
    with pytest.raises(ValueError, match="REQ-TEMP-001 is not a range requirement."):
        check_range(input_telemetry, input_requirement, "REQ-TEMP-001")


@pytest.mark.parametrize("input_telemetry, req_id, expected_result", [
    pytest.param(make_records("communication_status", ["OK", "NOK", "OK"]), "REQ-COMM-001", [1043],
                 id="communication_status_failure_in_middle"),
    pytest.param(make_records("communication_status", ["OK", "NOK", "SOMETHING", "OK", "NOK"]), "REQ-COMM-001",
                 [1043, 1044, 1046],
                 id="communication_status_several_failures"),
    pytest.param(make_records("communication_status", ["OK", "OK", "OK"]), "REQ-COMM-001", [],
                 id="communication_status_all_valid"),
    pytest.param(make_records("communication_status", ["NOK", "NOK", "NOK"]), "REQ-COMM-001", [1042, 1043, 1044],
                 id="communication_status_all_failures"),
    pytest.param(make_records("communication_status", [21, "OK", "OK"]), "REQ-COMM-001", [1042],
                 id="communication_status_not_a_string"),
    pytest.param([], "REQ-COMM-001", [], id="communication_status_empty_list"),
])
def test_check_status_values(specifications_status_test_data, input_telemetry, req_id, expected_result):
    assert check_status(input_telemetry, specifications_status_test_data, req_id) == expected_result


@pytest.mark.parametrize("input_telemetry, input_requirement, req_id, expected_result", [
    pytest.param(
        [], {"REQ-TEMP-001": {"description": "Wrong requirement for check_status."}}, "REQ-COMM-001",
        "REQ-COMM-001 is not present in the specifications file.",
        id="status_requirement_missing"),

    pytest.param(
        [],
        {"REQ-COMM-001": {"description": "Satellite communication status shall be OK.",
                          "type": "status",
                          "parameter": "communication_status"}}, "REQ-COMM-001",
        "REQ-COMM-001 is missing the 'value' in the specifications file.",
        id="status_value_missing"),

    pytest.param(
        [],
        {"REQ-COMM-001": {"description": "Satellite communication status shall be OK.",
                          "type": "status",
                          "value": "OK"}}, "REQ-COMM-001",
        "REQ-COMM-001 is missing the parameter attribute in the specifications file.",
        id="status_parameter_missing"),

])
def test_check_status_wrong_requirements(input_telemetry, input_requirement, req_id, expected_result):
    with pytest.raises(KeyError, match=expected_result):
        check_status(input_telemetry, input_requirement, req_id)


@pytest.mark.parametrize("req_id, expected_result", [
    ("REQ-COMM-001", "Telemetry record 1000 does not contain communication_status info."),
])
def test_check_status_missing_parameter_in_telemetry(specifications_status_test_data, req_id, expected_result):
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1000,
        }, ]
    with pytest.raises(ValueError, match=expected_result):
        check_status(input_telemetry, specifications_status_test_data, req_id)


def test_check_status_wrong_type_in_requirement():
    input_telemetry = [
        {
            "timestamp": "2026-10-05T10:15:00",
            "communication_status": "OK",
            "packet_sequence": 1042,
        }]
    input_requirement = {
        "REQ-COMM-001": {
            "description": "Satellite communication status shall be OK.",
            "type": "range",
            "parameter": "communication_status",
            "value": "OK"
        }}
    with pytest.raises(ValueError, match="REQ-COMM-001 is not a status requirement."):
        check_status(input_telemetry, input_requirement, "REQ-COMM-001")
