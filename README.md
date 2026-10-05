# Satellite Ground System Test

This project is a small Python-based telemetry validation example for a satellite ground system. It reads sample telemetry data from a JSON file, loads requirement definitions from another JSON file, and checks whether the recorded values stay within the configured limits.


## Why this project exists

The repository demonstrates a lightweight monitoring workflow often used in mission operations:

- ingest telemetry payloads from disk
- compare sensor readings against engineering requirements
- flag out-of-range values for review
- keep requirements in a separate JSON specification file for easy updates

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

The specification file at `specifications/requirements.json` stores requirement thresholds in JSON format. It currently includes:

- `REQ-TEMP-001`: temperature must be in the range [-20, 60]

The actual Python script currently validates the temperature requirement, but the structure is ready to be extended to the battery requirement and other telemetry checks.

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
