import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def check_temperature(telemetry: list, specifications: dict) -> list:
    """
    This function verifies REQ-TEMP-001 against telemetry

    :param telemetry: list of telemetry records
    :param specifications: dictionary of requirements
    :return: list of telemetry records that do not comply with REQ-TEMP-001
    """
    invalid_records = []
    temp_req_id = "REQ-TEMP-001"
    try:
        requirement = specifications[temp_req_id]
    except KeyError:
        raise KeyError(f"{temp_req_id} is not present in the specifications file.")

    try:
        min_temp = requirement["min"]
        max_temp = requirement["max"]
    except KeyError as e:
        raise KeyError(f"{temp_req_id} is missing the {e} limit in the specifications file.")

    for data in telemetry:
        temp = data.get("temperature")
        if temp is None:
            raise ValueError(
                f"Telemetry record {data.get('packet_sequence')} does not contain temperature info.")
        if not (max_temp >= temp >= min_temp):
            print(
                f"WARNING: {data.get('packet_sequence')} does not comply with {temp_req_id} "
                f"--> {temp} not in [{min_temp};{max_temp}]")
            invalid_records.append(data.get('packet_sequence'))
    if invalid_records:
        print(f"Found {len(invalid_records)} records that do not comply with {temp_req_id}")
    return invalid_records


def get_data(telemetry_file: Path) -> list:
    """
    This function reads telemetry data from a JSON file and returns it as a list of dictionaries.

    :param telemetry_file: Path to the JSON file containing telemetry data
    :return: List of dictionaries representing telemetry records
    """
    try:
        with open(telemetry_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{telemetry_file.name} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"{telemetry_file.name} is not a valid JSON format.")


def get_requirements(req_file: Path) -> dict:
    """
    This function reads requirements from a JSON file and returns it as a dictionary.

    :param req_file: Path to the JSON file containing requirements
    :return: Dictionary of requirements
    """
    try:
        with open(req_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"{req_file.name} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"{req_file.name} is not a valid JSON format.")


if __name__ == "__main__":

    telemetry_path = PROJECT_ROOT / "data" / "telemetry.json"
    req_path = PROJECT_ROOT / "specifications" / "requirements.json"

    try:
        my_data = get_data(telemetry_path)
        requirements = get_requirements(req_path)
        check_temperature(my_data, requirements)
    except (ValueError, FileNotFoundError, KeyError) as e:
        print(f"ERROR: {e}")
