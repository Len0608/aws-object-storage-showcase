<!-- generated: 2026-10-09 00:00 -->

# Project Analysis — Universal Extension v1.0.0

## Purpose

Provides Stonebranch Universal Controller tasks for interacting with AWS S3 object storage, supporting listing bucket objects and uploading local files from the Universal Agent host.

---

## Execution Modes / Actions

| Mode | Trigger | Description |
|---|---|---|
| List Objects | `input_data.action.value == "List Objects"` | Lists all objects in the specified S3 bucket; respects `UE_MAX_OUTPUT_RECORDS` env var to cap output rows |
| Upload File | `input_data.action.value == "Upload File"` | Uploads a local file from the agent host to an S3 bucket at a specified object key |

Dispatch mechanism: `ACTION_MAPPER.get(input_data.action.value)` in `extension.py:execute()`.

---

## Complete Field Table

| name | label | fieldType | required | requireIfVisible | choices | showIfField | showIfFieldValue | requireIfField | requireIfFieldValue | hint |
|---|---|---|---|---|---|---|---|---|---|---|
| action | Action | Choice | false | false | List Objects, Upload File | — | — | — | — | Select the S3 operation to perform |
| aws_credentials | AWS Credentials | Credential | true | false | — | — | — | — | — | AWS IAM credentials: user=Access Key ID, password=Secret Access Key, token=Session Token (optional) |
| aws_region | AWS Region | Text | true | false | — | — | — | — | — | AWS region identifier, e.g. us-east-1 |
| bucket_name | Bucket Name | Text | true | false | — | — | — | — | — | Target S3 bucket name, e.g. my-demo-bucket |
| local_file | Local File Path | Text | false | true | — | Choice Field 1 | Upload File | — | — | Absolute path on the agent host to the local file to upload, e.g. /tmp/report.csv |
| s3_object_key | S3 Object Key | Text | false | true | — | Choice Field 1 | Upload File | — | — | Destination key in the S3 bucket, e.g. reports/report.csv |
| status | Status | Text (Output Only) | false | false | — | — | — | — | — | Short human-readable summary of the action result |
| object_count | Object Count | Text (Output Only) | false | false | — | — | — | — | — | Total number of objects found in the bucket (List Objects action only) |

---

## Cross-references

**Always-required fields**
- `aws_credentials` — always required
- `aws_region` — always required
- `bucket_name` — always required

**Conditionally-required fields (requireIfVisible = true)**
- `local_file` — required when visible; visible only when `action` = "Upload File"
- `s3_object_key` — required when visible; visible only when `action` = "Upload File"

**Field visibility dependencies (showIfField)**
- `local_file` → `showIfField: "Choice Field 1"`, `showIfFieldValue: "Upload File"`
- `s3_object_key` → `showIfField: "Choice Field 1"`, `showIfFieldValue: "Upload File"`

**Mutually exclusive options**
- `action` drives two mutually exclusive modes:
  - `"List Objects"` — `local_file` and `s3_object_key` hidden; `object_count` output is populated
  - `"Upload File"` — `local_file` and `s3_object_key` shown and required; `object_count` not applicable

---

## Error Handling

| Scope | Error | Handling |
|---|---|---|
| `extension.py:execute()` | `ExecutionError` (base) | Caught; logged; added to ExtensionManager; returns `build_result` with typed exit code and message |
| `extension.py:execute()` | Any unhandled `Exception` | Wrapped in `UnexpectedSystemError`; added to ExtensionManager; returns `build_result` |
| `actions/upload_file.py` | Missing required fields (`aws_region`, `bucket_name`, `local_file`, `s3_object_key`) | Raises `ValidationError` per field |
| `actions/upload_file.py` | Local file not found on agent host | Raises `LocalFileNotFoundError` |
| `actions/list_objects.py` | Missing `aws_region` or `bucket_name` | Raises `ValidationError` |
| `actions/list_objects.py` | `UE_MAX_OUTPUT_RECORDS` non-integer | `ValueError` caught locally; falls back to default record limit |
| `utility.py:list_all_objects()` | `botocore.exceptions.ClientError` | Caught; delegated to `_raise_from_client_error` |
| `utility.py:upload_file()` | `botocore.exceptions.ClientError` | Caught; delegated to `_raise_from_client_error` |
| `utility.py:_raise_from_client_error()` | Auth error codes | Raises `AuthenticationError` |
| `utility.py:_raise_from_client_error()` | `NoSuchBucket` | Raises `BucketNotFoundError` |
| `utility.py:_raise_from_client_error()` | Access denied codes | Raises `AccessDeniedError` |
| `utility.py:_raise_from_client_error()` | Other ClientError | Raises `S3ServiceError` |
