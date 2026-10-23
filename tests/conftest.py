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


@pytest.fixture
def specifications_sequence_test_data():
    return {
        "REQ-SEQ-001": {
            "description": "Satellite packet number shall increase by one unit.",
            "type": "sequence",
            "parameter": "packet_sequence",
            "step": 1
        },
        "REQ-SEQ-003": {
            "description": "Satellite packet number shall increase by three units.",
            "type": "sequence",
            "parameter": "packet_sequence",
            "step": 3
        },
    }
