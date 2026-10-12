import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def check_range(telemetry: list, specifications: dict, req_id: str) -> list:
    """
    This function verifies requirement req_id against telemetry

    :param telemetry: list of telemetry records
    :param specifications: dictionary of requirements
    :param req_id: requirement to check
    :return: list of telemetry records that do not comply with req_id
    """
    invalid_records = []
    try:
        requirement = specifications[req_id]
    except KeyError:
        raise KeyError(f"{req_id} is not present in the specifications file.")

    try:
        parameter = requirement["parameter"]
    except KeyError:
        raise KeyError(f"{req_id} is missing the parameter attribute in the specifications file.")

    try:
        min_value = requirement["min"]
        max_value = requirement["max"]
    except KeyError as e:
        raise KeyError(f"{req_id} is missing the {e} limit in the specifications file.")

    for data in telemetry:
        temp = data.get(parameter)
        if temp is None:
            raise ValueError(
                f"Telemetry record {data.get('packet_sequence')} does not contain {parameter} info.")
        if not (max_value >= temp >= min_value):
            print(
                f"WARNING: {data.get('packet_sequence')} does not comply with {req_id} "
                f"--> {temp} not in [{min_value};{max_value}]")
            invalid_records.append(data.get('packet_sequence'))
    if invalid_records:
        print(f"Found {len(invalid_records)} records that do not comply with {req_id}")
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
