import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def check_range(telemetry: list, specifications: dict, range_req_id: str) -> list:
    """
    This function verifies a range requirement (min and max limit on one parameter) against telemetry.

   :param telemetry: list of telemetry records
    :param specifications: dictionary of requirements
    :param range_req_id: ID of the range requirement to verify (e.g. "REQ-TEMP-001")
    :return: list of packet sequence numbers of the records that do not comply with the requirement

    """
    invalid_records = []
    try:
        requirement = specifications[range_req_id]
    except KeyError:
        raise KeyError(f"{range_req_id} is not present in the specifications file.")

    if requirement.get("type") != "range":
        raise ValueError(f"{range_req_id} is not a range requirement.")

    try:
        parameter = requirement["parameter"]
    except KeyError:
        raise KeyError(f"{range_req_id} is missing the parameter attribute in the specifications file.")

    try:
        min_value = requirement["min"]
        max_value = requirement["max"]
    except KeyError as e:
        raise KeyError(f"{range_req_id} is missing the {e} limit in the specifications file.")

    for data in telemetry:
        temp = data.get(parameter)
        if temp is None:
            raise ValueError(
                f"Telemetry record {data.get('packet_sequence')} does not contain {parameter} info.")
        if not (max_value >= temp >= min_value):
            print(
                f"WARNING: {data.get('packet_sequence')} does not comply with {range_req_id} "
                f"--> {temp} not in [{min_value};{max_value}]")
            invalid_records.append(data.get('packet_sequence'))
    if invalid_records:
        print(f"Found {len(invalid_records)} records that do not comply with {range_req_id}")
    return invalid_records


def check_status(telemetry: list, specifications: dict, status_req_id: str) -> list:
    """
    This function verifies a status requirement against telemetry.

    :param telemetry: list of telemetry records
    :param specifications: dictionary of requirements
    :param status_req_id: ID of the status requirement to verify (e.g. "REQ-COMM-001")
    :return: list of packet sequence numbers of the records that do not comply with the requirement

    """
    invalid_records = []
    try:
        requirement = specifications[status_req_id]
    except KeyError:
        raise KeyError(f"{status_req_id} is not present in the specifications file.")

    if requirement.get("type") != "status":
        raise ValueError(f"{status_req_id} is not a status requirement.")

    try:
        parameter = requirement["parameter"]
    except KeyError:
        raise KeyError(f"{status_req_id} is missing the parameter attribute in the specifications file.")

    try:
        req_status = requirement["value"]
    except KeyError as e:
        raise KeyError(f"{status_req_id} is missing the {e} in the specifications file.")

    for data in telemetry:
        telemetry_status = data.get(parameter)
        if telemetry_status is None:
            raise ValueError(
                f"Telemetry record {data.get('packet_sequence')} does not contain {parameter} info.")
        if telemetry_status != req_status:
            print(
                f"WARNING: {data.get('packet_sequence')} does not comply with {status_req_id} "
                f"--> {telemetry_status} is not equal to  {req_status}")
            invalid_records.append(data.get('packet_sequence'))
    if invalid_records:
        print(f"Found {len(invalid_records)} records that do not comply with {status_req_id}")
    return invalid_records


def check_sequence(telemetry: list, specifications: dict, seq_req_id: str) -> list:
    """
    This function verifies that the packet_sequence are incremented by a step define in the requirement

    :param telemetry: list of telemetry records
    :param specifications: dictionary of requirements
    :param seq_req_id: ID of the sequence requirement to verify (e.g. "REQ-SEQ-001")
    :return: List of packet sequences that do not follow the previous one
    """
    invalid_seq = []

    try:
        requirement = specifications[seq_req_id]
    except KeyError:
        raise KeyError(f"{seq_req_id} is not present in the specifications file.")

    if requirement.get("type") != "sequence":
        raise ValueError(f"{seq_req_id} is not a sequence requirement.")

    try:
        parameter = requirement["parameter"]
    except KeyError:
        raise KeyError(f"{seq_req_id} is missing the parameter attribute in the specifications file.")

    try:
        seq_step = requirement["step"]
    except KeyError as e:
        raise KeyError(f"{seq_req_id} is missing the {e} in the specifications file.")

    if type(seq_step) is not int:
        raise TypeError(f"{seq_req_id} has an invalid 'step' ({seq_step!r}), it must be an integer.")

    previous_seq = None
    for data in telemetry:
        current_sequence = data.get(parameter)
        if current_sequence is None:
            raise ValueError(f"One telemetry record does not contain {parameter} info.")

        if previous_seq is None:
            previous_seq =  current_sequence
            continue
        elif current_sequence != previous_seq + seq_step:
            invalid_seq.append(current_sequence)
        previous_seq = current_sequence

    return invalid_seq


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


def get_requirement_info(specifications: list, req_id: str, attributes: list, req_type: str) -> dict:
    req_info = {}

    try:
        requirement = specifications[req_id]
        req_info["requirement"] = requirement
    except KeyError:
        raise KeyError(f"{req_id} is not present in the specifications file.")

    if requirement.get("type") != req_type:
        raise ValueError(f"{req_id} is not a {req_type} requirement.")

    for att in attributes:
        try:
            req_info[att] = requirement[att]
        except KeyError:
            raise KeyError(f"{req_id} is missing the {e} in the specifications file.")

    return req_info


if __name__ == "__main__":

    telemetry_path = PROJECT_ROOT / "data" / "telemetry.json"
    req_path = PROJECT_ROOT / "specifications" / "requirements.json"

    for req_id in ["REQ-TEMP-001", "REQ-BATTERY-001", "REQ-SIGNAL-STRENGTH-001", "REQ-SEQ-001"]:
        try:
            # my_data = get_data(telemetry_path)
            requirements = get_requirements(req_path)
            # check_range(my_data, requirements, req_id)
            input_telemetry = [
                {
                    "packet_sequence": 1042,
                }, {
                    "packet_sequence": 1043,
                }, {
                    "packet_sequence": 1044,
                }]
            print(check_sequence(input_telemetry, requirements, req_id))
        except (ValueError, FileNotFoundError, KeyError) as e:
            print(f"ERROR: {e}")

    try:
        check_status(get_data(telemetry_path), get_requirements(req_path), "REQ-COMM-001")
    except (ValueError, FileNotFoundError, KeyError) as e:
        print(f"ERROR: {e}")
