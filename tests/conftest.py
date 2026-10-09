import pytest


@pytest.fixture
def temperature_specifications():
    return {
        "REQ-TEMP-001": {
            "description": "Description of the requirement.",
            "type": "range",
            "parameter": "temp",
            "min": -20,
            "max": 60
        }
    }


@pytest.fixture(params=
[
    {
        "input": [
            {
                "timestamp": "2026-10-05T10:15:00",
                "temperature": 24.5,
                "packet_sequence": 1042,
            },
            {
                "timestamp": "2026-10-05T10:16:00",
                "satellite_id": "TESTSAT-1",
                "packet_sequence": 1043,
                "temperature": 25.1,
            },
            {
                "timestamp": "2026-10-05T10:17:00",
                "satellite_id": "TESTSAT-1",
                "temperature": 65,
                "packet_sequence": 1044,
            }
        ],
        "expected": [1044]
    },
    {
        "input": [
            {
                "timestamp": "2026-10-05T10:15:00",
                "satellite_id": "TESTSAT-1",
                "temperature": 24.5,
                "packet_sequence": 1042,
            }],
        "expected": []
    },
    {
        "input": [
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
        "expected": [1040]
    },
    {
        "input": [
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
        "expected": [1052]
    },
    {
        "input": [],
        "expected": []
    },
],
    ids=["one_above_max", "all_valid", "lower_boundary", "upper_boundary", "empty_list"])
def temperature_dataset(request):
    return request.param
