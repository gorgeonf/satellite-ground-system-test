from pathlib import Path

from src.telemetry import get_requirements

SPEC_PATH = Path(__file__).resolve().parent.parent / "specifications" / "requirements.json"


def test_temperature_requirements():
    """
    The real requirements file defines REQ-TEMP-001 with limits -20 and 60.
    """
    requirements = get_requirements(SPEC_PATH)
    assert "REQ-TEMP-001" in requirements
    assert requirements["REQ-TEMP-001"]["parameter"] == "temperature"
    assert requirements["REQ-TEMP-001"]['min'] == -20
    assert requirements["REQ-TEMP-001"]['max'] == 60

def test_battery_requirements():
    """
    The real requirements file defines REQ-BATTERY-001 with limits 24 and 32.
    """
    requirements = get_requirements(SPEC_PATH)
    assert "REQ-BATTERY-001" in requirements
    assert requirements["REQ-BATTERY-001"]["parameter"] == "battery_voltage"
    assert requirements["REQ-BATTERY-001"]['min'] == 24
    assert requirements["REQ-BATTERY-001"]['max'] == 32

def test_signal_strength_requirements():
    """
    The real requirements file defines REQ-SIGNAL-STRENGTH-001 with limits -90 and 0.
    """
    requirements = get_requirements(SPEC_PATH)
    assert "REQ-SIGNAL-STRENGTH-001" in requirements
    assert requirements["REQ-SIGNAL-STRENGTH-001"]["parameter"] == "signal_strength"
    assert requirements["REQ-SIGNAL-STRENGTH-001"]['min'] == -90
    assert requirements["REQ-SIGNAL-STRENGTH-001"]['max'] == 0
