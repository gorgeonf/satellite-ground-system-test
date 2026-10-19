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


@pytest.fixture
def specifications_status_test_data():
    return {
        "REQ-COMM-001": {
            "description": "Satellite communication status shall be OK.",
            "type": "status",
            "parameter": "communication_status",
            "value": "OK"
        },
    }


def make_records(parameter: str, values: list) -> list:
    packet_number = 1042
    data_set = []
    for v in values:
        data_set.append({parameter: v, "packet_sequence": packet_number})
        packet_number += 1
    return data_set
