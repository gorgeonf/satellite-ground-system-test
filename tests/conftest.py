from dataclasses import dataclass

import pytest


@pytest.fixture
def specifications_range_test_data():
    return {
        "REQ-TEMP-001": {
            "description": "Satellite temperature shall remain between -20°C and +60°C, inclusive.",
            "type": "range",
            "parameter": "temperature",
            "min": -20,
            "max": 60
        },
        "REQ-BATTERY-001": {
            "description": "Satellite battery voltage shall remain between 24 V and 32 V, inclusive.",
            "type": "range",
            "parameter": "battery_voltage",
            "min": 24,
            "max": 32
        },
        "REQ-SIGNAL-STRENGTH-001": {
            "description": "Satellite signal strength shall remain above -90, inclusive.",
            "type": "range",
            "parameter": "signal_strength",
            "min": -90,
            "max": 0
        }
    }


@dataclass
class RangeParametersDataSet:
    req_id: str
    input: list
    expected: list


TEST_RANGE_PARAMETERS_DATASET = [
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "temperature": 24.5,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:16:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1043,
            "temperature": 65,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 20,
            "packet_sequence": 1044,
        }
    ],
        expected=[1043], req_id="REQ-TEMP-001"),
        id="temperature_failure_in_middle"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "temperature": 24.5,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:16:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1043,
            "temperature": -30,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 5,
            "packet_sequence": 1044,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 70,
            "packet_sequence": 1045,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 65,
            "packet_sequence": 1046,
        }

    ],
        expected=[1043, 1045, 1046], req_id="REQ-TEMP-001"),
        id="temperature_several_failures"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "temperature": 24.5,
            "packet_sequence": 1042,
        }],
        expected=[], req_id="REQ-TEMP-001"),
        id="temperature_all_valid"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "temperature": -21,
            "packet_sequence": 1040,
        },
        {
            "temperature": -20,
            "packet_sequence": 1041,
        },
        {
            "temperature": -19,
            "packet_sequence": 1042,
        },
    ],
        expected=[1040], req_id="REQ-TEMP-001"),
        id="temperature_lower_boundary"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "temperature": 59,
            "packet_sequence": 1050,
        },
        {
            "temperature": 60,
            "packet_sequence": 1051,
        },
        {
            "temperature": 61,
            "packet_sequence": 1052,
        },
    ],
        expected=[1052], req_id="REQ-TEMP-001"),
        id="temperature_upper_boundary"),
    pytest.param(RangeParametersDataSet(input=[

    ],
        expected=[], req_id="REQ-TEMP-001"),
        id="temperature_empty_list"),

    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "battery_voltage": 26,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:16:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1043,
            "battery_voltage": 20,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "battery_voltage": 30,
            "packet_sequence": 1044,
        }
    ],
        expected=[1043], req_id="REQ-BATTERY-001"),
        id="battery_failure_in_middle"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "battery_voltage": 12,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:16:00",
            "satellite_id": "TESTSAT-1",
            "packet_sequence": 1043,
            "battery_voltage": 20,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "battery_voltage": 26,
            "packet_sequence": 1044,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "battery_voltage": 28,
            "packet_sequence": 1045,
        },
        {
            "timestamp": "2026-10-05T10:17:00",
            "satellite_id": "TESTSAT-1",
            "battery_voltage": 34,
            "packet_sequence": 1046,
        }
    ],
        expected=[1042, 1043, 1046], req_id="REQ-BATTERY-001"),
        id="battery_several_failures"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "battery_voltage": 29,
            "packet_sequence": 1042,
        }],
        expected=[], req_id="REQ-BATTERY-001"),
        id="battery_all_valid"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "battery_voltage": 23,
            "packet_sequence": 1040,
        },
        {
            "battery_voltage": 24,
            "packet_sequence": 1041,
        },
        {
            "battery_voltage": 25,
            "packet_sequence": 1042,
        },
    ],
        expected=[1040], req_id="REQ-BATTERY-001"),
        id="battery_lower_boundary"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "battery_voltage": 31,
            "packet_sequence": 1050,
        },
        {
            "battery_voltage": 32,
            "packet_sequence": 1051,
        },
        {
            "battery_voltage": 33,
            "packet_sequence": 1052,
        },
    ],
        expected=[1052], req_id="REQ-BATTERY-001"),
        id="battery_upper_boundary"),
    pytest.param(RangeParametersDataSet(input=[

    ],
        expected=[], req_id="REQ-BATTERY-001"),
        id="battery_empty_list"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -50,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -100,
            "packet_sequence": 1043,
        },
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -20,
            "packet_sequence": 1044,
        }],
        expected=[1043], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_failure_in_middle"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -50,
            "packet_sequence": 1042,
        },
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -110,
            "packet_sequence": 1043,
        },
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -120,
            "packet_sequence": 1044,
        }
        ,
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -100,
            "packet_sequence": 1045,
        },
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -20,
            "packet_sequence": 1046,
        }
    ],
        expected=[1043, 1044, 1045], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_several_failures"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -50,
            "packet_sequence": 1042,
        }],
        expected=[], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_all_valid"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "timestamp": "2026-10-05T10:15:00",
            "satellite_id": "TESTSAT-1",
            "signal_strength": -50,
            "packet_sequence": 1042,
        }],
        expected=[], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_all_valid"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "signal_strength": -91,
            "packet_sequence": 1040,
        },
        {
            "signal_strength": -90,
            "packet_sequence": 1041,
        },
        {
            "signal_strength": -89,
            "packet_sequence": 1042,
        },
    ],
        expected=[1040], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_lower_boundary"),
    pytest.param(RangeParametersDataSet(input=[
        {
            "signal_strength": -1,
            "packet_sequence": 1050,
        },
        {
            "signal_strength": 0,
            "packet_sequence": 1051,
        },
        {
            "signal_strength": 1,
            "packet_sequence": 1052,
        },
    ],
        expected=[1052], req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_upper_boundary"),
    pytest.param(RangeParametersDataSet(input=[

    ],
        expected=[],
        req_id="REQ-SIGNAL-STRENGTH-001"),
        id="signal_strength_empty_list"),
]
