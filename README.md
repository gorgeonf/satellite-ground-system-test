# Satellite Ground System Test

This project is a small Python telemetry verification example for a satellite ground system.
It reads sample telemetry data from a JSON file, loads requirement definitions from another JSON file,
and checks whether the recorded values comply with the requirements. The checking functions are
tested with pytest, and the tests run on Jenkins.

## Why this project exists

The repository shows a requirements-based verification workflow:

- read telemetry data from disk
- compare telemetry values against engineering requirements
- report records that do not comply with a requirement
- keep requirements in a separate JSON specification file so they can be changed without touching the code
- test the checking functions with pytest
- run the tests on Jenkins, manually and automatically when the GitHub repository changes

## Project structure

```text
.
├── data/
│   └── telemetry.json          # sample telemetry payload
├── specifications/
│   └── requirements.json       # requirement thresholds
├── src/
│   └── telemetry.py            # telemetry validation logic
├── tests/
│   └── test_telemetry.py       # placeholder for future automated tests
├── requirements.txt            # Python dependencies
├── README.md                   # project documentation
├── .gitignore
└── .venv/                      # local virtual environment
```

## Data and requirements

### Telemetry data

The data file at `data/telemetry.json` contains a list of telemetry records such as:

- timestamp
- satellite identifier
- temperature
- battery voltage
- signal strength
- packet sequence
- communication status

### Requirement definitions

The specification file at `specifications/requirements.json` stores requirement thresholds in JSON format. It currently
includes:

- `REQ-TEMP-001`: temperature must be in the range [-20, 60]

The actual Python script currently validates the temperature requirement, but the structure is ready to be extended to
the battery requirement and other telemetry checks.

## Setup

Create and activate a virtual environment, then install dependencies:

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

## Notes

This project is intentionally minimal and is meant as a starter example for ground-system telemetry screening.
It can be expanded to support more requirements, richer validation logic, alerting, and CLI-based reporting.
