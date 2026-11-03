# Satellite Ground System Test

A small Python project that verifies satellite telemetry against a list of requirements.
Requirements are stored in a JSON file, telemetry is read from another JSON file, and Python
functions check each telemetry record against each requirement. The checking functions are tested
with pytest. Running the verification produces a CSV report with a PASS or FAIL result per requirement.

CI on Jenkins (manual runs and runs triggered by changes in the GitHub repository) is planned.

## Why this project exists

The repository shows a requirements-based verification workflow:

- read telemetry data from disk
- compare telemetry values against engineering requirements
- report which requirements fail and which telemetry records cause the failure
- keep requirements in a separate JSON file so they can be changed without touching the code
- test the checking functions with pytest

## Requirements

The requirements are in `specifications/requirements.json`. The values are made up for this
exercise.

| ID | Type | Parameter | Rule |
|---|---|---|---|
| REQ-TEMP-001 | range | temperature | between -20 and 60, inclusive |
| REQ-BATTERY-001 | range | battery_voltage | between 24 and 32, inclusive |
| REQ-SIGNAL-STRENGTH-001 | range | signal_strength | between its min and max limits, inclusive |
| REQ-COMM-001 | status | communication_status | must be "OK" |
| REQ-SEQ-001 | sequence | packet_sequence | each packet number is the previous one plus 1 |

The `type` of a requirement decides which checker verifies it.

## Telemetry data

`data/telemetry.json` contains a list of telemetry records with these fields: timestamp,
satellite_id, temperature, battery_voltage, signal_strength, packet_sequence, communication_status.

## Test architecture

- `check_range`, `check_status` and `check_sequence` (in `src/telemetry.py`) each verify one
  requirement against the telemetry and return the packet sequence numbers of the records that do
  not comply. They raise an error when the requirement or a telemetry record is invalid.
- `produce_requirement_results` (in `src/verification.py`) runs every requirement in the file with
  the checker that matches its type, and returns one result row per requirement.
  `write_results_csv_file` writes the rows to a CSV file.
- Checker tests build their own small requirements and telemetry in the test, so they only fail
  when a checker is broken. Boundary values, empty input and error cases are covered with
  parametrized tests, and error tests assert the exact error message.
- The functions that read files are tested with small files in `tests/data/`.
- One test checks that the real `requirements.json` contains `REQ-TEMP-001` with its limits.

## Project structure

```text
.
├── data/
│   └── telemetry.json          # sample telemetry
├── specifications/
│   └── requirements.json       # requirements
├── src/
│   ├── telemetry.py            # file loading and requirement checkers
│   └── verification.py         # runs all checkers and writes the CSV report
├── tests/
│   ├── data/                   # small files used by the loading tests
│   ├── conftest.py             # fixtures
│   └── test_*.py               # pytest tests
├── reports/                    # generated report (ignored by git)
├── requirements.txt
└── README.md
```

## Setup

Create and activate a virtual environment, then install the dependencies.

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS/Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## How to run

Run all commands from the project root.

Verify the telemetry against the requirements (writes `reports/requirements_report.csv`):

```bash
python -m src.verification
```

Run the tests:

```bash
pytest
```

Use `python -m src.verification` and not `python src/verification.py`, which fails with a
`ModuleNotFoundError` because of the `src.` imports.

## Example verification result

For the three sample records in `data/telemetry.json` (the third one has a temperature of 65),
the report is:

```csv
requirement,status,failing_packets
REQ-TEMP-001,FAIL,1044
REQ-BATTERY-001,PASS,
REQ-SIGNAL-STRENGTH-001,PASS,
REQ-COMM-001,PASS,
REQ-SEQ-001,PASS,
```

When several records fail a requirement, their packet numbers are separated by `;`.

## CI

Planned: a Jenkins job that runs `pytest`, started manually and automatically when the GitHub
repository changes.