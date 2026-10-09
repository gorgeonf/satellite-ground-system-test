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
