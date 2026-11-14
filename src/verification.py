import csv
from pathlib import Path
from src.telemetry import check_range, check_status, check_sequence, get_requirements, get_telemetry_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def produce_requirement_results(telemetry: list, requirements: dict) -> list:
    """Check the telemetry against every requirement and build one result row per requirement.

    The checker is chosen from the requirement "type": "range", "status" or "sequence".

    Args:
        telemetry: List of telemetry records.
        requirements: Requirements keyed by requirement ID.

    Returns:
        List of rows [requirement_id, status, failing_packets], where status is
        "PASS" or "FAIL" and failing_packets lists the failing packet_sequence
        numbers joined with ";" (empty string on PASS).

    Raises:
        ValueError: If a requirement has an unknown type.
        Errors raised by the checkers are not caught.
    """
    csv_rows = []
    invalid_record = []
    for req_id, req in requirements.items():
        match req.get("type"):
            case "range":
                invalid_record = check_range(telemetry, requirements, req_id)
            case "status":
                invalid_record = check_status(telemetry, requirements, req_id)
            case "sequence":
                invalid_record = check_sequence(telemetry, requirements, req_id)
            case _:
                raise ValueError(f"{req_id} has an unknown type: {req.get('type')}")

        req_status = "FAIL" if invalid_record else "PASS"
        failing_packets = ';'.join(str(p) for p in invalid_record)
        csv_rows.append([req_id, req_status, failing_packets])
    return csv_rows


def write_results_csv_file(csv_path: Path, csv_rows: list) -> None:
    """Write the requirement results to a CSV file, with a header row.

    The file is overwritten if it already exists. The parent folder must exist.

    Args:
        csv_path: Path of the CSV file to write.
        csv_rows: Rows returned by produce_requirement_results.

    Raises:
        FileNotFoundError: If the parent folder of csv_path does not exist.
    """
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        header = ['requirement', 'status', 'failing_packets']
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(csv_rows)


if __name__ == "__main__":
    telemetry_path = PROJECT_ROOT / "data" / "telemetry.json"
    req_path = PROJECT_ROOT / "specifications" / "requirements.json"

    report_dir_path = PROJECT_ROOT / "reports"
    # Create the directory safely
    report_dir_path.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir_path / "requirements_report.csv"

    requirements = get_requirements(req_path)
    telemetry = get_telemetry_data(telemetry_path)

    res = produce_requirement_results(telemetry, requirements)
    write_results_csv_file(csv_path, res)
