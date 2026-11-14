# Satellite Ground System Test

A small Python project that verifies satellite telemetry against a list of requirements.
Requirements are stored in a JSON file, telemetry is read from another JSON file, and Python
functions check each telemetry record against each requirement. The checking functions are tested
with pytest. Running the verification produces a CSV report with a PASS or FAIL result per requirement.

A Jenkins pipeline, defined in the `Jenkinsfile`, runs the tests and the verification, and archives
the CSV report.

## Why this project exists

The repository shows a requirements-based verification workflow:

- read telemetry data from disk
- compare telemetry values against engineering requirements
- report which requirements fail and which telemetry records cause the failure
- keep requirements in a separate JSON file so they can be changed without touching the code
- test the checking functions with pytest
- run everything in a CI pipeline

## Requirements

The requirements are in `specifications/requirements.json`. The values are made up for this
exercise.

| ID | Type | Parameter | Rule |
|---|---|---|---|
| REQ-TEMP-001 | range | temperature | between -20 and 60 °C, inclusive |
| REQ-BATTERY-001 | range | battery_voltage | between 24 and 32 V, inclusive |
| REQ-SIGNAL-STRENGTH-001 | range | signal_strength | between -90 and 0, inclusive |
| REQ-COMM-001 | status | communication_status | must be "OK" |
| REQ-SEQ-001 | sequence | packet_sequence | each packet number is the previous one plus 1 |

The `type` of a requirement decides which checker verifies it.

## Telemetry data

`data/telemetry.json` contains a list of telemetry records with these fields: timestamp,
satellite_id, temperature, battery_voltage, signal_strength, packet_sequence, communication_status.

The sample file has six records with injected faults: one temperature above the limit, two battery
voltages above the limit, and packet numbers that repeat and go backwards.

## How it works

- `check_range`, `check_status` and `check_sequence` (in `src/telemetry.py`) each verify one
  requirement against the telemetry and return the packet sequence numbers of the records that do
  not comply. They raise an error when the requirement or a telemetry record is invalid.
- `produce_requirement_results` (in `src/verification.py`) runs every requirement in the file with
  the checker that matches its type, and returns one result row per requirement. An unknown type
  raises a `ValueError`.
- `write_results_csv_file` writes the rows to a CSV file.

## Tests

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
├── Jenkinsfile                 # CI pipeline
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

Verify the telemetry against the requirements (writes `reports/requirements_report.csv`, and
creates the `reports/` folder if needed):

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

With the sample `data/telemetry.json`, the report is:

```csv
requirement,status,failing_packets
REQ-TEMP-001,FAIL,1044
REQ-BATTERY-001,FAIL,1044;1045
REQ-SIGNAL-STRENGTH-001,PASS,
REQ-COMM-001,PASS,
REQ-SEQ-001,FAIL,1042;1044
```

When several records fail a requirement, their packet numbers are separated by `;`. For
REQ-SEQ-001, the listed packets are the ones where the sequence breaks.

## CI

The pipeline is defined in the `Jenkinsfile` and runs on a local Jenkins instance. Builds are
started manually.

| Stage | What it does |
|---|---|
| Setup | creates a virtual environment and installs `requirements.txt` |
| Tests | runs pytest |
| Verify | runs `python -m src.verification` |

If a stage fails, the following stages do not run. When all stages pass, the CSV report is
archived with the build.

The Verify stage does not fail the build when a requirement fails. The PASS/FAIL result per
requirement is in the archived CSV.

The Setup stage points to the Python installation on my machine. Change that path to run the
pipeline elsewhere.

## What this demonstrates technically

- **Requirements as data.** Limits and expected values live in `requirements.json`. The checker is
  chosen from the requirement type, so a new requirement of an existing type needs no code change.
- **Traceability from requirement to record.** Each FAIL in the report lists the packet sequence
  numbers of the records that caused it.
- **Explicit error handling.** Invalid requirements, invalid records and unknown requirement types
  raise errors with clear messages instead of producing a silent PASS.
- **Isolated unit tests.** Checker tests use their own small data, so a change to the sample
  telemetry or requirements does not break them. Error tests check the exact message.
- **Pipeline as code.** The CI steps are versioned in the repository. Each build starts from a fresh
  virtual environment and keeps the report as a build artifact.