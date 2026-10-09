# Requirements Meeter Output

## Zipsafe Decision
- **Result**: false
- **Reason**: Packages with data files — botocore ships JSON service model and endpoint data files (e.g. `botocore/data/endpoints.json`, `botocore/cacert.pem`) that cannot be loaded from inside a zip archive

## CLI Tools
- None — the extension uses boto3 SDK calls exclusively and does not invoke any CLI tools

## Python Dependencies
- boto3==1.42.97 — Has data files (botocore dependency ships JSON service models and endpoint data); version corrected from analysis spec 1.43.110 (non-existent on PyPI) to latest available 1.42.97
- botocore==1.42.97 — Has data files (JSON service model files under `botocore/data/`, `botocore/cacert.pem`); version corrected from analysis spec 1.43.110 to latest available 1.42.97
- tabulate==0.9.0 — Pure Python; version corrected from analysis spec 0.10.0 (non-existent on PyPI) to latest available 0.9.0; supports `rounded_outline` table format

## Setup.py Changes
- VENDOR_FOLDER added: no (already present in setup.py; no CLI binaries to vendor)
- data_files updated: no (setup.py already handles the zip_safe=False path correctly, including conditional VENDOR_FOLDER inclusion when vendor directory exists)
